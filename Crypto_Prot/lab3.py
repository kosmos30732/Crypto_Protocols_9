import hashlib
import random
from Crypto.Util import number

SIZE = 1024


def random_bitstring(m):
    bitstring = "1" + "".join(random.choice("01") for _ in range(m-1))
    return bitstring


def gen_p_q():
    # размерность q = m
    m = SIZE // 2
    # размерность p = L
    L = SIZE
    _L = int(-1 * (L / 160) // 1 * -1)
    _m = int(-1 * (m / 160) // 1 * -1)
    _N = int(-1 * (L / 1024) // 1 * -1)
    while True:
        seed = random_bitstring(m)
        U = 0
        for i in range(0, _m):
            tmp1 = hashlib.sha1((bin(int(seed, 2) + i)[2:]).encode()).hexdigest()
            tmp2 = hashlib.sha1(
                (bin((int(seed, 2) + i + _m) % (pow(2, m + 1)))[2:]).encode()
            ).hexdigest()
            U += (int(tmp1, 16) ^ int(tmp2, 16)) * pow(2, 160 * i)
        U = U % (pow(2, m))
        q = U | pow(2, m - 1) | 1
        if number.isPrime(q) == True:
            break
    counter = 0
    while True:
        R = int(seed, 2) + 2 * _m + _L * counter
        V = 0
        for i in range(0, _L):
            V += int(hashlib.sha1((bin(R + i)[2:]).encode()).hexdigest(), 16) * pow(
                2, 160 * i
            )
        W = V % (pow(2, L))
        X = W | pow(2, L - 1)
        p = X - (X % (2 * q)) + 1
        if p > pow(2, L - 1) and number.isPrime(p) == True:
            return p, q
        counter += 1
        if counter == (4096 * _N):
            return None


def gen_g(p, q):
    j = (p - 1) // q
    while True:
        h = random.randint(2, p - 2)
        g = pow(h, j, p)
        if g != 1:
            return g


p, q = gen_p_q()
if p == None:
    exit(1)
g = gen_g(p, q)
# print(f"Сторона А сгенерировала:\n\tp={hex(p)}\n\tg={hex(g)}\n")

secret_key_A = number.getRandomInteger(SIZE)
#assert(secret_key_A>2 and secret_key_A<p-1)
#assert(pow(secret_key_A,q,p)==1)
#assert()
public_key_A = pow(g, secret_key_A, p)
public_key_A+=12131
print(
    f"А сгенерировала секретный ключ\n\tSecret key A={hex(secret_key_A)}\nИ отправляет стороне В публичный ключ, а также p и g:\n\tPublic key={hex(public_key_A)}\n\tp={hex(p)}\n\tg={hex(g)}\n"
)

secret_key_B = number.getRandomInteger(SIZE)
public_key_B = pow(g, secret_key_B, p)
#public_key_B+=123123
print(
    f"B сгенерировала секретный ключ\n\tSecret key A={hex(secret_key_B)}\nИ отправляет стороне A публичный ключ\n\tPublic key={hex(public_key_B)}\n"
)
secret_sb = pow(public_key_A, secret_key_B, p)
print(f"B получила общий секретный ключ\n\tSecret={hex(secret_sb)}")

secret_sa = pow(public_key_B, secret_key_A, p)
print(f"A получила общий секретный ключ\n\tSecret={hex(secret_sa)}")
print(f"Общий ключ равен на сторонах: {secret_sa==secret_sb}")