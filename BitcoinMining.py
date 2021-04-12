def mine(start, cores, ans, ver, prev_block, mrkl_root, time_, bits, target_str):
    try:
        import hashlib, struct
        nonce = start
        while True:
            while nonce % 2**32 != 0:
                while nonce % 10000 != 0:
                    if hashlib.sha256(hashlib.sha256(( struct.pack("<L", ver) + bytes.fromhex(prev_block)[::-1] + bytes.fromhex(mrkl_root)[::-1] + struct.pack("<LLL", time_, bits, nonce))).digest()).digest()[::-1] < target_str:
                        ans[1] = nonce
                        ans[2] = ( struct.pack("<L", ver) + bytes.fromhex(prev_block)[::-1] + bytes.fromhex(mrkl_root)[::-1] + struct.pack("<LLL", time_, bits, nonce))
                        return
                    nonce += cores
                if ans[1] and ans[2] == 0:
                    exit()
                if hashlib.sha256(hashlib.sha256(( struct.pack("<L", ver) + bytes.fromhex(prev_block)[::-1] + bytes.fromhex(mrkl_root)[::-1] + struct.pack("<LLL", time_, bits, nonce))).digest()).digest()[::-1] < target_str:
                    ans[1] = nonce
                    ans[2] = ( struct.pack("<L", ver) + bytes.fromhex(prev_block)[::-1] + bytes.fromhex(mrkl_root)[::-1] + struct.pack("<LLL", time_, bits, nonce))
                    return
                nonce += cores
            ver += 1
    except KeyboardInterrupt:
        exit()
def cored_miner(ans, ver, prev_block, mrkl_root, time_, bits, target_str):
    from time import time, sleep
    from multiprocessing import Process
    from psutil import cpu_count
    start = time()
    n = 0
    while n <= cpu_count():
        Process(target=mine, args=(n, cpu_count(), ans, ver, prev_block, mrkl_root, time_, bits, target_str,), daemon=True).start()
        n += 1
    while ans[1] == -1:
        if ans[1] and ans[2] == 0:
            sleep(5)
            exit()
        pass
    end = time()
