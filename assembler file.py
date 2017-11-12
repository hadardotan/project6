


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
    while asm_file.readline():
        line_number += 1
    line_number.close()
    return line_number

def initialze_symble_table():
    symble_table = {}
    # "R0":"0","R1":"1","R2":"2","R3":"3","R4":"4","R5":"5","R6":"6",
    for i in range(16):
        symble_table["R"+str(i)] = str(i)
    print(symble_table)


def binary_str_to_decimal_int(binary_string):
    return int(binary_string, 2)






def decimal_int_to_binary_str(decimal_int):
    return "{:b}".format(decimal_int)



