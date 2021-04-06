from BitcoinMining import cored_miner
from multiprocessing import Process, Manager
from ast import literal_eval
from time import sleep
from time import time
import blockcypher
import subprocess
import binascii
import os
manager = Manager()
ans = manager.dict()
def Bitcoind():
    os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoind -prune=550 -wallet=PoeticDeath")
def dblsha(data):
 	return hashlib.sha256(hashlib.sha256(data).digest()).digest()
B = Process(target=Bitcoind)
B.start()
sleep(30)
try:
    while True:
        start = time()
        ans[1] = -1
        old_block = blockcypher.get_latest_block_hash()
        prev_block = old_block
        ver = 1
        s = subprocess.check_output("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli getmininginfo", shell=True)
        s = str(str(s)).replace("b\'", "")
        s = str(str(s)).replace("\'", "")
        s = str(str(s)).replace("\\n", "")
        s = literal_eval(s)
        r = subprocess.check_output("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli getblocktemplate {'\"rules\": [\"segwit\"]'}", shell=True)
        r = str(str(r)).replace("b\'", "")
        r = str(str(r)).replace("\'", "")
        r = str(str(r)).replace("\n", "")
        r = str(str(r)).replace("\\n", "")
        r = literal_eval(r)
        txnlist = [binascii.a2b_hex(a['data']) for a in r['transactions']]
        merklehashes = [dblsha(t) for t in txnlist]
        while len(merklehashes) > 1:
            if len(merklehashes) % 2:
                merklehashes.append(merklehashes[-1])
            merklehashes = [dblsha(merklehashes[i] + merklehashes[i + 1]) for i in range(0, len(merklehashes), 2)]
        mrkl_root = merklehashes[0]
        time_ = r['curtime']
        bits = r['bits']
        target_str = hex(s['difficulty'] * 2**(8*(0x1b -3)))[2:]
        while len(target_str) < 64:
            target_str = "0" + target_str
        target_str = int("0x" + target_str, 16)
        P = Process(target=cored_miner, args=(ans,))
        P.start()
        while prev_block == old_block:
            prev_block = blockcypher.get_latest_block_hash()
            if ans[1] != -1:
                os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli submitheader " + str("\"") + ans[1] + str("\""))
                print("Successfully solved block", str(blockcypher.get_latest_block_height(old_block)+1), "in", str(time() - start), "seconds.")
                break
        P.terminate()
        if ans[1] == -1:
            print("Didn't solve block", str(blockcypher.get_latest_block_height(old_block)+1), "in time, lasted", str(time() - start), "seconds.")
except KeyboardInterrupt:
    P.terminate()
    B.terminate()
    exit()
