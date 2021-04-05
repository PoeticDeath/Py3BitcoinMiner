from BitcoinMining import cored_miner
from multiprocessing import Process, Manager
from ast import literal_eval
from time import time
import blockcypher
import subprocess
import os
manager = Manager()
ans = manager.dict()
def Bitcoind():
    os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoind -prune=550 -wallet=PoeticDeath")
B = Process(target=Bitcoind)
B.start()
try:
    while True:
        start = time()
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
                print("Successfully solved block", str(blockcypher.get_latest_block_height(old_block)+1), "in", str(time() - start), "seconds.")
                break
        P.terminate()
        if ans[1] == -1:
            print("Didn't solve block", str(blockcypher.get_latest_block_height(old_block)+1), "in time, lasted", str(time() - start), "seconds.")
except:
    B.terminate()
    exit()
