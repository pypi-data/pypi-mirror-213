from typing import Dict, NewType, Type, Union


long = NewType("long", int)

DType = Type[Union[bool, int, float, long]]


class RegSpec:
    def __init__(self, dtype: DType, rw: str, addr: int, multiplier: int = 1) -> None:
        assert dtype in [bool, int, float, long]
        assert rw in ["r", "w", "rw", "wr"]
        self.dtype = dtype
        self.rw = rw
        self.addr = addr
        self.multiplier = multiplier


# fmt: off
REGMAP: Dict[str, RegSpec] = {
    'output':         RegSpec(bool,  'rw', 0x0001       ),
    'protection':     RegSpec(int,   'r',  0x0002       ),
    # HM305P has: "305"
    'model':          RegSpec(int,   'r',  0x0003       ),
    # HM305P has: "19280" -> 4B50h -> "KP" or "PK", depending on byte order ...
    #             subtract 3 from each char would give "HM" ...
    'class':          RegSpec(int,   'r',  0x0004       ),
    'decimals':       RegSpec(int,   'r',  0x0005       ),
    'voltage':        RegSpec(float, 'r',  0x0010       ),
    'current':        RegSpec(float, 'r',  0x0011, 10   ),
    'power':          RegSpec(long,  'r',  0x0012, 1000 ),
    'powercal':       RegSpec(long,  'r',  0x0014, 1000 ),
    'ovp':            RegSpec(float, 'rw', 0x0020       ),
    'ocp':            RegSpec(float, 'rw', 0x0021, 10   ),
    'opp':            RegSpec(long,  'rw', 0x0022, 1000 ),
    'voltage:set':    RegSpec(float, 'rw', 0x0030       ),
    'current:set':    RegSpec(float, 'rw', 0x0031, 10   ),
    'timespan':       RegSpec(int,   'rw', 0x0032,      ),
    'm1:voltage':     RegSpec(float, 'rw', 0x1000,      ),
    'm1:current':     RegSpec(float, 'rw', 0x1001, 10   ),
    'm1:time':        RegSpec(int,   'rw', 0x1002,      ),
    'm1:enable':      RegSpec(bool,  'rw', 0x1003,      ),
    'm2:voltage':     RegSpec(float, 'rw', 0x1010,      ),
    'm2:current':     RegSpec(float, 'rw', 0x1011, 10   ),
    'm2:time':        RegSpec(int,   'rw', 0x1012,      ),
    'm2:enable':      RegSpec(bool,  'rw', 0x1013,      ),
    'm3:voltage':     RegSpec(float, 'rw', 0x1020,      ),
    'm3:current':     RegSpec(float, 'rw', 0x1021, 10   ),
    'm3:time':        RegSpec(int,   'rw', 0x1022,      ),
    'm3:enable':      RegSpec(bool,  'rw', 0x1023,      ),
    'm4:voltage':     RegSpec(float, 'rw', 0x1030,      ),
    'm4:current':     RegSpec(float, 'rw', 0x1031, 10   ),
    'm4:time':        RegSpec(int,   'rw', 0x1032,      ),
    'm4:enable':      RegSpec(bool,  'rw', 0x1033,      ),
    'm5:voltage':     RegSpec(float, 'rw', 0x1040,      ),
    'm5:current':     RegSpec(float, 'rw', 0x1041, 10   ),
    'm5:time':        RegSpec(int,   'rw', 0x1042,      ),
    'm5:enable':      RegSpec(bool,  'rw', 0x1043,      ),
    'm6:voltage':     RegSpec(float, 'rw', 0x1050,      ),
    'm6:current':     RegSpec(float, 'rw', 0x1051, 10   ),
    'm6:time':        RegSpec(int,   'rw', 0x1052,      ),
    'm6:enable':      RegSpec(bool,  'rw', 0x1053,      ),
    # "beep" special menu function
    'beep':           RegSpec(bool,  'rw', 0x8804,      ),
    # power output on power up: (default was: 3)
    #     (special menu function "O.U.T.")
    #        0: "off"     (off)
    #        1: "on"      (on)
    #        2: "on off"  (restore)
    #      >=3: "out"     (unclear what is different from "2")
    'powerstat':      RegSpec(int,   'rw', 0x8801,      ),
    # "0x8802": defaultshow: reads as "0", seems to be read-only
    #     'defaultshow':    RegSpec(int,   'r',  0x8802,      ),
    # "0x8803": scp: short circuit protection? reads as "0", seems to be read-only
    #     'scp':            RegSpec(int,   'r',  0x8803,      ),
    # "0x8804": 6 ?
    # "0x8888": 3 ?
    # "0xCCCC": sdtime: ? reads as "0", seems to be read-only
    #    'sdtime':          RegSpec(int,   'rw', 0xcccc,      ),
    # "0x9999": "addr" special menu function
    'addr':           RegSpec(int,   'rw', 0x9999,      ),

}
# fmt: on
