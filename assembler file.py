


def read_asm_file(file_path):
    """
    This function returns a list of tuples, representing Articles that are
    neighbors. The tuple contain two string, which are the articles titles.
    The second article is neighbor to the first: the first one has link to its
    pair in the tuple.
    :param file_name
    :return: list of tuples
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
    This function "helps" the function "read_article_links" by counting the
    number of lines in the file
    :param file_name:
    :return:
    """
    asm_file = open(file_name)
    line_number = 0
    while line_number.readline():
        line_number += 1
    line_number.close()
    return line_number







