"""
@author: Pierre
"""

if __name__=="__main__":
    from os import path as os_path
    from sys import path as sys_path

    path=os_path.dirname(os_path.abspath(__file__))
    sys_path.insert(0, os_path.join(path, "../../.."))
    path=None
    #print(sys.path)
#endIf

def simplify_html(self, content, resplit=False, recurs=False, **kwargs):
    """Simplify the HTML page : remove the span balise for exemple

:param str|list|dict content: Content to simplify
:param bool resplit: Resplit datas (on ponctuation)
:param bool recurs: For recusivity if content is list|dict
"""

    if content is None and not recurs:
        content = self.data
    #endIf

    if isinstance(content, list) or isinstance(content, tuple):

        l = [
            self.simplify_html(content=e, resplit=resplit, recurs=True)
            for e in content
        ]

        if l:
            return l
        else:
            return None if self.convertEmptyNone else ""
        #endIf

    elif isinstance(content, dict):

        if self.convert_keys:
            return {
                self.simplify_html(content=k, resplit=resplit, recurs=True)
                :
                self.simplify_html(content=v, resplit=resplit, recurs=True)
                for k, v in content.items()
            }
        else:
            return {
                k
                :
                self.simplify_html(content=v, resplit=resplit, recurs=True)
                if not k in self.skip_values else v
                for k, v in content.items()
            }
        #endIf

    elif isinstance(content, int) or isinstance(content, float):

        content = str(content)

    elif content is None:

        return None if self.convertEmptyNone else ""

    elif not isinstance(content, str) or not content:

        return None if self.convertEmptyNone else ""

    #endIf

    if resplit:
        content=content.replace(".",".<br/>")
        content=content.replace(";",";<br/>")
        content=content.replace(":",":<br/>")
    #endIf

    # Simplifications
    _replaceRVerset="/®®®/"
    _replaceVVerset="/ßßß/"
    content=content.replace('<font color="#ff0000">','')
    content=content.replace('</font>','')
    content=content.replace('<strong><span class=\"verse_number\">R/</span> </strong>','R/ ')
    content=content.replace('<strong><span class=\"verse_number\">R/</span></strong>','R/ ')
    content=content.replace('<strong> <span class=\"verse_number\">R/</span></strong>','R/ ')
    content=content.replace('<strong> <span class=\"verse_number\">R/</span> </strong>','R/ ')
    content=content.replace('<span class="verse_number">R/</span>', "R/ ")
    content=content.replace('<span class="verse_number">V/</span>', "V/ ")
    content=content.replace('<span class="verse_number">R/', _replaceRVerset) # pour eviter les soucis, avec <span>R/ 01</span> par exemple ds les psaumes
    content=content.replace('<span class="verse_number">V/', _replaceVVerset)
    content=content.replace('<span class=\"verse_number\">',"<b>")
    content=content.replace('<span class="verse_number">','<b>')
    content=content.replace('<span class=\"chapter_number\">', '<b>')
    content=content.replace('<span class="chapter_number">', '<b>')
    content=content.replace("</span>"," </b>")
    content=content.replace("<span>","<b>")
    content=content.replace("<strong>","<b>")
    content=content.replace("</strong>","</b>")
    content=content.replace("<em>","<i>")
    content=content.replace("</em>","</i>")
    content=content.replace("<br>","<br/>")
    content=content.replace("<br />","<br/>")
    content=content.replace("<br />","<br/>")
    content=content.replace("<br\xa0/>","<br/>")
    #content=content.replace("\n\n\n","<br/><br/>")
    #content=content.replace("\n\n\n\n","<br/><br/>")
    #content=content.replace("\n\n","<br/><br/>")
    content=content.replace("\n","")
    content=content.replace("*","<b>&star;</b>")
    content=content.replace("+","<b>+</b>")
    content=content.replace("_","&lowbar;")

    # Ajout gras la ou il n'y en a pas
    content=content.replace("R/","<b>R/</b>")
    content=content.replace("V/","<b>V/</b>")
    if("(<b>" in content and "</b>)" in content):
        content=content.replace("(<b>","<b>(").replace("</b>)",")</b>")
    #endIf


    content=content.replace(_replaceRVerset,"<b>R/ ") # la fermeture de la balise devrait aller apres le </span> quand il y a des versets ;)
    content=content.replace(_replaceVVerset,"<b>V/ ")

    # Doublons (pre)
    #content=content.replace("<span><span>","").replace("</span></span>","")

    self.removeDuplicates(content, tag="b")
    self.removeDuplicates(content, tag="i")
    self.removeDuplicates(content, tag="u")

    content="<br/>".join([e.strip() for e in content.split("<br/>")]).strip()

    return content

#endDef
