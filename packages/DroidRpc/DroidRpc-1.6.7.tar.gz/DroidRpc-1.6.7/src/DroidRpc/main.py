# Python client for connecting to LORA Research's bot services

__author__ = "LORA Research"
__email__ = "asklora@loratechai.com"

import asyncio
import socket
from .droid_grpc import DroidStub
from .droid_pb2 import (
    BatchCreateRequest, 
    BatchCreateResponse, 
    BatchHedgeRequest, 
    BatchHedgeResponse,
)
from grpclib.client import Channel
from typing import Optional, Generator, Dict, Any, List
from itertools import cycle
from numpy.typing import NDArray
import numpy as np
import pandas as pd
from .formatting import (
    array_to_bytes,
    bytes_to_array,
    create_request_dict_to_proto,
    hedge_request_dict_to_proto,
    create_response_proto_to_dict,
    hedge_response_proto_to_dict
)


class Client:
    """
    This is a thick client, and wraps the raw gRPC client.
    It implements different calling methods for creating and hedging bots, as 
    well as client-side load balancing to accommodate horizontal scaling of the 
    droid server.

    Current implementation will not discover new servers after the client is
    initialized, but will remove dead servers from the pool.

    *Note: Input validation is done server side. DROID server is a headless svc.
    """
    def __init__(
            self,
            host: str = "droid.droid",
            port: int = 50065,
            max_retries: int = 3,
            max_batch_size: int = 400,
        ):
        """
        Args:
            host: The host name to connect to.
            port: The port to connect to.
            max_retries: The maximum number of retries to attempt.
        """
        self.host = host
        self.port = port
        self.max_retries = max_retries
        self.max_batch_size = max_batch_size
        
        self._pool = [] # List of channels for all DROID servers
        self._pool_itr = None # Iterator for client-side load balancing
        self.renew_pool()

    def  __repr__(self) -> str:
        return f"""
Droid Client:
    Host: {self.host}
    Port: {self.port}
    Batch Size: {self.max_batch_size}
    IP Pool: {[x["ip"] for x in self._pool]}
    Connected: {self.connected}
    Connections: {self.connections}
        """

    async def __aenter__(self) -> "Client": 
        return self
    
    async def __aexit__(self, *args) -> None:
        await self.close()

    def _new_subclient(self, ip: str) -> Dict[str, Any]:
        """Creates a sub-client stored as a dict."""
        channel = Channel(ip, self.port)
        return {
            "ip": ip,
            "channel": channel,
            "stub": DroidStub(channel),
        }

    def _get_ips(self) -> List[str]:
        """Returns available server IPs."""
        ips = []
        ais = socket.getaddrinfo(self.host,0,0,0,0)
        for result in ais:
            ips.append(result[-1][0])
        return list(set(ips)) # Remove duplicates
    
    def _remove_dead_subclients(self) -> None:
        """Removes channels that are dead."""
        if self._pool_itr is None: return
        # for subclient in self._pool:
        #     if not subclient["channel"]._connected:
        #         subclient["channel"].close()
        #         self._pool.remove(subclient)
        if len(self._pool) == 0:
            raise ConnectionError("No available servers.")

    def renew_pool(self) -> None:
        """Updates pool of subclients with available servers."""
        self._remove_dead_subclients()
        pool = self._pool
        available_ips = self._get_ips()
        current_ips = [subclient["ip"] for subclient in pool]
        new_ips = list(set(available_ips) - set(current_ips))
        # Add new subclients to pool
        for ip in new_ips:
            pool.append(self._new_subclient(ip))
            self._pool_itr = cycle(pool)
        self.max_retries = len(self._pool)
    
    @property
    def connected(self) -> bool:
        """Checks if the client is connected to any server."""
        # FIXME the connected property only == True after the first call
        for subclient in self._pool:
            if subclient["channel"]._connected:
                return True
        return False
    
    @property
    def connections(self) -> List[str]:
        """Returns a count of connected servers."""
        conns = 0
        for subclient in self._pool:
            if subclient["channel"]._connected:
                conns += 1
        return conns

    async def close(self) -> None:
        """Closes the all subclient connections."""
        for subclient in self._pool:
            subclient["channel"].close()
        assert self.connections == 0, "Failed to close all connections."

    async def create_bot(
            self,
            ticker: str,
            spot_date: np.datetime64,
            bot_id: str,
            investment_amount: np.float32,
            price: np.float32,
            margin: Optional[np.float16] = None,
            fraction: Optional[bool] = None,
            multiplier_1: Optional[np.float16] = None,
            multiplier_2: Optional[np.float16] = None,
            r: Optional[np.float32] = None,
            q: Optional[np.float32] = None,
            # TODO: add other optional inputs for create/hedge_bot(s)
        ) -> Dict[str, NDArray]:
        """
        Create a single bot.
        *Note: Actually just wraps the batch function (create_bots).

        Args:
            ticker: The ticker of the underlying asset.
            spot_date: Bot start date.
            bot_id: Composite id of bot type, option type, and holding period.
            investment_amount: Initial investment amount.
            price: Current price of stock.
            margin: Margin ratio (e.g. 1 = no margin).
            fraction: Whether fractional shares are allowed.
            multiplier_1: Multiplier (1) for target price level (1); 
                e.g. [Classic] - [stop loss] should be negative. 
            multiplier_2: Multiplier (2) for target price level (2), 
                must be > Multiplier (1).
            r: Interest rate.
            q: Dividend yield.

        Returns:
            dict: A dictionary of bot properties.
        """
        inputs = locals().copy()
        inputs.pop('self')
        inputs = {k: np.array([v]) for k, v in inputs.items() if v is not None}
        resp = await self.create_bots(**inputs)
        return {k: v[0] for k, v in resp.items() if v is not None}
    
    async def create_bots(
            self,
            ticker: NDArray[str],
            spot_date: NDArray[np.datetime64],
            bot_id: NDArray[str],
            investment_amount: NDArray[np.float32],
            price: NDArray[np.float32],
            margin: Optional[NDArray[np.float16]] = None,
            fraction: Optional[NDArray[bool]] = None,
            multiplier_1: Optional[NDArray[np.float16]] = None,
            multiplier_2: Optional[NDArray[np.float16]] = None,
            r: Optional[np.float32] = None,
            q: Optional[np.float32] = None,
        ) -> Dict[str, NDArray]:
        """
        Creates a batch of bots from a dictionary of inputs.
        The inputs must be arrays.

        Args:
            ticker: The tickers of the underlying asset.
            spot_date: Bot start dates.
            bot_id: Composite ids of bot type, option type, and holding period.
            investment_amount: Initial investment amounts.
            price: Current price of the stocks.
            margin: Margin ratios (e.g. 1 = no margin).
            fraction: Whether fractional shares are allowed.
            multiplier_1: Multipliers (1) for target price levels (1); 
                e.g. [Classic] - [stop loss] should be negative. 
            multiplier_2: Multipliers (2) for target price levels (2), 
                must be > Multiplier (1).
            r: Interest rates.
            q: Dividend yields.

        Returns:
            dict: A dictionary of bot properties.
        """
        inputs = locals().copy()
        inputs.pop('self')
        inputs = {k: array_to_bytes(v) for k, v in inputs.items() \
            if v is not None}
        assert len(inputs['ticker']) <= self.max_batch_size, \
            f"Max batch size ({self.max_batch_size}) exceeded."

        conn_err = False
        for _ in range(self.max_retries):
            try:
                resp = await next(self._pool_itr)["stub"].CreateBots(
                    BatchCreateRequest(**inputs))
                break
            except ConnectionRefusedError:
                print('DROID connection error. Retrying...')
                self._remove_dead_subclients()
                conn_err = True
        if conn_err:
            # TODO: Schedule renewing of subclients
            pass

        return create_response_proto_to_dict(resp)

    async def hedge_bot(
        self,
        ticker: NDArray[str],
            spot_date: NDArray[np.datetime64],
            bot_id: NDArray[str],
            investment_amount: NDArray[np.float32],
            price: NDArray[np.float32],
            margin: NDArray[np.float16],
            fraction: NDArray[bool],
            last_share_num: NDArray[np.float32],
            total_bot_share_num: NDArray[np.float32],
            expire_date: NDArray[np.datetime64],
            price_level_1: NDArray[np.float32],
            price_level_2: NDArray[np.float32],
            r: Optional[np.float32] = None,
            q: Optional[np.float32] = None,
        ) -> Dict[str, NDArray]:    
        """
        Hedge a single bot.
        *Note: Actually just wraps the batch function (hedge_bots).

        Args:
            ticker: The ticker of the underlying asset.
            spot_date: Bot start date.
            bot_id: Composite id of bot type, option type, and holding period.
            investment_amount: Initial investment amount.
            price: Current price of stock.
            margin: Margin ratio (e.g. 1 = no margin).
            fraction: Whether fractional shares are allowed.
            last_share_num: Number of shares currently held.
            total_bot_share_num: Initial investment amount / price at creation.
            expire_date: Bot end date, i.e. holding period end.
            price_level_1: Lower price level.
            price_level_2: Upper price level.
            r: Interest rates.
            q: Dividend yields.

        Returns:
            Dict[str, NDArray]: A dictionary of bot properties.
        """
        inputs = locals().copy()
        inputs.pop('self')
        inputs = {k: np.array([v]) for k, v in inputs.items() if v is not None}
        resp = await self.hedge_bots(**inputs)
        return {k: v[0] for k, v in resp.items() if v is not None}

    async def hedge_bots(
            self,
            ticker: NDArray[str],
            spot_date: NDArray[np.datetime64],
            bot_id: NDArray[str],
            investment_amount: NDArray[np.float32],
            price: NDArray[np.float32],
            margin: NDArray[np.float16],
            fraction: NDArray[bool],
            last_share_num: NDArray[np.float32],
            total_bot_share_num: NDArray[np.float32],
            expire_date: NDArray[np.datetime64],
            price_level_1: NDArray[np.float32],
            price_level_2: NDArray[np.float32],
            r: Optional[np.float32] = None,
            q: Optional[np.float32] = None,
        ) -> Dict[str, NDArray[Any]]:
        """
        Hedges a batch of bots from a dictionary of inputs.
        The inputs must be arrays. In future we want to support generators
        but this involves some planning with @Clair.

        Args:
            ticker: The ticker of the underlying asset.
            spot_date: Bot start date.
            bot_id: Composite id of bot type, option type, and holding period.
            investment_amount: Initial investment amount.
            price: Current price of stock.
            margin: Margin ratio (e.g. 1 = no margin).
            fraction: Whether fractional shares are allowed.
            last_share_num: Number of shares currently held.
            total_bot_share_num: Initial investment amount / price at creation.
            expire_date: Bot end date, i.e. holding period end.
            price_level_1: Lower price level.
            price_level_2: Upper price level.
            r: Interest rates.
            q: Dividend yields.

        Returns:
            Dict[str, NDArray]: A dictionary of bot properties.
        """
        inputs = locals().copy()
        inputs.pop('self')
        inputs = {k: array_to_bytes(v) for k, v in inputs.items() \
            if v is not None}
        assert len(inputs['ticker']) <= self.max_batch_size, \
            f"Max batch size ({self.max_batch_size}) exceeded."
        
        conn_err = False
        for _ in range(self.max_retries):
            try:
                resp = await next(self._pool_itr)["stub"].HedgeBots(
                    BatchHedgeRequest(**inputs))
            except ConnectionRefusedError:
                print('DROID connection error. Retrying...')
                self._remove_dead_subclients()
                # TODO: Schedule renewal of subclients
                resp = await next(self._pool_itr)["stub"].HedgeBots(
                    BatchHedgeRequest(**inputs))
        if conn_err:
            # TODO: Schedule renewal of subclients
            pass

        return hedge_response_proto_to_dict(resp)
    
    async def create_bots_from_dataframe(
            self,
            inputs: pd.DataFrame,
        ) -> pd.DataFrame:
        """
        Creates a batch of bots from a dataframe containing inputs.

        Args:
            inputs: Should document the schema somewhere..
        """
        # Convert to dict of numpy arrays
        inputs = inputs.to_dict(orient='list')
        assert len(inputs['ticker']) <= self.max_batch_size, \
            f"Max batch size ({self.max_batch_size}) exceeded."
        spot_dates = pd.to_datetime(inputs["spot_date"]).date.astype(str)
        del inputs["spot_date"] # Because this breaks below dict comprehension
        inputs = {k: array_to_bytes(np.array(v)) \
            for k, v in inputs.items() \
            if v is not None}
        inputs["spot_date"] = array_to_bytes(spot_dates)

        # Call DROID
        # TODO: Use self.create_bots() instead, reduce code duplication
        conn_err = False
        for _ in range(self.max_retries):
            try:
                resp = await next(self._pool_itr)["stub"].CreateBots(
                    BatchCreateRequest(**inputs))
                break
            # TODO: better error handling here (e.g. for TimeoutError)
            except ConnectionRefusedError:
                print('DROID connection error. Retrying...')
                self._remove_dead_subclients()
                conn_err = True
        if conn_err:
            self.renew_pool()
            # TODO: Schedule renewing of subclients
            pass

        resp = create_response_proto_to_dict(resp)
        return pd.DataFrame.from_dict(resp)

    async def hedge_bots_from_dataframe(
            self,
            inputs: pd.DataFrame,
        ) -> pd.DataFrame:
        """
        Hedges a batch of bots from a dataframe containing inputs.

        Args:
            inputs: Should document the schema somewhere..
        """
        # Convert to dict of numpy arrays
        # TODO: Use self.create_bots() instead, reduce code duplication
        inputs = inputs.to_dict(orient='list')
        assert len(inputs['ticker']) <= self.max_batch_size, \
            f"Max batch size ({self.max_batch_size}) exceeded."
        spot_dates = pd.to_datetime(inputs["spot_date"]).date.astype(str)
        expire_dates = pd.to_datetime(inputs["expire_date"]).date.astype(str)
        del inputs["spot_date"] # Because these break below dict comprehension
        del inputs["expire_date"]
        
        inputs = {k: array_to_bytes(np.array(v)) \
            for k, v in inputs.items() \
            if v is not None}
        inputs["spot_date"] = array_to_bytes(spot_dates)
        inputs["expire_date"] = array_to_bytes(expire_dates)

        conn_err = False
        for _ in range(self.max_retries):
            try:
                resp = await next(self._pool_itr)["stub"].HedgeBots(
                    BatchHedgeRequest(**inputs))
                break
            except ConnectionRefusedError:
                print('DROID connection error. Retrying...')
                self._remove_dead_subclients()
                conn_err = True
            except TimeoutError:
                conn_err = True
        if conn_err:
            self.renew_pool()
            # TODO: Schedule renewing of subclients
            pass

        resp = hedge_response_proto_to_dict(resp)
        return pd.DataFrame.from_dict(resp)
