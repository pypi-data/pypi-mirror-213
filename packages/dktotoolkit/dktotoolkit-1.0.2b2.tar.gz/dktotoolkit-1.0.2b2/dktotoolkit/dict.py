def dict2obj(d=None, obj=None):
    """Convert nested Python dictionnary to object

:author: geeksforgeeks.org

:param dict d: input dictionnary
:param obj: a class (could be empty)
    """

    if isinstance(d, list):  # si d est une liste
        d = [dict2obj(x) for x in d]
    # endIf

    if not isinstance(d, dict):  # si d est un dico
        return d
    # endIf

    if obj is None:
        class C:
            pass
        # endClass

        obj = C()
    # endIf

    for k in d:
        obj.__dict__[k] = dict2obj(d[k])
    # endFor

    return obj

# endDef
