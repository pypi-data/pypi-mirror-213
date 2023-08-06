# -*- coding: utf-8 -*-
from ._remove_duplicates import _removeDuplicates

class ParserHTML:
    def __init__(self,
                 data_input:str=None,
                 convertEmptyNone:bool=False,
                 convert_keys:bool=False,
                 skip_values:list=[]
                 ):
        """Parser un texte, une liste, un dictionnaire

:param str|int|float|list|tuple|dict data_input: Donnee a convertir (recursif)
:param bool convertEmptyNone: If True return None if field empty, if False return ''
:param bool convert_keys: If type(data_input) is dict : If True parse keys of dict  else not parse keys
:param list|str|int skip_values: Values to skip if data_input is list (int/list[int]) or dict (str/list[str]) ; UNIQUEMENT AVEC DICT ET CONVERT_KEY=FALSE POUR LE MOMENT
"""

        self.data = data_input
        self.convertEmptyNone = convertEmptyNone
        self.convert_keys = convert_keys
        self.skip_values = [skip_values,] if not isinstance(skip_values, list) else skip_values
        # https://www.journaldunet.com/solutions/dsi/1195751-accents-caracteres-speciaux-html/

        self.characters_html_utf8={
            # A
            "&agrave;":"à", "&Agrave;":"À",
            "&acirc;":"â",  "&Acirc;":"Â",    "&auml;":"ä",  "&Auml;":"Ä",
            # E
            "&eacute;":"é", "&Eacute;":"É",   "&egrave;":"è","&Egrave;":"È",
            "&ecirc;":"ê",  "&Ecirc;":"Ê",    "&euml;":"ë",  "&Euml;":"Ë",
            # I
            "&icirc;":"î",  "&Icirc;":"Î",    "&iuml;":"ï",  "&Iuml;":"Ï",
            # O
            "&ocirc;":"ô",  "&Ocirc;":"Ô",    "&ouml;":"ô",  "&Ouml;":"Ö",
            # U
            "&ograve;":"ù", "&Ograve;":"Ù",
            "&ucirc;":"û",  "&Ucirc;":"Û",    "&uuml;":"ü",  "&Uuml;":"Ü",
            # Ligatures
            "&aelig;":"æ",  "&AEmig;":"Æ",
            # Symboles
            "&nbsp;":"\xa0",
            "&rsquo;":"'",
            "&laquo;":"«",   "&raquo;":"»",
            "\xa0":" ",
            "&#8217;":"’", # en vrai, c'est un rsquo, mais comme il est deja utilise...
            "\xa0":" ","&nbsp;":" ","&8239;":" ","&thinsp;":" "," ":" ",
            "&star;":"*", "&plus;":"+", "&minus;":"-", "&lowbar;":"_",
            "&gt;":">", "&lt;":"<"
        }

        self.balises_html_markdown={
            "<p>":"", "</p>":"\n",
            "<br/>":"\n",
            "<u>":"__", "</u>":"__",
            "<i>":"*",  "</i>":"*",
            "<b>":"**", "</b>":"**",
        }
    #endDef

    from ._html_to_utf8 import html_to_utf8
    from ._utf8_to_html import utf8_to_html
    from ._html_to_markdown import html_to_markdown
    from ._simplify_html import simplify_html

    # Static methods
    @staticmethod
    def removeDuplicates(content, tag="br"):
        """
        Supprime les balises en double dans le contenu HTML.

        :param content: Le contenu HTML à traiter.
        :type content: str
        :param tag: Le nom de la balise à vérifier pour les doublons, par défaut "br".
        :type tag: str
        :returns: Le contenu HTML avec les balises en double supprimées.
        :rtype: str
        :raises Exception: Si une erreur se produit lors du traitement du contenu HTML.
        """
        return _removeDuplicates(content=content, tag=tag)
    #endDef

    # Class methods



#endClass

