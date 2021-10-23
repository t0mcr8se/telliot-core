"""  Oracle Query Module

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import Any

from telliot.types.value_type import ValueType
from telliot.utils.serializable import SerializableModel
from web3 import Web3


class OracleQuery(SerializableModel):
    """Oracle Query

    An OracleQuery specifies how to pose a question to the
    Tellor Oracle and how to format/interpret the response.

    The OracleQuery class serves
    as the base class for all Queries, and implements default behaviors.
    Each subclass corresponds to a unique Query Type supported
    by the TellorX network.

    All public attributes of an OracleQuery represent an input that can
    be used to customize the query.

    The base class provides:

    - Calculation of the contents of the ``data`` field to include with the
      ``TellorX.Oracle.tipQuery()`` contract call.

    - Calculation of the ``id`` field field to include with the
      ``TellorX.Oracle.tipQuery()`` and ``TellorX.Oracle.submitValue()``
      contract calls.

    WORK IN PROGRESS - Descriptor formats still under development

    """

    @property
    def descriptor(self) -> str:
        """Get the query descriptor string.
        The Query descriptor is a unique string representation of the query.
        The descriptor is required for users to specify the query to TellorX
        through the ``TellorX.Oracle.tipQuery()`` contract call.

        By convention, the descriptor includes the text representation
        of the OracleQuery and the :class:`ValueType` of its response.

            `query` ? `value_type`
        """
        return f"{self.json()}?{self.value_type.json()}"

    @property
    def value_type(self) -> ValueType:
        """Returns the ValueType expected by the current Query configuration

        The value type defines required data type/structure of the
        ``value`` submitted to the contract through
        ``TellorX.Oracle.submitValue()``

        This method must be overridden by subclasses
        """
        pass

    @property
    def query_data(self) -> bytes:
        """Returns the ``data`` field for use in ``TellorX.Oracle.tipQuery()``
        contract call.

        """
        return self.descriptor.encode("utf-8")

    @property
    def query_id(self) -> bytes:
        """Returns the query ``id`` for use with the
        ``TellorX.Oracle.tipQuery()`` and ``TellorX.Oracle.submitValue()``
        contract calls.
        """
        return bytes(Web3.keccak(self.query_data))

    def json(self, **kwargs: Any) -> str:
        """Convert to compact JSON format used in query descriptor"""

        return super().json(**kwargs, separators=(",", ":"))