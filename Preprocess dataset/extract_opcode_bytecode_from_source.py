from solcx import compile_standard, install_solc
import json
import re
import os
import csv
import pandas as pd

def getVersionPragma(filename):                     # param la path cua contract          
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    for line in data:                               # duyet tung dong trong contract do
        if 'pragma' in line and 'solidity' in line:                        # neu dong do chua chu "pragma"
            temp = line.split()                     # chuyen dong do thanh list ['pragma', 'solidity', '^0.4.19;']
            if len(temp) == 3 and temp[2][0].isnumeric() == True:       # ['pragma', 'solidity', '0.4.19;']
                return temp[2][0:-1]
            elif len(temp) == 3 and temp[2][1].isnumeric() == True:       # ['pragma', 'solidity', '^0.4.19;']
                return temp[2][1:-1]
            elif len(temp) == 3 and temp[2][1].isnumeric() == False:    # ['pragma', 'solidity', '<=0.4.19;']
                return temp[2][2:-1]
            elif len(temp) > 3 and len(temp[2]) == 1:
                return temp[2][-1]
            elif len(temp) == 4 and temp[2][1].isnumeric() == True:      # ['pragma', 'solidity', '>0.4.22', '<0.6.0]
                return temp[2][1:]
            elif len(temp) == 4 and temp[2][1].isnumeric() == False:     # ['pragma', 'solidity', '>=0.4.22', '<0.6.0]
                return '0.5.0'
    return '0.4.22'

def clean_opcode(opcode_str):
    # remove hex characters (0x..)
    opcode_str = re.sub(r'0x[a-fA-F0-9]+', '', opcode_str)
    
    # remove newline characters
    opcode_str = opcode_str.replace('\n', ' ')
    
    # extract only the opcode names
    opcodes = re.findall(r'[A-Z]+', opcode_str)
    
    return opcodes

def get_bytecode(regex, bytecode):
    cc = bytecode.split(regex)
    bytecode = ''.join(cc)
    match = re.findall(r"__.{1,50}_", bytecode)
    if len(match) != 0:
        bytecode = get_bytecode(match[0], bytecode)
        return bytecode
    else:
        return bytecode

def return_source_code(file_path):
    with open(file_path,"r", encoding='utf-8') as f:
        content = f.read()
    return content

def return_bytecode_opcode(file, file_path):
    with open (file_path, "r", encoding='utf-8') as f:
        content = f.read()

    version = getVersionPragma(file_path)
    print(version)
    try:
        install_solc(version)
    except:
        version = '0.4.11'
        install_solc(version)
    print(file)
    try:
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {'cc': {"content": content}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["evm.bytecode.opcodes", "metadata", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version=version,
        )
    except:
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {'cc': {"content": content}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["evm.bytecode.opcodes", "metadata", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version='0.4.24',
        )

    contracts_name = compiled_sol["contracts"]['cc'].keys()
    list_opcode = []
    list_bytecode = []
    for contract in contracts_name:
        bytecode = compiled_sol["contracts"]["cc"][contract]["evm"]["bytecode"]["object"]
        opcode = compiled_sol["contracts"]["cc"][contract]["evm"]["bytecode"]["opcodes"]
        
        
        match = re.findall(r"__.{1,50}_", bytecode)
        if len(match) != 0:
            bytecode = get_bytecode(match[0], bytecode)

        list_bytecode.append(bytecode)
        list_opcode.append(opcode)
    
    final_bytecode = ''.join(list_bytecode)
    final_opcode = ''.join(list_opcode)
    final_opcode = clean_opcode(final_opcode)
    final_opcode = ''.join(list_opcode)

    return final_bytecode, final_opcode

header = ['name', 'arithmetic', 'clean', 'reentrancy', 'bytecode', 'opcode', 'source_code']
rows = []

root_path = 'preprocess'
vulns = ['arithmetic', 'clean', 'reentrancy']

flag = 0
for vuln in vulns:
    files = os.listdir(vuln)
    for file in files:
        if file == '0xdfc328c19c8de45ac0117f836646378c10e0cda3.sol':
        #     flag = 1
        # if flag == 1:
            file_path = os.path.join(vuln, file)
            bytecode , opcode = return_bytecode_opcode(file, file_path)
            source_code = return_source_code(os.path.join(root_path, vuln, file))
            if vuln == 'arithmetic':
                row = [file, '1', '0', '0', bytecode, opcode, source_code]
            elif vuln == 'clean':
                row = [file, '0', '1', '0', bytecode, opcode, source_code]
            elif vuln == 'reentrancy':
                row = [file, '0', '0', '1', bytecode, opcode, source_code]
            
            rows.append(row)

            outfile_bytecode = os.path.join('bytecode', vuln, file)
            with open(outfile_bytecode, 'w', encoding='utf-8') as f:
                f.write(bytecode)
            outfile_opcode = os.path.join('opcode', vuln, file)
            with open(outfile_opcode, 'w', encoding='utf-8') as f:
                f.write(opcode)
            print(row)
        

# out_file_csv = r'D:\OneDrive - Trường ĐH CNTT - University of Information Technology\UIT\DACN\Dataset\dataset_multimodal_arithmetic_clean_reentrancy_BOS_no1.csv'

# df = pd.DataFrame(rows, columns=header)
# df.to_csv(out_file_csv, index=False)
# with open(out_file_csv, 'w', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     # write the header
#     writer.writerow(header)

#     # write multiple rows
#     writer.writerows(rows)