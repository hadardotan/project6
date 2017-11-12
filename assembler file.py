


def read_asm_file(file_path):
    """
    This function returns a list of string, each string is a line from asm file.
    :param file_path
    :return: asm_lines
    """
    asm_file = open(file_path)
    asm_lines = []
    file_length = number_of_lines(file_path)
    for i in range(file_length):
        line = asm_file.readline()
        #do something with line
        asm_lines.append(line)
    asm_file.close()
    return asm_lines


def number_of_lines(file_name):
    """
    This function return the lenght (of rows) of asm file
    :param file_name:
    :return: line_number
    """
    asm_file = open(file_name)
    line_number = 0
    while line_number.readline():
        line_number += 1
    line_number.close()
    return line_number



