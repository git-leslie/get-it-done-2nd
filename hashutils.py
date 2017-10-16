import hashlib
import random
import string


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])
    #random.choice(string)...is ascii table letters
    #randomly chooses and asci letter 5 times




def make_pw_hash(password, salt=None): #take pw, turn to hash, store in DB on user's account, instead of in plain text
    if not salt: #let user provide salt, but if they dont, make a random one
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password)).hexdigest()
    return '{0},{1}'.format(hash,salt)
    #return hashlib.sha256(str.encode(password)).hexdigest()


def check_pw_hash(password, hash): #verify users pw
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True
    else:
        return False