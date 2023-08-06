def get_interval(number):
    """
    Convert a percentage to an interval

:param float number: A percentage

:return: palierX, with X between a = 0%-10% and j=90-100%
:rtypes: str
"""

    if isinstance(number, str):
        return "nohit"
    # endIf

    i = int(number // 10)
    l = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

    return f'palier{l[i]}'
#
