# This file is an example of how to use the the raw DROID gRPC client.
# In practice you would want to use the Client class in main.py instead.

import asyncio

from grpclib.client import Channel

from droid_grpc import DroidStub
from droid_pb2 import BatchCreateRequest, BatchCreateResponse
from formatting import (
    create_request_dict_to_proto,
    hedge_request_dict_to_proto,
    create_response_proto_to_dict,
    hedge_response_proto_to_dict
)
from numpy import array

def create_bot_base_values_generator():
    data = {
        'ticker': array(['AAPL.O'], dtype='<U6'), 
        'spot_date': array(['2023-01-19'], dtype='datetime64[D]'), 
        'bot_id': array(['UNO_ITM_025'], dtype='<U14'), 
        'multiplier_1': array([-4.31301907]), 
        'multiplier_2': array([2.64497467]), 
        'price': array([509299.9958627]), 
        'fraction': array([False]), 
        'margin': array([3.45183316]), 
        'investment_amount': array([240338.00809266]), 
        'atm_volatility_spot': array([1.52595116]), 
        'atm_volatility_one_year': array([0.18815144]), 
        'atm_volatility_infinity': array([0.32524658]), 
        'slope': array([6.35573421]), 
        'slope_inf': array([2.93640623]), 
        'deriv': array([0.19231628]), 
        'deriv_inf': array([-0.12714732]), 
        'r': array([0.12255669]), 
        'q': array([9.55143566e-06])
    }
    for i in range(1):
        proto = create_request_dict_to_proto(data)
        yield proto
    
def hedge_bot_base_values_generator():
    data = {
        'ticker': array(['AAPL.O', 'AAPL.O', 'AAPL.O'], dtype='<U6'), 
        'bot_id': array(['UNO_OTM_05', 'UNO_ITM_016666', 'UNO_OTM_007692'], dtype='<U14'), 
        'last_share_num': array([1165.,    0., 1301.]), 
        'total_bot_share_num': array([1165, 7786, 3455]), 
        'price_level_1': array([175605.47263322, 315544.76675577, 366086.02791683]), 
        'price_level_2': array([202070.67160607, 375277.54975171, 387354.08043229]), 
        'spot_date': array(['2020-08-08', '2021-09-01', '2021-07-18'], dtype='datetime64[D]'), 
        'expire_date': array(['2021-06-25', '2021-10-28', '2021-07-18'], dtype='datetime64[D]'), 
        'price': array([923711.00854766, 584450.07504951, 222233.42987555]), 
        'fraction': array([ True,  True,  True]), 
        'margin': array([1.38665455, 5.75109741, 7.82989436]), 
        'investment_amount': array([ 369833.95147724, 1183754.0878817 ,  919393.56218934]), 
        'atm_volatility_spot': array([ 1.45171069,  1.34702482, -0.33065873]), 
        'atm_volatility_one_year': array([0.71657428, 0.94830164, 0.71680603]), 
        'atm_volatility_infinity': array([0.74670436, 0.58360164, 0.61856561]), 
        'slope': array([5.90734333, 2.0645404 , 5.95029074]), 
        'slope_inf': array([4.21320814, 5.3027279 , 2.57661038]), 
        'deriv': array([0.05471683, 0.2345494 , 0.39241127]), 
        'deriv_inf': array([-3.17944069, -1.29908935,  1.28468478]), 
        'r': array([1.85214759e-01, 9.14655018e-05, 1.96355226e-01]), 
        'q': array([0.00342752, 0.00089481, 0.00042698])
    }
    for i in range(1):
        proto = hedge_request_dict_to_proto(data)
        yield proto

async def create_bots(stub: DroidStub) -> None:
    msgs = create_bot_base_values_generator()
    async with stub.CreateBots.open() as stream:
        for msg in msgs:
            await stream.send_message(msg)
            resp = await (stream.recv_message())
            resp = create_response_proto_to_dict(resp)
            print("CREATE RESPONSE\n---")
            for k, v in resp.items():
                print(k, v)
            print("---\n\n")

        await stream.end()

async def hedge_bots(stub: DroidStub) -> None:
    msgs = hedge_bot_base_values_generator()
    async with stub.HedgeBots.open() as stream:
        for msg in msgs:
            await stream.send_message(msg)
            resp = await (stream.recv_message())
            resp = hedge_response_proto_to_dict(resp)
            print("HEDGE RESPONSE\n---")
            for k, v in resp.items():
                print(k, v)
            print("---\n\n")

        await stream.end()

async def main():
    channel = Channel('droid.droid', 50065)
    stub = DroidStub(channel)
    create = asyncio.create_task(create_bots(stub))
    hedge = asyncio.create_task(hedge_bots(stub))
    await asyncio.gather(create, hedge)

if __name__ == '__main__':
    asyncio.run(main())

