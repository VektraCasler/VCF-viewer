import os
import re
import io

FOLDER = 'reference'
FILENAME = 'infotrack_data_dump_cleaned.tsv'

file_path = os.path.join(FOLDER, FILENAME)

with open(file_path, 'r', 'ascii') as file_input:
    lines = file_input.readlines()

# time to process the lines individually
for line in lines:
    chunks = line.split('\t')
    print(chunks)
    quit()
