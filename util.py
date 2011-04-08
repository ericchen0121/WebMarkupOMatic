def lines(file):
    """adds a newline to the end of the file"""
    for line in file: yield line
    yield '\n'

def blocks(file): 
    """
    For each line with a newline at the end, it adds it to the block list.
    Then, it joins them all and resets the block to empty.
    """
    block = []
    for line in lines(file): 
        if line.strip():
            block.append(line)
        elif block: 
            yield ''.join(block).strip()
            block = []
