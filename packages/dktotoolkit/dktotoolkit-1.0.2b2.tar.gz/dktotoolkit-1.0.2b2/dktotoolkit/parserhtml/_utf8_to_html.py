import traceback
from ..function_recursive import recurs_function
from ..functions import compatMode

def utf8_to_html(self, convertbreaklines:bool=False, data:str=None, cleanHTML:bool=False, recurs:bool=False, inplace:bool=False, **kwargs)->str:
    """ Convert utf8 / html+utf8 to pure HTML
:param bool convertbreaklines: Convert \n to <br/>
:param str|list|dict data: Input datas
:param bool recurs: Use recursivity (if list, dict)
:param bool inplace: (False) Replace self.data and return None
:param bool cleanHTML: Clean the HTML (default: False)
Warning : by default, delete \n (convertbreaklines has the priority) !
"""

    cleanHTML_proper, kwargs_proper = compatMode("cleanHTML", ["cleanhtml", "clean_HTML", "clean_html"], **kwargs)
    if cleanHTML_proper:
        cleanHTML, kwargs = cleanHTML_proper, kwargs_proper
    #endIf

    if kwargs:
        t = traceback.format_list(traceback.extract_stack())
        sys.stderr.write("> WARNING Unexpected kwargs, but not critical\n")
        sys.stderr.write("".join(t))
    #endIf

    if data is None and not recurs:
        data = self.data
    #endIF

    if data is None:
        return None
    elif not isinstance(data, str):

        recurs_datas = recurs_function(
            self.utf8_to_html,
            data=data,
            convertbreaklines=convertbreaklines,
            cleanHTML=cleanHTML,
            recurs=True,
            inplace=False,
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

    if convertbreaklines:
        data = data.replace("\n", "<br/>")
    #endIf

    if cleanHTML:
        data = self.simplify_html(content=data, recurs=False, **kwargs)
    #endIf

    if data is None and inplace:
        self.data = None
        return None
    elif data is None:
        return None
    #endIf

    balises_html = ["<", ">", " "]

    # Replace
    for k, v in self.characters_html_utf8.items():
        if v in balises_html:
            continue
        #endIf
        data = data.replace(v, k)
    #endFor

    if inplace:
        self.data = data
        return None
    else:
        return data
    #endIf

    return None

#endDef
