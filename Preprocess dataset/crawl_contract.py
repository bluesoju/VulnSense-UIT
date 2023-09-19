import json
from collections import Counter
import requests

with open("results_wild.json") as f:
    data = json.load(f)

contract_name = list(data.keys())

dataset = dict()

def get_source_code_2_file(address, vuln):
    r = requests.get(f'https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey=II5M5BPF2DJNW5Y3WZKZJV6N7HCSUJ4UNZ')
    cc = r.text
    res = json.loads(cc)
    source = res['result'][0]['SourceCode']

    with open(f'{vuln}/{address}.sol', 'w', encoding='utf-8') as f:
        f.write(source)


for contract in contract_name:
    nb_re = 0
    nb_time = 0
    nb_clean = 0
    tools_name = list(data[contract]['tools'].keys())
    for tool in tools_name:
        vuln_in_contract = list(data[contract]['tools'][tool]["categories"].keys())
        if "reentrancy" in vuln_in_contract:
            nb_re = nb_re + 1
        elif "time_manipulation" in vuln_in_contract:
            nb_time = nb_time + 1
        elif len(vuln_in_contract) == 0:
            nb_clean = nb_clean + 1

    if nb_re > 1 and nb_time == 0:
        dataset[contract] = 'reentrancy'
        get_source_code_2_file(contract, 'reentrancy')
    elif nb_time > 1 and nb_re == 0:
        dataset[contract] = 'timestamp'
        get_source_code_2_file(contract, 'timestamp')
    elif nb_clean == len(tools_name):
        dataset[contract] = 'clean'
        get_source_code_2_file(contract, 'clean')
