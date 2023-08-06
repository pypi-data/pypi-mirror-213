import traceback
from ..function_recursive import recurs_function

def html_to_markdown(self, displayMarkdown=False, data=None, recurs=False, inplace=False, **kwargs)->str:
    """Convert HTML to Markdown

:param bool displayMarkdown: Add backslash to display the markdown content
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

    if not isinstance(data,str):

        recurs_datas = recurs_function(
            self.html_to_markdown,
            data=data,
            recurs=True,
            displayMarkdown=displayMarkdown,
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

    escaped_markdown = ["&star;", "&lowbar;"]  # Necessite echappement

    for k, v in self.characters_html_utf8.items():
        if k in escaped_markdown:
            data = data.replace(k, f"\{v}")
        else:
            data = data.replace(k, v)
        #endIf
    #endFor


    if(displayMarkdown):
        balises_html_to_markdown = {
            "&gt;":"\>",
            "&lt;":"<",
            "&star;":"\\\\\*",
            "&plus;":"+",
            "&lowbar;":"\\\\\_",
            "_":"\_",
            "*":"\*"
        }
    else:
        balises_html_to_markdown={
            "&gt;":">",
            "&lt;":"<"
        }
    #endIf

    for k, v in self.balises_html_markdown.items():
        data = data.replace(k,v)
    #endFor

    if inplace:
        self.data = data
        return None
    else:
        return data
    #endIf

#endDef
