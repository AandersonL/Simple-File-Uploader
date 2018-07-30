import random
import base64
import hashlib
import string




def gen_key():
    # Generate 256 random bits
    rand_bits = str(random.getrandbits(256)).encode()
    # Use a sha256 hash function to generate a key
    hash_key = hashlib.sha256(rand_bits).digest()
    # Parse base64 in random choice
    rand_choice = random.choice(['aa','eF', 'eK','jj', 'kJ']).encode()
    key_b64 = base64.b64encode(hash_key, rand_choice).decode()


    key_b64 = key_b64.strip('=')
    # fix the length
    letters = string.ascii_letters
    letters_num = len(letters) - 1

    while len(key_b64) % 4 != 0:
        key_b64 += letters[random.randint(0, letters_num)]

    # Finally, split the string to use correctly
    
    api_key = '-'.join([''.join(x) for x in zip(*[iter(key_b64)]*4)])

    return api_key




if __name__ == '__main__':
    print(gen_key())

