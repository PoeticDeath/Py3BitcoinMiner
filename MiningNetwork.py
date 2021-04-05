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
    bits =
    target_str =
    P = Process(target=cored_miner, args=(ans,))
    P.start()
    while prev_block == old_block:
        prev_block = blockcypher.get_latest_block_hash()
        if ans[1] != -1:
            os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli submitblock " + ans[1])
            break
    P.terminate()
