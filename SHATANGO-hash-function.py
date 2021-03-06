def knight(blocks,nonce):
    sponge = nonce
    for j in blocks:
        if isinstance(sponge,int): sponge ^= (sponge << 256) + j
        if isinstance(sponge,list): sponge.append(j)
        if isinstance(sponge,int): sponge = [int(d) for d in str(bin(sponge))[2:]]
        for z in sponge:
            z ^= j
    output = sponge
    while len(output)>1:
        output[1] ^= (output[0] >> abs(output[0]))
        del output[0]
    tag = output
    for j in blocks:
        for k in output: 
            if isinstance(j,int): 
                if isinstance(sponge,int): tag = ((k^j) << sponge) + tag
                if isinstance(sponge,list):
                    for s in sponge:
                        tag = ((k^j) << abs(s)) + tag
            if isinstance(j,list):
                for m in j:
                    if isinstance(sponge,list):
                        for s in sponge:
                            tag = ((k^m) << s) + tag
    return tag

def tango(state,rounds,nonce):
    bc = state
    for r in range(rounds):
        for i in range(4,nonce+4):
            bc.append(state[i]^(state[i-1]&state[i-2])^~(state[i-3]|state[i-4]))
            t = bc[(i+nonce-1) % nonce] ^ (bc[(i+nonce-4) % nonce]) << (nonce+3)**2
            for j in range(nonce**2):
                state[j+1] ^= t
        t = state[1]
        for i in range(nonce**2):
            j = knight(state,nonce << (nonce+3)**2)
            state[j] = t ^ j << (j+3)**2
        for j in range(nonce**2 + 1):
            for i in range(nonce):
                bc[i] = state[j+i]
                state[j+i] ^= (~bc[(i+1) % nonce]) & bc[(i+2) % nonce]
    state[0] ^= knight(r,nonce)
    return state

print(tango([2,2,2,2,2,2,2,2,2,2],5,3))
