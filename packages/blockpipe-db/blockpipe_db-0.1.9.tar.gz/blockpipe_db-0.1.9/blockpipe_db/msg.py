import msgpack
from hexbytes import HexBytes
from dataclasses import dataclass


@dataclass
class GetLogs1Request:
    __slot__ = ['network', 'address', 'topic0',
                'from_block_number', 'from_log_index', 'limit']

    network: str
    address: HexBytes
    topic0: HexBytes
    from_block_number: int
    from_log_index: int
    limit: int

    def to_bytes(self) -> bytes:
        return msgpack.packb({
            'GetLogs1': [self.network, self.address, self.topic0,
                         self.from_block_number, self.from_log_index, self.limit],
        })  # type: ignore
