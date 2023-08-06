
# Table of Contents



import pathlib
import re

import rich.console

from rich.table import Table

from p2g import lib

INTO<sub>ARRAY</sub> = 0
INDENT = "    "
INTO<sub>ATTR</sub> = 0
INDENT = "    "

INTO<sub>GBL</sub> = 1
INDENT = ""

def def<sub>prefix</sub>(key):
    if INTO<sub>ARRAY</sub>:  # no cover
        return f'dst["{key}"]'
    if INTO<sub>ATTR</sub>:  # no cover
        return f"dst.{key}"

return f"{key}"

MAKE<sub>PFX</sub> = "p2g."

class NAXES:
    def \_<sub>init</sub>\_<sub>(self)</sub>:
        pass

def \_<sub>str</sub>\_<sub>(self)</sub>:
    return "NAXES"

class MacroVar:
    def \_<sub>init</sub>\_<sub>(self, \*, key, addr, alias=None, size=None, name="", typ="")</sub>:
        self.typ = typ
        self.key = key
        self.addr = addr

self.name = name
self.<sub>alias</sub> = alias
self.size = size
suffix = ""
self.last = None
if isinstance(self.size, NAXES):
    self.last = NAXES
    suffix = "…"
else:
    self.last = self.addr + self.size - 1
    if self.last != self.addr:
        suffix = f" … #{self.last:5}"
self.range<sub>as</sub><sub>text</sub> = f"#{self.addr:5}{suffix}"

@property
def alias(self):
    if self.<sub>alias</sub>:
        return self.<sub>alias</sub>
    return "no alias"

def for<sub>regen</sub>(self):
    funcname = self.\_<sub>class</sub>\_\_.\_<sub>qualname</sub>\_\_
    res = [str(self.addr)]
    if self.size is not None:
        res.append(f"size={self.size}")
    restxt = ", ".join(res)
    return f"{def<sub>prefix</sub>(self.name)} = {funcname}({restxt})"

def for<sub>txt</sub>(self):
    return (
        self.range<sub>as</sub><sub>text</sub>,
        str(self.size),
        self.key,
        self.typ,
        self.name,
    )

def for<sub>org</sub>(self):
    return f"| `{self.name}` | `{self.size}` | `{self.range_as_text}` |\n"

def for<sub>py</sub><sub>out</sub>(self):
    return f"# {self.addr} .. {self.last} {self.name} .."

def \_<sub>lt</sub>\_<sub>(self, other)</sub>:
    return self.addr < other.addr

class Gen(MacroVar):
    def \_<sub>init</sub>\_<sub>(
        self,
        \*,
        exp<sub>name</sub>,
        idc,
        addr,
        size=None,
        typ,
    )</sub>:
        self.exp<sub>name</sub> = exp<sub>name</sub>

super().\_<sub>init</sub>\_<sub>(
    key=idc,
    addr=addr,
    size=size,
    typ=typ,
)</sub>

def for<sub>py</sub><sub>out</sub>(self):
    rs = ""

sstr = ""
if self.size is not None and self.size != 1:
    sstr = f"[{self.size}]"
return f"{def<sub>prefix</sub>(self.name)} = {MAKE<sub>PFX</sub>}Fixed{sstr}({rs}addr={self.addr})"

def one(addr, typ="Float"):
    return Gen(
        exp<sub>name</sub>="Fixed",
        idc="v" + typ[0],
        addr=addr,
        size=1,
        typ=typ,
    )

def ione(addr):
    return one(addr, typ="Int")

class Alias(MacroVar):
    def \_<sub>init</sub>\_<sub>(self, src)</sub>:
        super().\_<sub>init</sub>\_<sub>(key="A", addr=src.addr, size=src.size, alias=src)</sub>

def for<sub>regen</sub>(self):
    return f"{def<sub>prefix</sub>(self.name.ljust(20))} = alias({def<sub>prefix</sub>}{self.alias.name})"

def for<sub>py</sub><sub>out</sub>(self):
    return f"{def<sub>prefix</sub>(self.name)} = {MAKE<sub>PFX</sub>}alias({def<sub>prefix</sub>(self.alias.name)})"

def for<sub>txt</sub>(self):
    return (
        self.range<sub>as</sub><sub>text</sub>,
        str(self.size),
        self.key,
        self.typ,
        " also " + self.name,
    )

def fixed(addr, size, typ="Float"):
    return Gen(
        exp<sub>name</sub>="Fixed",
        idc="V",
        addr=addr,
        size=size,
        typ=typ,
    )

class Gap(MacroVar):
    C = 0

def <span class="underline">\_init\_<sub>(self, addr, size=None)</sub>:
    super().\_<sub>init</sub>\_\_(key="</span>", addr=addr, size=size)
    self.name = "-"

def for<sub>regen</sub>(self):
    self.name = f"gap{Gap.C:02}"
    Gap.C += 1
    return super().for<sub>regen</sub>()

def cwcpos(addr):
    return Gen(exp<sub>name</sub>="CWCPos", idc="m", addr=addr, size=NAXES(), typ="Float")

def machinepos(addr):
    return Gen(exp<sub>name</sub>="MachinePos", idc="m", addr=addr, size=NAXES(), typ="Float")

def workoffsettable(addr):
    return Gen(exp<sub>name</sub>="WorkOffsetTable", idc="W", addr=addr, typ="Float", size=NAXES())

def tooltable(addr, size, typ="Float"):
    return Gen(exp<sub>name</sub>="ToolTable", idc="T", addr=addr, size=size, typ=typ)

class PalletTable(MacroVar):
    def \_<sub>init</sub>\_<sub>(self, addr, size)</sub>:
        super().\_<sub>init</sub>\_<sub>(key="L", addr=addr, size=size, typ="Int")</sub>

class Names:
    interesting: list[MacroVar]

def \_<sub>init</sub>\_<sub>(self)</sub>:
    object.\_<sub>setattr</sub>\_<sub>(self, "interesting", [])</sub>

def py<sub>write</sub><sub>to</sub>(self, out):
    for v in self.interesting:
        out.write(INDENT + v.for<sub>py</sub><sub>out</sub>() + "\n")

def \_<sub>setattr</sub>\_<sub>(self, key, value)</sub>:
    if key[0].isupper():
        value.name = key
        object.\_<sub>setattr</sub>\_<sub>(self, key, value)</sub>

self.interesting.append(value)

class HaasNames(Names):
    title = "HAAS"

def \_<sub>init</sub>\_<sub>(self)</sub>:
    super().\_<sub>init</sub>\_<sub>()</sub>

self.NULL = one(0)
self.MACRO<sub>ARGUMENTS</sub> = fixed(1, size=33)
self.gap01 = Gap(34, size=66)
self.GP<sub>SAVED1</sub> = fixed(100, size=100)
self.gap02 = Gap(200, size=300)
self.GP<sub>SAVED2</sub> = fixed(500, size=50)

self.PROBE<sub>CALIBRATION1</sub> = fixed(550, size=6)
self.PROBE<sub>R</sub> = fixed(556, size=3)
self.PROBE<sub>CALIBRATION2</sub> = fixed(559, size=22)

self.GP<sub>SAVED3</sub> = fixed(581, size=119)
self.gap03 = Gap(700, size=100)
self.GP<sub>SAVED4</sub> = fixed(800, size=200)
self.INPUTS = fixed(1000, size=64)
self.MAX<sub>LOADS</sub><sub>XYZAB</sub> = fixed(1064, size=5)
self.gap04 = Gap(1069, size=11)
self.RAW<sub>ANALOG</sub> = fixed(1080, size=10)
self.FILTERED<sub>ANALOG</sub> = fixed(1090, size=8)
self.SPINDLE<sub>LOAD</sub> = one(1098)
self.gap05 = Gap(1099, size=165)
self.MAX<sub>LOADS</sub><sub>CTUVW</sub> = fixed(1264, size=5)
self.gap06 = Gap(1269, size=332)
self.TOOL<sub>TBL</sub><sub>FLUTES</sub> = tooltable(1601, size=200, typ="Int")
self.TOOL<sub>TBL</sub><sub>VIBRATION</sub> = tooltable(1801, size=200)
self.TOOL<sub>TBL</sub><sub>OFFSETS</sub> = tooltable(2001, size=200)
self.TOOL<sub>TBL</sub><sub>WEAR</sub> = tooltable(2201, size=200)
self.TOOL<sub>TBL</sub><sub>DROFFSET</sub> = tooltable(2401, size=200)
self.TOOL<sub>TBL</sub><sub>DRWEAR</sub> = tooltable(2601, size=200)
self.gap07 = Gap(2801, size=199)
self.ALARM = one(3000, typ="Int")
self.T<sub>MS</sub> = one(3001, typ="Time")
self.T<sub>HR</sub> = one(3002, typ="Time")
self.SINGLE<sub>BLOCK</sub><sub>OFF</sub> = ione(3003)
self.FEED<sub>HOLD</sub><sub>OFF</sub> = ione(3004)
self.gap08 = Gap(3005, size=1)
self.MESSAGE = ione(3006)
self.gap09 = Gap(3007, size=4)
self.YEAR<sub>MONTH</sub><sub>DAY</sub> = one(3011, typ="Time")
self.HOUR<sub>MINUTE</sub><sub>SECOND</sub> = one(3012, typ="Time")
self.gap10 = Gap(3013, size=7)
self.POWER<sub>ON</sub><sub>TIME</sub> = one(3020, typ="Time")
self.CYCLE<sub>START</sub><sub>TIME</sub> = one(3021, typ="Time")
self.FEED<sub>TIMER</sub> = one(3022, typ="Time")
self.CUR<sub>PART</sub><sub>TIMER</sub> = one(3023, typ="Time")
self.LAST<sub>COMPLETE</sub><sub>PART</sub><sub>TIMER</sub> = one(3024, typ="Time")
self.LAST<sub>PART</sub><sub>TIMER</sub> = one(3025, typ="Time")
self.TOOL<sub>IN</sub><sub>SPIDLE</sub> = ione(3026)
self.SPINDLE<sub>RPM</sub> = ione(3027)
self.PALLET<sub>LOADED</sub> = ione(3028)
self.gap11 = Gap(3029, size=1)
self.SINGLE<sub>BLOCK</sub> = ione(3030)
self.AGAP = one(3031)
self.BLOCK<sub>DELETE</sub> = ione(3032)
self.OPT<sub>STOP</sub> = ione(3033)
self.gap12 = Gap(3034, size=162)
self.TIMER<sub>CELL</sub><sub>SAFE</sub> = one(3196, typ="Time")
self.gap13 = Gap(3197, size=4)
self.TOOL<sub>TBL</sub><sub>DIAMETER</sub> = tooltable(3201, size=200)
self.TOOL<sub>TBL</sub><sub>COOLANT</sub><sub>POSITION</sub> = tooltable(3401, size=200)
self.gap14 = Gap(3601, size=300)
self.M30<sub>COUNT1</sub> = ione(3901)
self.M30<sub>COUNT2</sub> = ione(3902)
self.gap15 = Gap(3903, size=98)
self.LAST<sub>BLOCK</sub><sub>G</sub> = fixed(4001, size=21)
self.gap16 = Gap(4022, size=79)
self.LAST<sub>BLOCK</sub><sub>ADDRESS</sub> = fixed(4101, size=26)
self.gap17 = Gap(4127, size=874)
self.LAST<sub>TARGET</sub><sub>POS</sub> = cwcpos(5001)
self.MACHINE<sub>POS</sub> = machinepos(5021)
self.WORK<sub>POS</sub> = cwcpos(5041)
self.SKIP<sub>POS</sub> = cwcpos(5061)
self.TOOL<sub>OFFSET</sub> = fixed(5081, size=20)
self.gap18 = Gap(5101, size=100)
self.G52 = workoffsettable(5201)
self.G54 = workoffsettable(5221)
self.G55 = workoffsettable(5241)
self.G56 = workoffsettable(5261)
self.G57 = workoffsettable(5281)
self.G58 = workoffsettable(5301)
self.G59 = workoffsettable(5321)
self.gap19 = Gap(5341, size=60)
self.TOOL<sub>TBL</sub><sub>FEED</sub><sub>TIMERS</sub> = tooltable(5401, size=100, typ="Secs")
self.TOOL<sub>TBL</sub><sub>TOTAL</sub><sub>TIMERS</sub> = tooltable(5501, size=100, typ="Secs")
self.TOOL<sub>TBL</sub><sub>LIFE</sub><sub>LIMITS</sub> = tooltable(5601, size=100, typ="Int")
self.TOOL<sub>TBL</sub><sub>LIFE</sub><sub>COUNTERS</sub> = tooltable(5701, size=100, typ="Int")
self.TOOL<sub>TBL</sub><sub>LIFE</sub><sub>MAX</sub><sub>LOADS</sub> = tooltable(5801, size=100)
self.TOOL<sub>TBL</sub><sub>LIFE</sub><sub>LOAD</sub><sub>LIMITS</sub> = tooltable(5901, size=100)
self.gap20 = Gap(6001, size=197)
self.NGC<sub>CF</sub> = ione(6198)
self.gap21 = Gap(6199, size=802)
self.G154<sub>P1</sub> = workoffsettable(7001)
self.G154<sub>P2</sub> = workoffsettable(7021)
self.G154<sub>P3</sub> = workoffsettable(7041)
self.G154<sub>P4</sub> = workoffsettable(7061)
self.G154<sub>P5</sub> = workoffsettable(7081)
self.G154<sub>P6</sub> = workoffsettable(7101)
self.G154<sub>P7</sub> = workoffsettable(7121)
self.G154<sub>P8</sub> = workoffsettable(7141)
self.G154<sub>P9</sub> = workoffsettable(7161)
self.G154<sub>P10</sub> = workoffsettable(7181)
self.G154<sub>P11</sub> = workoffsettable(7201)
self.G154<sub>P12</sub> = workoffsettable(7221)
self.G154<sub>P13</sub> = workoffsettable(7241)
self.G154<sub>P14</sub> = workoffsettable(7261)
self.G154<sub>P15</sub> = workoffsettable(7281)
self.G154<sub>P16</sub> = workoffsettable(7301)
self.G154<sub>P17</sub> = workoffsettable(7321)
self.G154<sub>P18</sub> = workoffsettable(7341)
self.G154<sub>P19</sub> = workoffsettable(7361)
self.G154<sub>P20</sub> = workoffsettable(7381)
self.gap22 = Gap(7401, size=100)
self.PALLET<sub>PRIORITY</sub> = PalletTable(7501, size=100)
self.PALLET<sub>STATUS</sub> = PalletTable(7601, size=100)
self.PALLET<sub>PROGRAM</sub> = PalletTable(7701, size=100)
self.PALLET<sub>USAGE</sub> = PalletTable(7801, size=100)
self.gap23 = Gap(7901, size=599)
self.ATM<sub>ID</sub> = ione(8500)
self.ATM<sub>PERCENT</sub> = one(8501, typ="Percent")
self.ATM<sub>TOTAL</sub><sub>AVL</sub><sub>USAGE</sub> = ione(8502)
self.ATM<sub>TOTAL</sub><sub>AVL</sub><sub>HOLE</sub><sub>COUNT</sub> = ione(8503)
self.ATM<sub>TOTAL</sub><sub>AVL</sub><sub>FEED</sub><sub>TIME</sub> = one(8504, typ="Secs")
self.ATM<sub>TOTAL</sub><sub>AVL</sub><sub>TOTAL</sub><sub>TIME</sub> = one(8505, typ="Secs")
self.gap24 = Gap(8506, size=4)
self.ATM<sub>NEXT</sub><sub>TOOL</sub><sub>NUMBER</sub> = ione(8510)
self.ATM<sub>NEXT</sub><sub>TOOL</sub><sub>LIFE</sub> = one(8511, typ="Percent")
self.ATM<sub>NEXT</sub><sub>TOOL</sub><sub>AVL</sub><sub>USAGE</sub> = ione(8512)
self.ATM<sub>NEXT</sub><sub>TOOL</sub><sub>HOLE</sub><sub>COUNT</sub> = ione(8513)
self.ATM<sub>NEXT</sub><sub>TOOL</sub><sub>FEED</sub><sub>TIME</sub> = one(8514, typ="Secs")
self.ATM<sub>NEXT</sub><sub>TOOL</sub><sub>TOTAL</sub><sub>TIME</sub> = one(8515, typ="Secs")
self.gap25 = Gap(8516, size=34)
self.TOOL<sub>ID</sub> = ione(8550)
self.TOOL<sub>FLUTES</sub> = ione(8551)
self.TOOL<sub>MAX</sub><sub>VIBRATION</sub> = one(8552)
self.TOOL<sub>LENGTH</sub><sub>OFFSETS</sub> = one(8553)
self.TOOL<sub>LENGTH</sub><sub>WEAR</sub> = one(8554)
self.TOOL<sub>DIAMETER</sub><sub>OFFSETS</sub> = one(8555)
self.TOOL<sub>DIAMETER</sub><sub>WEAR</sub> = one(8556)
self.TOOL<sub>ACTUAL</sub><sub>DIAMETER</sub> = one(8557)
self.TOOL<sub>COOLANT</sub><sub>POSITION</sub> = ione(8558)
self.TOOL<sub>FEED</sub><sub>TIMER</sub> = one(8559, typ="Secs")
self.TOOL<sub>TOTAL</sub><sub>TIMER</sub> = one(8560, typ="Secs")
self.TOOL<sub>LIFE</sub><sub>LIMIT</sub> = one(8561)
self.TOOL<sub>LIFE</sub><sub>COUNTER</sub> = one(8562)
self.TOOL<sub>LIFE</sub><sub>MAX</sub><sub>LOAD</sub> = one(8563)
self.TOOL<sub>LIFE</sub><sub>LOAD</sub><sub>LIMIT</sub> = one(8564)
self.gap26 = Gap(8565, size=435)
self.THERMAL<sub>COMP</sub><sub>ACC</sub> = one(9000)
self.gap27 = Gap(9001, size=15)
self.THERMAL<sub>SPINDLE</sub><sub>COMP</sub><sub>ACC</sub> = one(9016)
self.gap28 = Gap(9017, size=983)
self.GVARIABLES3 = fixed(10000, size=1000)
self.INPUTS1 = fixed(11000, size=256)
self.gap29 = Gap(11256, size=744)
self.OUTPUT1 = fixed(12000, size=256)
self.gap30 = Gap(12256, size=744)
self.FILTERED<sub>ANALOG1</sub> = fixed(13000, size=13)
self.COOLANT<sub>LEVEL</sub> = one(13013)
self.FILTERED<sub>ANALOG2</sub> = fixed(13014, size=50)
self.gap31 = Gap(13064, size=936)
self.SETTING = fixed(20000, size=10000)
self.PARAMETER = fixed(30000, size=10000)

self.TOOL<sub>TYP</sub> = fixed(50001, size=200)
self.TOOL<sub>MATERIAL</sub> = fixed(50201, size=200)
self.gap32 = Gap(50401, 50600)
self.gap32 = Gap(51001, 51300)
self.CURRENT<sub>OFFSET</sub> = fixed(50601, size=200)
self.CURRENT<sub>OFFSET2</sub> = fixed(50801, size=200)
self.VPS<sub>TEMPLATE</sub><sub>OFFSET</sub> = fixed(51301, size=100)
self.WORK<sub>MATERIAL</sub> = fixed(51401, size=200)
self.VPS<sub>FEEDRATE</sub> = fixed(51601, size=200)

self.APPROX<sub>LENGTH</sub> = fixed(51801, size=200)
self.APPROX<sub>DIAMETER</sub> = fixed(52001, size=200)
self.EDGE<sub>MEASURE</sub><sub>HEIGHT</sub> = fixed(52201, size=200)
self.TOOL<sub>TOLERANCE</sub> = fixed(52401, size=200)
self.PROBE<sub>TYPE</sub> = fixed(52601, size=200)

self.PROBE = Alias(self.SKIP<sub>POS</sub>)
self.WORK = Alias(self.WORK<sub>POS</sub>)

self.MACHINE = Alias(self.MACHINE<sub>POS</sub>)
self.G53 = Alias(self.MACHINE<sub>POS</sub>)

def txt<sub>out</sub>(outname, names):
    guts = Table(
        title=f"{names.title} Macro Variables",
        caption=f"Generated by {<span class="underline"><span class="underline">file</span></span>}",
    )

guts.add<sub>column</sub>("Range", justify="right")
guts.add<sub>column</sub>("N", justify="right")
guts.add<sub>column</sub>("K", justify="right")
guts.add<sub>column</sub>("Type", justify="center")
guts.add<sub>column</sub>("Name", justify="left")

snames = sorted(names.interesting)
for el in snames:
    guts.add<sub>row</sub>(\*el.for<sub>txt</sub>())
    if el.alias:
        el = el.alias

with open(outname, "w", encoding="utf-8") as out:
    console = rich.console.Console(file=out)
    console.print(guts, style=None)
    print("Generated ", outname)

def regen<sub>out</sub>(outname, defs):
    with open(outname, "w", encoding="utf-8") as out:
        for el in sorted(defs.interesting):
            out.write("        " + el.for<sub>regen</sub>())

def org<sub>out</sub>(outname, defs):
    with lib.openw(outname) as out:

out.write("| Name | Size | Address |\n")
out.write("| / | <r> |  |\n")

for el in sorted(defs.interesting):
    if el.name != "-":
        out.write(el.for<sub>org</sub>())

out.write("|-&#x2013;&#x2014;|-&#x2013;&#x2014;|----&#x2013;&#x2014;|\n")

def py<sub>out</sub>(target<sub>filename</sub>, defs):
    tmp<sub>filepath</sub> = pathlib.Path(target<sub>filename</sub>).with<sub>suffix</sub>(".tmp")

with open(target<sub>filename</sub>, encoding="utf-8") as inf:
    repl = re.match(
        "(.\*?# MACHINE GEN BELOW.\*?).\*(.\*?# MACHINE.\*)",
        inf.read(),
        flags=re.DOTALL,
    )
if repl is not None:
    with open(tmp<sub>filepath</sub>, "w", encoding="utf-8") as out:
        out.write(repl.group(1) + "\n")
        defs.py<sub>write</sub><sub>to</sub>(out)
        out.write(INDENT + repl.group(2))
    tmp<sub>filepath.rename</sub>(target<sub>filename</sub>)

def makestdvars(outtxt<sub>name</sub>, outdef<sub>name</sub>, outpy<sub>name</sub>, outorg<sub>name</sub>):
    try:
        for names in [HaasNames()]:
            if outtxt<sub>name</sub>:
                txt<sub>out</sub>(outtxt<sub>name</sub>, names)
            if outdef<sub>name</sub>:
                regen<sub>out</sub>(outdef<sub>name</sub>, names)
            if outorg<sub>name</sub>:
                org<sub>out</sub>(outorg<sub>name</sub>, names)
            if outpy<sub>name</sub>:
                py<sub>out</sub>(outpy<sub>name</sub>, names)
    except FileNotFoundError as exc:  # no cover
        print(f"FAIL {exc.args[1]} '{exc.filename}'")
        return 1
    return 0

