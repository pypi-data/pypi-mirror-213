import traceback
from ..function_recursive import recurs_function

def html_to_utf8(self, data=None, recurs=False, inplace=False, **kwargs)->str:
    """Convert HTML to UTF8

:param str|list|dict data: Input datas
:param bool recurs: Use recursivity (if list, dict)
:param bool inplace: (False) Replace self.data and return None
"""

    if kwargs:
        t = traceback.format_list(traceback.extract_stack())
        sys.stderr.write("> WARNING Unexpected kwargs, but not critical\n")
        sys.stderr.write("".join(t))
    #endIf

    if data is None and not recurs:
        data = self.data
    #endIf

    if not isinstance(data, str):

        recurs_datas = recurs_function(
            self.html_to_utf8,
            data=data,
            recurs=recurs,
            inplace=inplace,
            convertEmptyNone = self.convertEmptyNone,
            convert_keys = self.convert_keys,
            skip_values = self.skip_values,
            **kwargs
        )

        if inplace:
            self.data = recurs_datas
            return None
        else:
            return recurs_datas
        #endIf

    #endIf

    for k, v in self.characters_html_utf8.items():
        data = data.replace(k, v)
    #endFor

    if inplace:
        self.data = data
        return None
    else:
        return data
    #endIf

#endDef

