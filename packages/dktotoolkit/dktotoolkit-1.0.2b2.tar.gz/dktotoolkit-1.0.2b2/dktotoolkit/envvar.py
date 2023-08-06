import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from .list import castList
from .str import str2digit


def load_dotenv(
        filename: str = "./.env",
        erase_variable: bool = False
) -> None:
    """Load .env file

:param str filename: Path and name of the file (default: ./.env)
:param bool erase_variable: Erase variable if already exists (default: False)

:return: Only add the values (str) inside environment variables
:rtypes: None
"""

    sys.stdout.write(F"> Load environment file : {filename}\n")

    with open(filename, 'r') as f:

        lines = f.readlines()

        for line in lines:

            linesplit = line.split("\n")[0].split("#")[0].split("=")

            if len(linesplit) > 1:

                var = linesplit[0].strip()
                val = linesplit[1].strip().replace(",", ":").replace(";", ":")

                if os.environ.get(var, False) and not erase_variable:
                    msg = F"load_env> {var} = {os.environ.get(var)} "
                    msg += "(already set, erase_variable)\n"
                    sys.stdout.write(msg)
                # endIf

                sys.stdout.write(F"load_env> {var} = {val} : ")
                if "\"" in val:
                    msg = "warning : character \" "
                    msg += "in content (character removed)"
                    sys.stdout.write(msg)
                    val = val.replace("\"", "")
                else:
                    sys.stdout.write("Done")
                # endIf

                if not os.environ.get(var, False) or not erase_variable:
                    # On ne peut avoir en var que des str
                    os.environ[var] = val
                # endIf

                sys.stdout.write("\n")

            # endIf
        # endFor
    # endWith

    sys.stdout.write("\n")

    # TODO : ajouter valeurs par defaut si pas presentes !

# endDef


def getEnvironVar(varname: str, digit: bool = False):
    """Get environ variable

:param str varname: Name of the variable
:param bool digit: Try to convert to digit  (default: False)
"""

    if varname is None:
        return None
    # endIf

    var = os.environ.get(varname)

    for char in [":", ";", ","]:  # separators
        if char in var:

            L = castList(var, char, digit=digit)
            if L is not None:
                return L
            # endIf
        # endIf
    # endFor

    if digit:
        return str2digit(var.strip())
    else:
        return str(var.strip())
    # endIf

# endDef


def getTimesReminder(
        dotenv_timevar: str = "REMINDER",
        outdico: bool = False
):
    """Recuperer une liste d'heures
REMINDER=hhmmss:hhmmss
"""
    # If no tzinfo is given then UTC is assumed.
    tzone = ZoneInfo(getEnvironVar("TZONE", "Europe/Paris"))

    tuples_dotenv = getEnvironVar(dotenv_timevar)
    dico_out = {}

    if tuples_dotenv is None:
        return []
    # endIf

    for office, time in tuples_dotenv:
        l_hourMinSec = ["", "", ""]
        i = 0
        for char in time:

            if char.isdigit():
                l_hourMinSec[i] = l_hourMinSec[i] + char
                justchange = False
            elif not justchange:
                i += 1
                justchange = True
            # endIf
        # endFor

        l_hourMinSec = [int(e) if e else 0 for e in l_hourMinSec]
        d_hourMinSec = {
            "hour": l_hourMinSec[0],
            "minute": l_hourMinSec[1],
            "second": l_hourMinSec[2]
        }

        dico_out[office] = d_hourMinSec
        dico_out[office]["time"] = datetime.time(**d_hourMinSec, tzinfo=tzone)

    # endFor

    if outdico:
        return dico_out
    else:
        return [v["time"] for k, v in dico_out.items()]
    # endIf

# endDef
