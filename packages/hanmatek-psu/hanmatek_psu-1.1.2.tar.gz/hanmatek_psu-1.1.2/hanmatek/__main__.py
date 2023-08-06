import argparse
from pathlib import Path
from typing import Generator, Optional

from . import DeviceNotFoundError
from .HM3xxP import HM3xxP
from .HM3xxP_regmap import REGMAP


_UDEV_SYMLINK = "/dev/ttyHM3xxP"


def serial_interfaces() -> Generator[str, None, None]:
    by_id = Path("/dev/serial/by-id").glob("*")
    for link in by_id:
        yield str(link.resolve())


def _find_device(device: Optional[str], slave_addr: int) -> HM3xxP:

    if device:
        return HM3xxP(device, slave_addr=slave_addr)

    if Path(_UDEV_SYMLINK).exists():
        return HM3xxP(_UDEV_SYMLINK, slave_addr=slave_addr)

    devices = HM3xxP.discover(ports=serial_interfaces(), addresses=[slave_addr])

    if not devices:
        raise DeviceNotFoundError("no HM3xxP device could be discovered")

    if len(devices) > 1:
        raise DeviceNotFoundError(f"discovered multiple HM3xxP devices: {len(devices)}")

    return devices[0]


def main() -> bool:

    parser = argparse.ArgumentParser(prog="HM3xxP CLI")
    parser.add_argument(
        "cmd",
        type=str,
        nargs="?",
        help="The read or write command. See --list for the list of available commands.",
    )
    parser.add_argument("value", type=str, nargs="?", help="Write this value.")
    parser.add_argument(
        "-L",
        "--list",
        action="store_true",
        help="List available commands (cmd) and their data types.",
    )
    parser.add_argument(
        "-D",
        "--device",
        type=str,
        nargs="?",
        help="The serial interface device to use. If omitted, try to use /dev/HM3xxP (symlinked "
        "by the contained udev rule). If not found, auto-discovery is performed.",
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="search HM3xxP devices on all serial interfaces (see `ls -la /dev/serial/by-id`), "
        "using --slave-addr.",
    )
    parser.add_argument(
        "--scan",
        type=int,
        nargs="+",
        help="read the specified address range from the selected device. Address range is start "
        "address and optional length (default 256). Example: --scan 0 256",
    )
    parser.add_argument(
        "--slave-addr",
        metavar="ADDR",
        type=int,
        default=1,
        help="Modbus slave address of the device. Defaults to '1'. "
        "Can be changed using the 'addr' command or on the PSU special menu.",
    )
    args = parser.parse_args()

    if args.list:
        lencmd = max([len(cmd) for cmd in REGMAP])
        print(f"ADDR  {'CMD':{lencmd}}  R/W  TYPE")
        for cmd in REGMAP:
            reg = REGMAP[cmd]
            print(f"{reg.addr:04x}  {cmd:{lencmd}}  {reg.rw:3}  {reg.dtype.__name__}")
        return True

    if args.discover:
        devices = HM3xxP.discover(ports=serial_interfaces(), addresses=[args.slave_addr])
        lenport = max([len(dev.port) for dev in devices] + [len("DEVICE")])
        print(f"{'DEVICE':{lenport}}  ADDR  DEVICE")
        for dev in devices:
            print(f"{dev.port:{lenport}}  {dev.slave_addr:4}  {dev.info()}")
        return bool(devices)

    device = _find_device(args.device, args.slave_addr)

    if args.scan:
        start = args.scan[0]
        num = args.scan[1] if len(args.scan) > 1 else 256
        for i in range(num):
            try:
                addr = start + i
                value = device._read_register(addr=addr, dtype=int)
                print(f"0x{addr:04X}: {value}")
            except Exception as exc:
                print(f"0x{addr:04X}: {exc}")
        return True

    if not args.cmd:
        try:
            device_info = device.info()
            print(
                f"found HM3xxP device: {device_info} on {device.port} at "
                f"addr {device.slave_addr:03}"
            )
            print(f"    Output:        {'on' if device.read('output') else 'off'}")
            print(f"    Voltage (set): {device.read('voltage:set'):05.2f}")
            print(f"    Voltage:       {device.read('voltage'):05.2f}")
            print(f"    Current (set): {device.read('current:set'):05.3f}")
            print(f"    Current:       {device.read('current'):05.3f}")
            print(f"    Power:         {device.read('power'):05.3f}")
        except TimeoutError as exc:
            raise DeviceNotFoundError(
                f"Failed to get device info from {device.port} at addr {device.slave_addr}"
            ) from exc
        return True

    if not args.value:
        print(device.read(args.cmd))
    else:
        device.write(args.cmd, args.value)

    return True


if __name__ == "__main__":
    exit(int(not main()))
