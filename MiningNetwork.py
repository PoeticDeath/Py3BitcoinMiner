from RandomBitcoinMining import cored_miner as random_cored_miner
from BitcoinMining import cored_miner
from multiprocessing import Process, Manager
from ast import literal_eval
from time import sleep
from time import time
import blockcypher
import subprocess
import binascii
import hashlib, struct
import os
manager = Manager()
ans = manager.dict()
def Bitcoind():
    os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoind -prune=550 -wallet=PoeticDeath")
def dblsha(data):
 	return hashlib.sha256(hashlib.sha256(data).digest()).digest()
def varintEncode(n):
    if n < 0xfd:
        return struct.pack('<B', n)
    return b'\xfd' + struct.pack('<H', n)
B = Process(target=Bitcoind)
B.start()
sleep(30)
try:
    while True:
        start = time()
        ans[1] = -1
        ans[2] = -1
        ans[3] = -1
        ans[4] = -1
        s = subprocess.check_output("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli getmininginfo", shell=True)
        s = str(s).replace("b\'", "")
        s = str(s).replace("\'", "")
        s = str(s).replace("\\n", "")
        s = literal_eval(s)
        r = subprocess.check_output("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli getblocktemplate {'\"rules\": [\"segwit\"]'}", shell=True)
        r = str(r).replace("b\'", "")
        r = str(r).replace("\'", "")
        r = str(r).replace("\n", "")
        r = str(r).replace("\\n", "")
        r = literal_eval(r)
        txnlist = [binascii.a2b_hex(a['data']) for a in r['transactions']]
        merklehashes = [dblsha(t) for t in txnlist]
        while len(merklehashes) > 1:
            if len(merklehashes) % 2:
                merklehashes.append(merklehashes[-1])
            merklehashes = [dblsha(merklehashes[i] + merklehashes[i + 1]) for i in range(0, len(merklehashes), 2)]
        mrkl_root = str(hex(int().from_bytes(merklehashes[0], byteorder='big'))).replace("0x", "")
        time_ = r['curtime']
        bits = int(str(r['bits']), 16)
        exp = bits >> 24
        mant = bits & 0xffffff
        target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
        target_str = bytes.fromhex(target_hexstr)
        old_block = r['height']
        ol_block = old_block
        prev_block = r['previousblockhash']
        ver = r['version']
        #print(ver, prev_block, mrkl_root, time_, bits, target_str)
        PS = Process(target=cored_miner, args=(ans, ver, prev_block, mrkl_root, time_, bits, target_str,))
        PS.start()
        PR = Process(target=random_cored_miner, args=(ans, ver, prev_block, mrkl_root, time_, bits, target_str,))
        PR.start()
        while ol_block == old_block:
            n = subprocess.check_output("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli getblocktemplate {'\"rules\": [\"segwit\"]'}", shell=True)
            n = str(n).replace("b\'", "")
            n = str(n).replace("\'", "")
            n = str(n).replace("\n", "")
            n = str(n).replace("\\n", "")
            n = literal_eval(n)
            ol_block = n['height']
            if ans[2] != -1:
                blkdata = ans[2].hex() + varintEncode(len(r['transactions'])).hex()
                if 'submit/coinbase' not in r['mutable']:
                    for txn in txnlist[1:]:
                        blkdata += txn.hex()
                print("\n", blkdata, "\n")
                os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli submitblock " + str("\"") + blkdata + str("\""))
                print("Successfully solved block", str(r['height']), "in", str(time() - start), "seconds.")
                break
            if ans[4] != -1:
                blkdata = ans[4].hex() + varintEncode(len(r['transactions'])).hex()
                if 'submit/coinbase' not in r['mutable']:
                    for txn in txnlist[1:]:
                        blkdata += txn.hex()
                print("\n", blkdata, "\n")
                os.system("/Programs/Bitcoin/bitcoin-0.21.0/bin/bitcoin-cli submitblock " + str("\"") + blkdata + str("\""))
                print("Successfully solved block", str(r['height']), "in", str(time() - start), "seconds.")
                break
        if ans[1] and ans[2] and ans[3] and ans[4] == -1:
            print("Didn't solve block", str(r['height']), "in time, lasted", str(time() - start), "seconds.")
            ans[1] = ans[2] = ans[3] = ans[4] = 0
        sleep(10)
        PS.terminate()
        PR.terminate()
except KeyboardInterrupt:
    ans[1] = ans[2] = ans[3] = ans[4] = 0
    sleep(10)
    PS.terminate()
    PR.terminate()
    B.terminate()
    exit()
