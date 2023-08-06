def linecols2dict(content="", line=None, hits=None, time=None, perhit=None, percent=None):
    """
    Convert cols to a dictionnary

:param str content: the code
:param str line: the line number
:param str hits: the number of hits
:param str time: the total time passed on a line
:param str perhit: the time passed by hit on a line
:param str percent: the percent time passed on a line

:return: {line, hits, time, per hit, % time, line content}
:rtypes: dict
"""
    return {
        'line': int(line) if line else None,
        'hits': int(hits) if hits else None,
        'time': float(time) if time else None,
        'per hit': float(perhit) if perhit else None,
        '% time': float(percent) if percent else None,
        'line content': content
    }
# endDef


def convertLeadTrailSpace(chaine, char="\u00A0"):
    """
Convert leading and trailing spaces

:param str chaine: the input string
:param str char: the character to replace the leading and trailing spaces (\u00A0 = insecable, · = median point, ...)

:return: the string, with leading and trailing spaces replaced by the char
:rtypes: str
"""

    nb_debut = abs(len(chaine.lstrip()) - len(chaine))
    nb_fin = abs(len(chaine.rstrip()) - len(chaine))

    return char * nb_debut + chaine.strip() + char * nb_fin
# endDef
