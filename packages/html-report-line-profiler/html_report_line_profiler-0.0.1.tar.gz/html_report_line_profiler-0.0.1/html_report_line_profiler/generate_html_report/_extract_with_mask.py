def extractWithMask(the_list, the_mask, len_list:int=-1, rangelen_list:list=[]):
    """
Return a sublist using a mask. If mask[elt] == True : keep the element

:param list the_list: List where datas must be extracted
:param list the_mask: List of boolean
:param int len_list: Len of the list (to optimize loops)
:param rangelen_list: Range of the of the list (to optimize loops)

:return: the list, where mask is True
:rtypes:list

:todo: deplacer dans toolbox
"""

    if rangelen_list:
        return [the_list[i] for i in rangelen_list if the_mask[i]]
    elif len_list >= 0:
        rangelen_list = range(len_list)
        return [the_list[i] for i in rangelen_list if the_mask[i]]
    else:
        rangelen_list = range(len(the_list))
        return [the_list[i] for i in rangelen_list if the_mask[i]]
    # endIf

    return []
# endDef
