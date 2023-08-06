
from collections import abc as collection
import json
from fmp import wrappers_pb2 as fmp_wrappers
import google.protobuf.wrappers_pb2 as pb
from grpc import (
    StatusCode,
    RpcError
)
from arista.studio.v1 import models, services

MAINLINE_WS_ID = ""
# ID of the "Inventory and Topology" studio that enumerates all devices and interfaces
# available to studios
TOPOLOGY_STUDIO_ID = "TOPOLOGY"
RPC_TIMEOUT = 30  # in seconds


def GetOneForFullWSState(apiClientGetter, stateStub, stateGetReq, configStub, confGetAllReq):
    '''
    For Studio APIs, the state for a particular workspace can be difficult to determine.
    A state for a particular workspace only exists if an update has occurred for that workspace,
    and even then may only exist in a partial manner.
    State may also exist in mainline, or the configuration change in the workspace may have
    explicitly deleted the state.

    NOTE: If a ws state only exists in the ws (e.g. is part of a studio added in the ws itself),
    this method will return an RPCError with a code() of StatusCode.NOT_FOUND

    GetOneForFullWSState does the following to provide the information necessary to construct
    the full resource state for the workspace:
        - Issue get on the X state endpoint for the mainline state.
        - If the state DOES exist there, check the X configuration endpoint of the workspace to
          see if the state has been explicitly deleted there.

    Params:
    - apiClientGetter:  The API client getter, i.e. ctx.getApiClient
    - stateStub:        The stub for the state endpoint
    - stateGetReq:      A workspace-aware get request to be made to the state client for mainline.
    - configStub:       The stub for the config endpoint
    - confGetAllReq:    A workspace-aware get all request to be made to the config client for the
                        desired workspace.

    Returns:
    - The mainline state value, or None if the resource has been deleted
    - The list of configurations applied to the state in the workspace
    '''

    if not hasattr(stateGetReq.key, 'workspace_id'):
        raise ValueError("Passed request to GetOneWithWS has no key attribute 'workspace_id'")

    stateClient = apiClientGetter(stateStub)
    if stateGetReq.key.workspace_id.value != MAINLINE_WS_ID:
        stateGetReq.key.workspace_id.value = MAINLINE_WS_ID
    # Issue a get to the state endpoint for Mainline
    result = stateClient.GetOne(stateGetReq)

    # Check the config endpoint for the workspace to ensure that
    # the mainline value has not been deleted
    configClient = apiClientGetter(configStub)

    configs = []
    for resp in configClient.GetAll(confGetAllReq, timeout=RPC_TIMEOUT):
        configs.append(resp.value)

    return result.value, configs


def getCompleteInputState(apiClientGetter, wsID):
    wid = pb.StringValue(value=wsID)
    sid = pb.StringValue(value=TOPOLOGY_STUDIO_ID)

    stateGetReq = services.InputsRequest(
        key=models.InputsKey(studio_id=sid, workspace_id=wid,
                             path=fmp_wrappers.RepeatedString(values=[])))

    confGetAllReq = services.InputsConfigStreamRequest()
    confGetAllReq.partial_eq_filter.append(
        models.Inputs(key=models.InputsKey(studio_id=sid, workspace_id=wid))
    )

    mainlineState, configs = GetOneForFullWSState(apiClientGetter=apiClientGetter,
                                                  stateStub=services.InputsServiceStub,
                                                  stateGetReq=stateGetReq,
                                                  configStub=services.InputsConfigServiceStub,
                                                  confGetAllReq=confGetAllReq)
    for conf in configs:
        prevInput = None
        inputToUpdate = mainlineState
        for elem in conf.key.path:
            prevInput = inputToUpdate
            inputToUpdate = inputToUpdate[elem]

        if conf.remove:
            prevInput.pop(conf.key.path[-1], None)
        else:
            confInputs = json.loads(conf.inputs.value)
            __update(inputToUpdate, confInputs)

    return mainlineState


def __update(d, u):
    for k, v in u.items():
        if isinstance(v, collection):
            d[k] = __update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
