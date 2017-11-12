import math
import os
import sys


def open_path(path):
    files = {}
    if os.path.isdir(path):
        dir = os.listdir(path)
        for ob in dir:
            if (not os.path.isdir(ob)) and (os.path.basename(ob).endswith(".asm")):
                name = os.path.basename(ob)
                asm_lines = read_asm_file(path+"\\"+name)
                files[name] = asm_lines
        return files, path
    else:
        name = os.path.basename(path)
        asm_lines = read_asm_file(path)
        files[name] = asm_lines
    return files , os.path.dirname(path)

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
    asm_file.close()
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


def first_pass(symble_table,asm):
    no_coments_asm =[]
    for line in asm:
        line = line.strip()
        if not line.startswith("//") and  not (line == "" ):
            no_coments_asm.append(line)
    line_counter = 0
    for line in no_coments_asm:
        if not line.startswith("("):
            line_counter += 1
        else:
            lable_name = line[1:-2]   # without ( )
            symble_table[lable_name] = line_counter + 1
    return symble_table,no_coments_asm

def second_pass(symble_table,asm_lines,hack_file):
    variable_number = 16
    for i in range(len(asm_lines)):
        print(asm_lines[i])




def create_hack_file(hack_path,asm):
    symble_table = initialze_symble_table()
    hack_file = open(hack_path,"w+")
    hack_file.write("hi new hack file")
    symble_table, asm = first_pass(symble_table,asm)
    second_pass(symble_table, asm,hack_file)
    hack_file.close()




def main(path):
    """
    Function that calls the 'run' function to run the game 'Asteroids'.
    :param amnt: An integer defines how many asteroids will be created.
    """
    files,folder_path = open_path(path)

    for key in files.keys():
        name = key[:-4] + ".hack"
        hack_path = folder_path + "\\" + name
        create_hack_file(hack_path,files[key])



example_path = r"C:\Users\mika\Desktop\nand2tetris\nand2tetris\projects\06\our project\examples folder\max.asm"
main(example_path)

""""
if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(sys.argv[0])
"""
