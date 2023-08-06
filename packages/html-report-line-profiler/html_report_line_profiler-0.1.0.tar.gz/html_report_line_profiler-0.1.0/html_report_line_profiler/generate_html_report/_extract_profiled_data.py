import io

from ._extract_tools import convertLeadTrailSpace, linecols2dict

def extract_profiled_data(stream=None, file_name:str=None):
    """
Extract the profiled data

:param io.StringIO stream: a stream (NOT TESTED), or a string (with datas)
:param str file_name: the filename

:return: {'timer unit', 'total time', 'file', 'function', 'report': [ {line, hits, per hit, % time, line content}, ...]}
:rtypes: dict
"""

    if isinstance(stream, str):
        profile_text = stream
    elif isinstance(stream, io.StringIO):
        profile_text = stream
    elif stream is None and file_name is not None:
        with open(file_name, 'r') as f:
            profile_text = f.read()
        # endWith
    #endIf

    profile_text_split = [e for e in profile_text.split("\n")]

    startCodeIdx = 0  # Index du debut du code
    timer_unit = ""
    total_time = ""
    file_info = ""
    function_info = ""

    data = {}
    i = 0
    report = []

    while i < len(profile_text_split):

        if not profile_text_split[i]:
            pass
        elif profile_text_split[i].startswith('Timer unit:'):
            timer_unit = profile_text_split[i].replace('Timer unit:', '').strip()
        elif profile_text_split[i].startswith('Total time:'):
            total_time = profile_text_split[i].replace('Total time:', '').strip()
        elif profile_text_split[i].startswith('File:'):
            file_info = profile_text_split[i].replace('File:', '').strip()
        elif profile_text_split[i].startswith('Function:'):
            function_info = profile_text_split[i].replace('Function:', '').strip()
        elif profile_text_split[i].startswith('Line'):
            startCodeIdx = profile_text_split[i].index("Line Contents")
        elif  profile_text_split[i].startswith('=') :
            pass
        else:

            line_data = profile_text_split[i].strip().split()

            if len(line_data) > 1 and line_data[1].isdigit():
                content = convertLeadTrailSpace(profile_text_split[i][startCodeIdx:])
                line_data_dict = linecols2dict(
                    content=content,
                    line=line_data[0],
                    hits=line_data[1],
                    time=line_data[2],
                    perhit=line_data[3],
                    percent=line_data[4]
                )
            elif len(line_data) > 1:
                content = convertLeadTrailSpace(profile_text_split[i][startCodeIdx:])
                try:
                    line = float(line_data[0])
                    line_data_dict = linecols2dict(
                        content=content,
                        line=line
                    )
                except ValueError:
                    i += 1
                    continue
                #

            else:
                try:
                    line = float(line_data[0])
                    line_data_dict = linecols2dict(
                        content=None,
                        line=line
                    )
                except ValueError:
                    i += 1
                    continue
                #

            #

            report.append(line_data_dict)
        # endIf
        i = i + 1
    # endWhile
    section_data = {
        'timer unit': timer_unit,
        'total time': total_time,
        'file': file_info,
        'function': function_info,
        'report': report
    }

    return section_data
