"""  :mod:`telliot.queries.query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import ClassVar
from typing import List
from typing import Union

from pydantic import BaseModel
from telliot.queries.value_type import ValueType
from web3 import Web3

CoerceToTipId = Union[bytearray, bytes, int, str]


def to_tip_id(value: CoerceToTipId) -> bytes:
    """Coerce input type to tip id in Bytes32 format"""
    if isinstance(value, bytearray):
        value = bytes(value)

    if isinstance(value, bytes):
        bytes_value = value

    elif isinstance(value, str):
        value = value.lower()
        if value.startswith("0x"):
            value = value[2:]
        bytes_value = bytes.fromhex(value)

    elif isinstance(value, int):
        bytes_value = value.to_bytes(32, "big", signed=False)

    else:
        raise TypeError("Cannot convert {} to tip id".format(value))

    if len(bytes_value) != 32:
        raise ValueError("Tip ID must have 32 bytes")

    return bytes_value


class OracleQuery(BaseModel):
    """Oracle Query

    An :class:`OracleQuery` specifies how to pose a question to the
    Tellor Oracle and how to format/interpret the response.

    The :class:`OracleQuery` class serves
    as the base class for all Queries, and implements default behaviors.
    Each subclass corresponds to a unique Query Type supported
    by the TellorX network.

    The base class provides:

    - Query :attr:`inputs` that enable customization of
      the query type.  Each input corresponds to a class attribute.

    - Calculation of the contents of the ``data`` field to include with the
      ``TellorX.Oracle.addTip()`` contract call.

    - Calculation of the ``id`` field field to include with the
      ``TellorX.Oracle.addTip()`` and ``TellorX.Oracle.submitValue()``
      contract calls.

    """

    #: A list of input names used to customize the query.  This should
    #: be overridden by all subclass Query Types.
    inputs: ClassVar[List[str]]

    @property
    def value_type(self) -> ValueType:
        """Returns the value type the current Query configuration

        The value type defines required data type/structure of the
        ``value`` submitted to the contract through
        ``TellorX.Oracle.submitValue()``

        This method must be overridden by subclasses
        """
        pass

    @property
    def tip_data(self) -> bytes:
        """Returns the ``data`` field for use in ``TellorX.Oracle.addTip()``
        contract call.

        By convention, the tip data includes the unique ID, a query string
        and the expected value type in the following format:

        <:attr:`query`> ? <:attr:`value_type`>

        This method may be overridden by subclasses
        """

        # rtype_str = dict2argstr(self.value_type.dict())

        qry = repr(self)
        rsp = repr(self.value_type)

        q = f"{qry}?{rsp}"

        return q.encode("utf-8")

    @property
    def tip_id(self) -> bytes:
        """Returns the tip ``id`` for use with the
        ``TellorX.Oracle.addTip()`` and ``TellorX.Oracle.submitValue()``
        contract calls.
        """
        return bytes(Web3.keccak(self.tip_data))

    # @property
    # def query(self) -> str:
    #     """Returns the default query
    #
    #     By default, a query will create a customized query string
    #     using currently configured values of each input.
    #     """
    #
    #     params = self.get_params()
    #
    #     param_str = dict2argstr(params)
    #
    #     q = f"{self.__class__.__name__}({param_str})"
    #
    #     return q

    # def get_params(self) -> Dict[str, Any]:
    #     """Returns a dictionary of all query input values"""
    #     result = {}
    #     for p in self.inputs:
    #         result[p] = self.__getattribute__(p)
    #
    #     return result
