from BitcoinMining import cored_miner
from multiprocessing import Process, Manager
from ast import literal_eval
from time import time
import blockcypher
import subprocess
import os
manager = Manager()
ans = manager.dict()
while True:
    ans[1] = -1
    old_block = blockcypher.get_latest_block_hash()
    prev_block = old_block
    ver = 1
    time_ = int(time())
    s = subprocess.check_output("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli getmininginfo", shell=True)
    s = str(str(s)).replace("b\'", "")
    s = str(str(s)).replace("\'", "")
    s = str(str(s)).replace("\\n", "")
    s = literal_eval(s)
    mrkl_root =
    target_str = hex(s['difficulty'] * 2**(8*(0x1b -3)))[2:]
    while len(target_str) < 64:
        target_str = "0" + target_str
    target_str = int("0x" + target_str, 16)
    bits = blockcypher.get_blockchain_overview(old_block)['bits']
    P = Process(target=cored_miner, args=(ans,))
    P.start()
    while prev_block == old_block:
        prev_block = blockcypher.get_latest_block_hash()
        if ans[1] != -1:
            os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli submitheader " + ans[1])
            break
    P.terminate()
