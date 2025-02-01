def convert_to_nexus(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        ntax = len(lines)
        nchar = len(lines[0].strip().split()[1]) # Get length of the sequence
        print(nchar, ntax)

        outfile.write("#NEXUS\n")
        outfile.write("BEGIN DATA;\n")
        outfile.write(f"    DIMENSIONS NTAX={ntax} NCHAR={nchar};\n")
        outfile.write("    FORMAT DATATYPE=STANDARD GAP=- MISSING=? ;\n")
        outfile.write("    MATRIX\n")

        for line in lines:
            parts = line.strip().split()
            print(parts)
            taxon_name = parts[0]
            sequence = parts[1]
            outfile.write(f"    {taxon_name} {sequence}\n")

        outfile.write("    ;\n")
        outfile.write("END;\n")

# Example usage:
# convert_to_nexus("/Users/claudiucreanga/projects/Boundaries/Beast_table_revised_2.txt", "/Users/claudiucreanga/projects/Boundaries/output.nex") # Replace with your file names

def check_sequence_lengths(nexus_file):
    with open(nexus_file, 'r') as infile:
        lines = infile.readlines()
    print(len(lines))
    in_matrix = False
    for line_num, line in enumerate(lines):
        line = line.strip()  # Remove whitespace
        if line == "matrix":
            in_matrix = True
        elif line == ";":  # Exit after the matrix
            in_matrix = False
            break
        elif in_matrix and line != "": #check if we are in the matrix block and if the line is not empty
            parts = line.split()
            if len(parts)>1: #check if there is a taxon name and a sequence
                taxon_name = parts[0]
                sequence = parts[1]
                seq_len = len(sequence)
                print(f"Line {line_num + 1}: {taxon_name} - Length: {seq_len}")
                if seq_len != 94: #check if the length is different from 94
                    print(f"WARNING: {taxon_name} has a length different from 94.")

# Example usage:
check_sequence_lengths("/Users/claudiucreanga/projects/Boundaries/output.nex")  # Replace with your file name