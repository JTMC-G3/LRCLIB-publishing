
import hashlib

def verify_nonce(hashed, target):
    if len(hashed) != len(target):
        return False
    
    for i in range(len(hashed)):
        if hashed[i] < target[i]:
            return True
        elif hashed[i] > target[i]:
            return False
    
    return True

def solve_challenge(prefix, target_hex):
    nonce = 0
    target = bytes.fromhex(target_hex)
    
    while True:
        input_str = f"{prefix}{nonce}"
        hashed = hashlib.sha256(input_str.encode()).digest()
        
        if verify_nonce(hashed, target):
            return str(nonce)
        else:
            nonce += 1

