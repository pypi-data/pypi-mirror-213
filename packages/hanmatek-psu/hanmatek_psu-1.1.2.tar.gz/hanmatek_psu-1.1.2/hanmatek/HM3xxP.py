import time
from typing import Any, Callable, Final, Iterable, List, Set, TypeVar, Union

import minimalmodbus

from hanmatek.HM3xxP_regmap import REGMAP, RegSpec, long, DType


T = TypeVar("T")


class HM3xxP:

    _supported_models: Final[Set[int]] = {305, 3010}

    def __init__(self, port: str, slave_addr: int = 1):
        self.port = port
        self.slave_addr = slave_addr
        self.instrument = minimalmodbus.Instrument(
            port=port, slaveaddress=slave_addr, mode=minimalmodbus.MODE_RTU
        )
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.1

    def _retry(self, func: Callable[[], T], retries: int = 10, delay: float = 0.01) -> T:
        last_exc = None
        for _ in range(retries):
            try:
                return func()
            except minimalmodbus.ModbusException as exc:
                last_exc = exc
            time.sleep(delay)
        raise TimeoutError(f"no response from device after {retries} retries") from last_exc

    @classmethod
    def _boolish(cls, value: Any) -> bool:
        if str(value).lower() in ["1", "1.0", "on", "true", "yes"]:
            return True
        if str(value).lower() in ["0", "0.0", "off", "false", "no"]:
            return False
        raise ValueError(f"cannot convert {value} to bool")

    @classmethod
    def _convert_type(
        cls, value: Union[bool, int, float, str], reg: RegSpec, multiplier: float
    ) -> Union[bool, int, float]:
        if reg.dtype == bool:
            return cls._boolish(value)
        if reg.dtype == int:
            return int(float(value) * multiplier)
        # float or long
        return float(value) * multiplier

    def read(self, register: str) -> Union[bool, int, float]:

        if register not in REGMAP:
            raise ValueError(f"unknown register: {register}")

        reg = REGMAP[register]

        if "r" not in str(reg.rw):
            raise ValueError(f'not a "read" register: {register}')

        value = self._read_register(reg.addr, reg.dtype)

        return self._convert_type(value, reg, 1 / reg.multiplier)

    def _read_register(self, addr: int, dtype: DType) -> Union[int, float]:
        if dtype in [bool, int]:
            f_read = lambda: self.instrument.read_register(addr, 0)  # noqa: E731
        elif dtype == float:
            f_read = lambda: self.instrument.read_register(addr, 2)  # noqa: E731
        elif dtype == long:
            f_read = lambda: self.instrument.read_long(addr)  # noqa: E731
        else:
            assert False, f"internal error - unsupported data type: {dtype}"

        value: Union[int, float] = self._retry(func=f_read)

        return value

    def write(self, register: str, value: Union[bool, int, float, str]) -> None:
        if register not in REGMAP:
            raise ValueError(f"unknown register: {register}")

        reg = REGMAP[register]

        if "w" not in reg.rw:
            raise ValueError(f'not a "write" register: {register}')

        write_value = self._convert_type(value, reg, reg.multiplier)

        self._write_register(reg.addr, write_value, reg.dtype)

    def _write_register(self, addr: int, value: Union[bool, int, float], dtype: DType) -> None:
        if dtype == float:
            f_read = lambda: self.instrument.write_register(addr, value, 2)  # noqa: E731
        elif dtype == int:
            f_read = lambda: self.instrument.write_register(addr, value, 0)  # noqa: E731
        elif dtype == bool:
            f_read = lambda: self.instrument.write_register(addr, int(value), 0)  # noqa: E731
        elif dtype == long:
            f_read = lambda: self.instrument.write_long(addr, int(value))  # noqa: E731
        else:
            assert False, f"internal error - unsupported data type: {dtype}"
        self._retry(func=f_read)

    def info(self) -> str:
        return int(self.read("class")).to_bytes(2, byteorder="big").decode() + str(
            self.read("model")
        )

    @classmethod
    def discover(cls, ports: Iterable[str], addresses: Iterable[int] = [1]) -> List["HM3xxP"]:
        devices = []
        for port in ports:
            for addr in addresses:
                device = HM3xxP(port=port, slave_addr=addr)
                try:
                    if (
                        device.read("model") in cls._supported_models
                        and device.read("class") == 19280
                    ):
                        devices.append(device)
                except TimeoutError:
                    pass
        return devices
