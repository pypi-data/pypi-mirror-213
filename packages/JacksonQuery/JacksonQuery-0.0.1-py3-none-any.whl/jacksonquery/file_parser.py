from tika import parser as parser


def parse_file(filepath):
    """
    Parses a PDF file into a list of strings.

    :param filepath: (str) Path to the PDF file.
    :return: (list) List of strings.
    """
    raw = parser.from_file(filepath)
    string_list = raw.get('content').split('\n')
    string_list = list(filter(None, string_list))  # filter Nones
    string_list = [s for s in string_list if s != ' ']  # filter whitespaces

    return string_list


def parse_names(string_list):
    """
    Parses a list of strings into a list of subaccount names.

    :param string_list: (list) List of strings.
    :return: (list) List of subaccount names.
    """
    section_name = 'TABLE OF CONTENTS '
    subaccount_names = string_list[string_list.index(section_name) + 5:string_list.index('Additional Information '
                                                                                         'About the Funds 772 ')]
    for s in subaccount_names:
        subaccount_names[subaccount_names.index(s)] = ' '.join(s.split(' ')[:-2])

    return subaccount_names


def split_into_sublists(string_list, subaccount_names):
    """
    Splits a list of strings into a list of sublists, where each sublist is a subaccount.

    :param string_list: (list) List of strings.
    :param subaccount_names: (list) List of subaccount names.
    :return: (list) List of sublists.
    """
    sublists = []
    current_sublist = []

    string_list = string_list[430:39248]  # filter prospectus's start and end
    for line in string_list:
        line_stripped = line.strip()  # Remove leading and trailing whitespaces
        if line_stripped in subaccount_names:
            if current_sublist:  # If the current sublist is not empty, add it to the list of sublists
                sublists.append(current_sublist)
            current_sublist = [line_stripped]  # Start a new sublist with the current line
        else:
            current_sublist.append(line)  # Add the current line to the current sublist

    # Add the last sublist to the list of sublists
    if current_sublist:
        sublists.append(current_sublist)

    return sublists[1:]
