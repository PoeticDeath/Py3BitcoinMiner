def mine(ans, cur):
    try:
        from random import randint
        import hashlib, struct
        nonce = randint(0, 4294967297)
        count = 0
        while ans[1] == -1:
            header = ( struct.pack("<L", ver) + bytes.fromhex(prev_block)[::-1] + bytes.fromhex(mrkl_root)[::-1] + struct.pack("<LLL", time_, bits, nonce))
            hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
            cur[1] = nonce
            cur[2] = count
            if hash[::-1] < target_str:
                ans[1] = nonce
            nonce = randint(0, 4294967297)
            count += 1
    except:
        exit()
def cored_miner():
    from time import time
    from multiprocessing import Process, Manager
    from psutil import cpu_count
    manager = Manager()
    ans = manager.dict()
    cur = manager.dict()
    ans[1] = -1
    cur[1] = 0
    cur[2] = 0
    start = time()
    Process(target=mine, args=(ans, cur,)).start()
    while ans[1] == -1:
        print(f'{cur[1]:,}' + ' ' + f'{cur[2]:,}', f'{int(cur[2] / (time() - start)):,}', 'H/s  ' , end='\r')
    end = time()
    print("It took " + str(end - start) + " seconds to mine the block.")
if __name__ == '__main__':
    ver = 2
    prev_block = "000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717"
    mrkl_root = "871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a"
    time_ = 0x53058b35 # 2014-02-20 04:57:25
    bits = 0x19015f53 # https://en.bitcoin.it/wiki/Difficulty
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    target_str = bytes.fromhex(target_hexstr)
    cored_miner()
    #while True:
    #    cored_miner()
