import os

from ._generate_tools import get_interval
from ..__version__ import __pkg_name__

def generate_html_page(
        data,
        path_css:str="",
        header:str="",
        index_same_dir:bool = False,
        not_above_index: bool = False
):
    """Convert dict create with :func:`extract_profile_data` to an HTML page

:param dict data: {'timer unit', 'total time', 'file', 'function', 'report': [ {line, hits, per hit, % time, line content}, ...]}
:param str path_css: path for the css file
:param str header: Add header
:param bool index_same_dir: Index is in the same directory (priority on not_above_index)
:param bool not_above_index: Not index.html above

:return: HTML content
:rtypes: str
"""
    html = ""

    for line_data in data['report']:

        line = line_data['line']

        if 'hits' in line_data.keys() and line_data['hits'] is not None:
            hits = line_data['hits']
        else:
            hits = ''
        #

        if 'time' in line_data.keys() and line_data['time'] is not None :
            time = line_data['time']
        else:
            time = ''
        #

        if 'per hit' in line_data.keys() and line_data['per hit'] is not None:
            per_hit = line_data['per hit']
        else:
            per_hit = ''
        #

        if '% time' in line_data.keys() and line_data['% time'] is not None:
            time_percentage = line_data['% time']
        else:
            time_percentage = ''
        #

        if 'line content' in line_data.keys() and line_data['line content'] is not None:
            line_content = line_data['line content']
        else:
            line_content = ''
        #

        html += f'''
            <tr class="{get_interval(time_percentage)}">
                <td class="line-number">{line}</td>
                <td class="hits">{hits}</td>
                <td class="time">{time}</td>
                <td class="per-hit">{per_hit}</td>
                <td class="percentage">{time_percentage}</td>
                <td class="line-content">{line_content}</td>
            </tr>
        '''
    # endFor
    template_html = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "template",
            "page.html"
        )
    )
    with open(template_html, "r") as f:
        page = f.read()
    # endWith

    if index_same_dir:
        page = page.replace(
            '<a href="../index.html">',
            '<a href="./index.html">'
        )
    elif not_above_index:
        page = page.replace(
            '<a href="../index.html">',
            '<a href="#">',
        )
    #

    page = page.replace(":HEADER:", f"<div id='header'>{str(header)}</div>" if header else "")
    page = page.replace(
        ":TIME_UNIT:",
        str(data['timer unit'])
        if 'timer unit' in data.keys() and
        data['timer unit'] is not None
        else ''
    )
    page = page.replace(
        ":TOTAL_TIME:",
        str(data['total time'])
        if 'total time' in data.keys() and
        data['total time'] is not None
        else ''
    )
    page = page.replace(
        ":FILE:",
        str(data['file'])
        if 'file' in data.keys() and
        data['file'] is not None
        else ''
    )
    page = page.replace(
        ":FUNCTION:",
        str(data['function'])
        if 'function' in data.keys() and
        data['function'] is not None
        else ''
    )
    page = page.replace(
        ":CONTENT:",
        str(html)
        if html is not None
        else ''
    )

    if path_css:
        page = page.replace("./style.css", os.path.join(path_css, "style.css"))
    # endIf

    return page


