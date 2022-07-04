from log import Log

import aminofix as af
import datetime


async def chooseCom(client, device_id: str = None):
    '''
    Choose a community

    Param:
        Params:
        client - global amino client class object to execute function
        device_id - random device_id

    Succes:
        returns community subclient class object 

    Fail:
        returns exeption
    '''
    ###################################### get list of communites ######################################
    try:
        clientList = await client.sub_clients(size=100)
    except Exception as e:
        print(f'{datetime.datetime.now()} [ERROR] {e}')
        return e

    ###################################### print communites ############################################
    i = 1
    for name, comID, uc in zip(clientList.name, clientList.comId, clientList.usersCount):
        print("{}: {}\n\tId: {}\n\tNumber of users: {}".format(i, name, comID, uc))
        i += 1

    community = int(input(f'[INPUT] Choose a community (1 - {i-1}): '))
    comId = clientList.comId[community - 1]
    
    ###################################### enter the community #########################################
    try:
        subClient = af.asyncfix.SubClient(comId=comId, profile=client.profile, deviceId=device_id)
    except Exception as e:
        Log.print_error_msg('{e}')
        return e

    return subClient, comId