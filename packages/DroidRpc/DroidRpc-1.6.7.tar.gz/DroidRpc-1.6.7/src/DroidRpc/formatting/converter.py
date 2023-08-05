# Contains functions that convert between different representations of data.
# We can convert protos to dict explicitly (without inferring) because we know
# the structure of the protos.

from io import BytesIO
import numpy as np
from typing import Dict, Union
from DroidRpc.droid_pb2 import (
    BatchCreateRequest,
    BatchCreateResponse,
    BatchHedgeRequest,
    BatchHedgeResponse,
)


def array_to_bytes(array: np.ndarray):
    """
    Converts a numpy array to a bytestream.
    """

    # If using default: certain value may not be ndarray. Convert first.
    if type(array) in [float, bool, str, int]:
        array = np.array(array)

    if array is None:
        return None

    if isinstance(array, np.ndarray):
        output = BytesIO()
        np.save(output, array, allow_pickle=False)
        return output.getvalue()
    else:
        raise TypeError(f"Array must be a numpy array, got {type(array)}")


def bytes_to_array(bytestream: BytesIO, dtype: Union[str, np.dtype]):
    """
    Converts a bytestream into a numpy array.
    """
    try:
        if bytestream == b'':  # Protobuf byte equivalent of "None"
            return None
        return np.load(BytesIO(bytestream), allow_pickle=False).astype(dtype)
    except Exception as e:
        raise type(e)(f"Error converting {bytestream} to array") from e


def create_request_proto_to_dict(req: BatchCreateRequest) -> Dict[str, bytes]:
    """
    Converts a create bots request into a dictionary.
    Note: Casting from bytes is done by the validator.
    """
    try:
        props = {
            "ticker": req.ticker,
            "spot_date": req.spot_date,
            "bot_id": req.bot_id,
            "investment_amount": req.investment_amount,
            "price": req.price,
            "margin": req.margin,
            "fraction": req.fraction,
            "multiplier_1": req.multiplier_1,
            "multiplier_2": req.multiplier_2,
            "currency": req.currency,
            "time_to_exp": req.time_to_exp,
            "option_type": req.option_type,
            "bot_type": req.bot_type,
            "atm_volatility_spot": req.atm_volatility_spot,
            "atm_volatility_one_year": req.atm_volatility_one_year,
            "atm_volatility_infinity": req.atm_volatility_infinity,
            "slope": req.slope,
            "slope_inf": req.slope_inf,
            "deriv": req.deriv,
            "deriv_inf": req.deriv_inf,
            "q": req.q,
            "r": req.r,
            "classic_vol": req.classic_vol
        }
        # Remove empty values
        props = {k: v for k, v in props.items() if v != b''}
        return props
    except AttributeError as e:
        raise ValueError("Input field(s) missing") from e
    except Exception as e:
        raise e


def hedge_request_proto_to_dict(req: BatchHedgeRequest) -> Dict[str, bytes]:
    """
    Converts a hedge bots request into a dictionary.
    Note: Casting from bytes is done by the validator.
    """
    try:
        props = {
            "ticker": req.ticker,
            "spot_date": req.spot_date,
            "bot_id": req.bot_id,
            "investment_amount": req.investment_amount,
            "price": req.price,
            "margin": req.margin,
            "fraction": req.fraction,
            "last_share_num": req.last_share_num,
            "total_bot_share_num": req.total_bot_share_num,
            "expire_date": req.expire_date,
            "price_level_1": req.price_level_1,
            "price_level_2": req.price_level_2,
            "currency": req.currency,
            "time_to_exp": req.time_to_exp,
            "option_type": req.option_type,
            "bot_type": req.bot_type,
            "atm_volatility_spot": req.atm_volatility_spot,
            "atm_volatility_one_year": req.atm_volatility_one_year,
            "atm_volatility_infinity": req.atm_volatility_infinity,
            "slope": req.slope,
            "slope_inf": req.slope_inf,
            "deriv": req.deriv,
            "deriv_inf": req.deriv_inf,
            "q": req.q,
            "r": req.r,
            "classic_vol": req.classic_vol
        }
        # Remove empty values
        props = {k: v for k, v in props.items() if v != b''}
        return props
    except AttributeError as e:
        raise ValueError("Input field(s) missing") from e
    except Exception as e:
        raise e


def create_response_proto_to_dict(res: BatchCreateResponse) -> Dict[str, bytes]:
    """
    Converts a BotBatchCreatorResponse into a dictionary.
    """
    f = bytes_to_array
    try:
        props = {
            "ticker": f(res.ticker, dtype=str),
            "spot_date": f(res.spot_date, dtype=np.datetime64),
            "bot_id": f(res.bot_id, dtype=str),
            "investment_amount": f(res.investment_amount, dtype=np.float32),
            "price": f(res.price, dtype=np.float32),
            "margin": f(res.margin, dtype=np.float16),
            "fraction": f(res.fraction, dtype=bool),
            "multiplier_1": f(res.multiplier_1, dtype=np.float16),
            "multiplier_2": f(res.multiplier_2, dtype=np.float16),
            "delta": f(res.delta, dtype=np.float32),
            "share_num": f(res.share_num, dtype=np.float32),
            "share_num_change": f(res.share_num_change, dtype=np.float32),
            "total_bot_share_num": f(res.total_bot_share_num, dtype=np.float32),
            "expire_date": f(res.expire_date, dtype=np.datetime64),
            "status": f(res.status, dtype=str),
            "price_level_1": f(res.price_level_1, dtype=np.float32),
            "price_level_2": f(res.price_level_2, dtype=np.float32),
            "max_loss_amount": f(res.max_loss_amount, dtype=np.float32),
            "max_loss_pct": f(res.max_loss_pct, dtype=np.float32),
            "max_loss_price": f(res.max_loss_price, dtype=np.float32),
            "target_profit_amount": f(res.target_profit_amount, dtype=np.float32),
            "target_profit_pct": f(res.target_profit_pct, dtype=np.float32),
            "target_profit_price": f(res.target_profit_price, dtype=np.float32),
            "classic_vol": f(res.classic_vol, dtype=np.float32),
            "vol_spot": f(res.vol_spot, dtype=np.float32),
            "vol_price_1": f(res.vol_price_1, dtype=np.float32),
            "vol_price_2": f(res.vol_price_2, dtype=np.float32),
            "q": f(res.q, dtype=np.float32),
            "r": f(res.r, dtype=np.float32),
            "option_price": f(res.option_price, dtype=np.float32),
        }
        return props
    except AttributeError as e:
        raise ValueError("Input field(s) missing") from e
    except Exception as e:
        raise e


def hedge_response_proto_to_dict(res: BatchHedgeResponse) -> Dict[str, bytes]:
    """
    Converts a BotBatchHedgerResponse into a dictionary.
    """
    f = bytes_to_array
    try:
        props = {
            "ticker": f(res.ticker, dtype=str),
            "spot_date": f(res.spot_date, dtype=np.datetime64),
            "bot_id": f(res.bot_id, dtype=str),
            "investment_amount": f(res.investment_amount, dtype=np.float32),
            "price": f(res.price, dtype=np.float32),
            "delta": f(res.delta, dtype=np.float32),
            "share_num": f(res.share_num, dtype=np.float32),
            "share_num_change": f(res.share_num_change, dtype=np.float32),
            "status": f(res.status, dtype=str),
            "vol_spot": f(res.vol_spot, dtype=np.float32),
            "vol_price_1": f(res.vol_price_1, dtype=np.float32),
            "vol_price_2": f(res.vol_price_2, dtype=np.float32),
            "q": f(res.q, dtype=np.float32),
            "r": f(res.r, dtype=np.float32),
            "option_price": f(res.option_price, dtype=np.float32),
        }
        return props
    except AttributeError as e:
        raise ValueError("Input field(s) missing") from e
    except Exception as e:
        raise e


def create_request_dict_to_proto(req: Dict[str, bytes]) -> BatchCreateRequest:
    """
    Converts a dictionary of `NDArray` into a BotBatchCreatorRequest.
    """
    f = array_to_bytes
    try:
        props = {
            "ticker": f(req.get("ticker", None)),
            "spot_date": f(req.get("spot_date", None)),
            "bot_id": f(req.get("bot_id", None)),
            "investment_amount": f(req.get("investment_amount", None)),
            "price": f(req.get("price", None)),
            "margin": f(req.get("margin", None)),
            "fraction": f(req.get("fraction", None)),
            "multiplier_1": f(req.get("multiplier_1", None)),
            "multiplier_2": f(req.get("multiplier_2", None)),
            "currency": f(req.get("currency", None)),
            "time_to_exp": f(req.get("time_to_exp", None)),
            "option_type": f(req.get("option_type", None)),
            "bot_type": f(req.get("bot_type", None)),
            "atm_volatility_spot": f(req.get("atm_volatility_spot", None)),
            "atm_volatility_one_year": f(req.get("atm_volatility_one_year", None)),
            "atm_volatility_infinity": f(req.get("atm_volatility_infinity", None)),
            "slope": f(req.get("slope", None)),
            "slope_inf": f(req.get("slope_inf", None)),
            "deriv": f(req.get("deriv", None)),
            "deriv_inf": f(req.get("deriv_inf", None)),
            "q": f(req.get("q", None)),
            "r": f(req.get("r", None)),
        }
        props = {k: v for k, v in props.items() if v is not None}
        return BatchCreateRequest(**props)
    except KeyError as e:
        raise ValueError("Missing field") from e


def hedge_request_dict_to_proto(req: Dict[str, bytes]) -> BatchHedgeRequest:
    """
    Converts a dictionary of `NDArray` into a BotBatchHedgerRequest.
    """
    f = array_to_bytes
    try:
        props = {
            "ticker": f(req.get("ticker", None)),
            "spot_date": f(req.get("spot_date", None)),
            "bot_id": f(req.get("bot_id", None)),
            "investment_amount": f(req.get("investment_amount", None)),
            "price": f(req.get("price", None)),
            "margin": f(req.get("margin", None)),
            "fraction": f(req.get("fraction", None)),
            "last_share_num": f(req.get("last_share_num", None)),
            "total_bot_share_num": f(req.get("total_bot_share_num", None)),
            "expire_date": f(req.get("expire_date", None)),
            "price_level_1": f(req.get("price_level_1", None)),
            "price_level_2": f(req.get("price_level_2", None)),
            "currency": f(req.get("currency", None)),
            "time_to_exp": f(req.get("time_to_exp", None)),
            "option_type": f(req.get("option_type", None)),
            "bot_type": f(req.get("bot_type", None)),
            "atm_volatility_spot": f(req.get("atm_volatility_spot", None)),
            "atm_volatility_one_year": f(req.get("atm_volatility_one_year", None)),
            "atm_volatility_infinity": f(req.get("atm_volatility_infinity", None)),
            "slope": f(req.get("slope", None)),
            "slope_inf": f(req.get("slope_inf", None)),
            "deriv": f(req.get("deriv", None)),
            "deriv_inf": f(req.get("deriv_inf", None)),
            "q": f(req.get("q", None)),
            "r": f(req.get("r", None)),
        }
        props = {k: v for k, v in props.items() if v is not None}
        return BatchHedgeRequest(**props)
    except KeyError as e:
        raise ValueError("Missing field") from e


def input_dict_to_array(inputs: Dict[str, Union[str, float, list]],
                        to_list: bool = True) \
        -> Dict[str, np.ndarray]:
    """
    [TO BE DEPRECATED]
    Converts values of an input dictionary from `typing.Any` to `NDArray` with the 
    correct dtype (key name determines the dtype via dict lookup).

    Specifically, used to create arguments to be passed to validator dataclasses 
    when creating props during testing, because this lets us create dicts with 
    scalar values when writing test cases. Basically lets us be lazy.

    Args:
        inputs: Dictionary of inputs
        to_list: Whether to convert values of the dict to np.NDArray. If False, will convert to scalar.

    Returns:
        Dictionary of inputs with values converted to np.NDArray and correct dtype.
    """
    from src.validator import input_dtypes
    return {k: np.array([v] if to_list else v).astype(input_dtypes[k])
            for k, v in inputs.items()}


def input_array_to_byte(inputs: Dict[str, np.ndarray]) -> Dict[str, BytesIO]:
    """
    Converts values of an input dictionary of `NDArrays` to `bytes`.
    Specifically, used to create arguments to be passed to validator dataclasses 
    when creating props during testing.

    Args:
        inputs: Dictionary of inputs

    Returns:
        Dictionary of inputs with values converted to bytes.
    """
    return {k: array_to_bytes(v) for k, v in inputs.items()}
