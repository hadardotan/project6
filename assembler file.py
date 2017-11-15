import math
import os
import string
import sys
from enum import Enum

C_INSTRUCTION_BINARY_START = "111"
VARIABLE_COUNTER_START = 16
NULL = "null"

def open_path(path):
    """
    :param path:
    :return:
    """
    files = {}
    if os.path.isdir(path):
        dir = os.listdir(path)
        for ob in dir:
            if (not os.path.isdir(ob)) and (
            os.path.basename(ob).endswith(".asm")):
                name = os.path.basename(ob)
                asm_lines = read_asm_file(path + "\\" + name)
                files[name] = asm_lines
        return files, path
    else:
        name = os.path.basename(path)
        asm_lines = read_asm_file(path)
        files[name] = asm_lines
    return files, os.path.dirname(path)

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
    binary = "0" * 16 + "{:b}".format(decimal_int)
    return binary[(len(binary) - 16):]

def initialze_symble_table():
    symble_table = {}
    for i in range(16):
        symble_table["R" + str(i)] = decimal_int_to_binary_16_str(i)
    symble_table["SCREEN"] = decimal_int_to_binary_16_str(16384)
    symble_table["KBD"] = decimal_int_to_binary_16_str(24576)
    symble_table["SP"] = decimal_int_to_binary_16_str(0)
    symble_table["LCL"] = decimal_int_to_binary_16_str(1)
    symble_table["ARG"] = decimal_int_to_binary_16_str(2)
    symble_table["THIS"] = decimal_int_to_binary_16_str(3)
    symble_table["THAT"] = decimal_int_to_binary_16_str(4)
    return symble_table

def first_pass(symble_table, asm):
    new_asm = []
    for line in asm:
        line = line.strip()
        if not line.startswith("//") and not (line == ""):
            new_asm.append(line)
    line_counter = 0
    for line in new_asm:
        if not line.startswith("("):
            line_counter += 1
        else:
            lable_name = line[1:-1]  # without ( )
            symble_table[lable_name] = decimal_int_to_binary_16_str(line_counter)    ####### +1
    no_coments_asm = []
    for line in new_asm:
        if not line.startswith("("):
            line = line.split("//")[0]
            no_coments_asm.append(line)
    # for i in range(len(no_coments_asm)):
    #     print(no_coments_asm[i])
    return symble_table, no_coments_asm

def initialze_dest_table():
    """
    creates dictonary  for translation of symbolic dest c-instruction into
     binary number.

    :return:
    """
    dest_table = {}
    dest_table["null"] = "000"
    dest_table["M"] = "001"
    dest_table["D"] = "010"
    dest_table["MD"] = "011"
    dest_table["A"] = "100"
    dest_table["AM"] = "101"
    dest_table["AD"] = "110"
    dest_table["AMD"] = "111"

    return dest_table

def initialze_jump_table():
    """
    creates dictonary  for translation of symbolic jump c-instruction into
     binary number.

    :return:
    """
    jump_table = {}
    jump_table["null"] = "000"
    jump_table["JGT"] = "001"
    jump_table["JEQ"] = "010"
    jump_table["JGE"] = "011"
    jump_table["JLT"] = "100"
    jump_table["JNE"] = "101"
    jump_table["JLE"] = "110"
    jump_table["JMP"] = "111"

    return jump_table

def initialze_comp_table():
    """
    creates dictonary  for translation of symbolic comp c-instruction into
     binary number. each comp instruction string has a  value in the
     dictonary for his a bit value and his 6 c-bits
     for example:
     "!M" = "0110001"
     means a="0" , (c1...c6)="110001"
    :return:
    """
    comp_table = {}
    comp_table["0"] = "0101010"
    comp_table["1"] = "0111111"
    comp_table["-1"] = "0111010"
    comp_table["D"] = "0001100"
    comp_table["A"] = "0110000"
    comp_table["M"] = "1110000"
    comp_table["!D"] = "0001101"
    comp_table["!A"] = "0110001"
    comp_table["!M"] = "1110001"
    comp_table["-D"] = "1001111"
    comp_table["-A"] = "0110011"
    comp_table["-M"] = "1110011"
    comp_table["D+1"] = "0011111"
    comp_table["A+1"] = "0110111"
    comp_table["M+1"] = "1110111"
    comp_table["D-1"] = "0001110"
    comp_table["A-1"] = "0110010"
    comp_table["M-1"] = "1110010"
    comp_table["D+A"] = "0000010"
    comp_table["D+M"] = "1000010"
    comp_table["D-A"] = "0010011"
    comp_table["D-M"] = "1010011"
    comp_table["A-D"] = "0000111"
    comp_table["M-D"] = "1000111"
    comp_table["D&A"] = "0000000"
    comp_table["D&M"] = "1000000"
    comp_table["D|A"] = "0010101"
    comp_table["D|M"] = "1010101"
    return comp_table

def do_c_instruction(line):
    """
    this function breaks a c-instruction line into its underlying fields:
    dest, comp and jump
    for each field the function generates corresponding binary code,

    then it assemble the translated binary code into 16-bit machine instruction
    :param line: string to translate
    :return: line translated to binary code
    """
    comp_table = initialze_comp_table()
    jump_table = initialze_jump_table()
    dest_table = initialze_dest_table()
    dest_end_index = line.find("=")
    if dest_end_index != -1:
        dest = line[0:dest_end_index]
    else:
        dest = NULL
    jump_start_index = line.find(";")
    if jump_start_index != -1:
        comp = line[(dest_end_index+1):(jump_start_index)]
        jump = line[jump_start_index + 1::]
    else:
        comp = line[(dest_end_index + 1)::]
        jump = NULL
    dest = dest_table[dest.strip()]
    comp = comp_table[comp.strip()]
    jump = jump_table[jump.strip()]
    binary_value = C_INSTRUCTION_BINARY_START + comp + dest + jump
    return binary_value

def add_variable_to_symble_table(symble_table, variable, index):
    """
    adds a new variable to the symble table with its index binary value
    :param symble_table
    :param variable:
    :param index:
    :return: news symble table with the new variable in it
    """

    symble_table[variable] = decimal_int_to_binary_16_str(index)
    return symble_table

def second_pass(symble_table, asm_lines, hack_file):
    """
    :param symble_table:
    :param asm_lines:
    :param hack_file:
    :return:
    """
    variable_counter = VARIABLE_COUNTER_START
    for line in asm_lines:
        if line.startswith("@"): # a-instruction
            line = line[1::]
            if line.isdigit() or line[0] == "-":
                hack_file.write(decimal_int_to_binary_16_str(int(line)) + '\n')
            elif not line in symble_table.keys():
                symble_table = add_variable_to_symble_table(symble_table,line,variable_counter)
                variable_counter += 1
                hack_file.write(symble_table[line] + '\n')
            else:
                hack_file.write(symble_table[line]+ '\n')
        else:
            hack_file.write(do_c_instruction(line)+ '\n')

def create_hack_file(hack_path, asm):
    symble_table = initialze_symble_table()
    hack_file = open(hack_path, "w+")
    symble_table, asm = first_pass(symble_table, asm)
    second_pass(symble_table, asm, hack_file)
    hack_file.close()

def main(path):
    """
    Function that calls the 'run' function to run the game 'Asteroids'.
    :param amnt: An integer defines how many asteroids will be created.
    """
    files, folder_path = open_path(path)
    for key in files.keys():
        name = key[:-4] + ".hack"
        hack_path = folder_path + "\\" + name
        create_hack_file(hack_path, files[key])

example_path = r"C:\Users\mika\Desktop\nand2tetris\nand2tetris\projects\06\our project\examples folder"
main(example_path)
