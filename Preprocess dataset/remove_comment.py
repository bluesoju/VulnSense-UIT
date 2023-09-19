import re
import os
import shutil


def remove_comment(inputFile, outputFile):
    with open(inputFile, 'r', encoding="utf-8") as f:
        source_code = f.read()
    #fdw = open(outputFile, 'w', encoding="utf-8")
    
    source_code = re.sub(r"//\*.*", "", source_code)
    source_code = re.sub(r"#.*", "", source_code)
    # Remove multi-line comments
    source_code = re.sub(r"/\*.*?\*/", "", source_code, flags=re.DOTALL)
    source_code = re.sub(r"\"\"\".*?\"\"\"/", "", source_code, flags=re.DOTALL)
    
    source_code = re.sub(r"//.*", "", source_code)

    # Remove redundant spaces and tabs
    source_code = re.sub(r"[\t ]+", " ", source_code)

    # Remove empty lines
    source_code = re.sub(r"^\s*\n", "", source_code, flags=re.MULTILINE)

    with open(outputFile, 'w', encoding="utf-8") as fdw:
        fdw.write(source_code)


vulns = ['clean', 'ari', 'reentrancy']
for vuln in vulns:
    files = os.listdir(vuln)
    for file in files:
        inputfile = os.path.join(vuln, file)
        if (vuln == 'ari'):
          outputfile = os.path.join('preprocess', 'arithmetic', file)
        else:
          outputfile = os.path.join('preprocess', vuln, file)
        remove_comment(inputfile, outputfile)
