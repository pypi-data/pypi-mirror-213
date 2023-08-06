from .exceptions import ParseError


def str2digit(input_str: str, sep: str = ":"):
    """
    Try to convert an input to a digit or a list of digit
TODO ! Add recurse function inside funcitons.py and use here !

:param str input_str: the input
:param str sep: the separator if it is a list (default: ":")

:return: the value as digit / as float / as list / as str
"""

    if input_str.isdigit():

        return int(input_str)

    elif not isinstance(input_str, str):  # pragma: no cover

        msg = f"> {input_str} is not a string ({type(input_str)})\n"
        raise ParseError(msg)

    # endIf

    if sep in input_str:
        lval = input_str.split(sep)
        lout = []

        for e in lval:

            if e.isdigit():
                lout.append(int(e))
                continue
            else:
                try:
                    lout.append(float(e))
                except ValueError:
                    lout.append(e)
                    continue
                # endTry
            # endIf

        # endFor

        return lout

    else:

        try:
            return float(input_str)
        except ValueError:  #
            return input_str
        # endTry

    # endIf

    raise ValueError  # pragma: no cover
# endDef
