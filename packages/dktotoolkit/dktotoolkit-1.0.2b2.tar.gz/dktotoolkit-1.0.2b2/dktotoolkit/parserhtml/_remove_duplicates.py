_this_file_="html._removeDuplicates.py"

import traceback
from bs4 import BeautifulSoup, Tag
from sys import stderr as sys_stderr

def _removeDuplicates(content, tag="br"):
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

    try:
        soup = BeautifulSoup(content)
    except Exception as e:
        sys_stderr.write(f"{_this_file_} (1)\n")
        traceback.print_exc()
        raise Exception
    #endTry

    for br in soup.find_all(tag):

        while isinstance(br.next_sibling, Tag) and br.next_sibling.name == tag:
            br.next_sibling.extract()
        #endWhile

    #endFor

    return str(soup)
#endDef
