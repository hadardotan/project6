import math


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

def binary_str_to_decimal_int(binary_string):
    return int(binary_string, 2)

def decimal_int_to_binary_16_str(decimal_int):
    if decimal_int < 0:  # 2's complement
        x = int(math.pow(2, 16) + decimal_int)
        a = "{:b}".format(x)
        return a
    binary = "0"*16 + "{:b}".format(decimal_int)
    return binary[(len(binary) - 16):]




def initialze_symble_table():
    symble_table = {}
    for i in range(16):
        symble_table["R"+str(i)] = decimal_int_to_binary_16_str(i)
    symble_table["SCREEN"] = decimal_int_to_binary_16_str(16384)
    symble_table["KBD"] = decimal_int_to_binary_16_str(24576)
    symble_table["SP"] = decimal_int_to_binary_16_str(0)
    symble_table["LCL"] = decimal_int_to_binary_16_str(1)
    symble_table["ARG"] = decimal_int_to_binary_16_str(2)
    symble_table["THIS"] = decimal_int_to_binary_16_str(3)
    symble_table["THAT"] = decimal_int_to_binary_16_str(4)
    return symble_table


s = initialze_symble_table()
print(s)

