import random
import math
import sympy
import socket
from Crypto.Util import number

SIZE = 128
SERVER_HOST = "127.0.0.1"
YOLTER_PORT = 1234


def generat_keys(secret_msg):
    while True:
        try:
            p, g, K, M = generate_keys(secret_msg)
            if p < secret_msg:
                continue
            X, Y = encrypt_message(p, g, r, secret_msg, M)
            decrypt_message(p, r, X, Y, M)
        except ValueError:
            pass
        else:
            return p, g, K, M


def find_primitive_root(prime):
    fact = sympy.factorint(prime - 1)
    for g in range(2, prime):
        ok = True
        for i in fact.keys():
            if pow(g, int((prime - 1) / i), prime) == 1:
                ok = False
                break
        if ok:
            return g
    return None


def generate_keys(secret_msg):
    g = 0
    while True:
        p = number.getPrime(SIZE)  # Генерируем большое простое число p
        primitive_root = find_primitive_root(p)
        if (
            math.gcd(secret_msg, p - 1) == 1
            and math.gcd(secret_msg, p) == 1
            and (primitive_root is not None)
        ):
            g = primitive_root
            break
    K = pow(g, r, p)  # Открытый ключ K
    while True:
        M = random.randint(2, p - 2)
        if math.gcd(M, p) == 1:
            break
    return p, g, K, M


def encrypt_message(p, g, r, secret_msg, M):
    X = pow(g, secret_msg, p)
    Y = ((M - r * X) * pow(secret_msg, -1, p - 1)) % (p - 1)
    return X, Y


def decrypt_message(p, r, X, Y, M):
    secret_msg = pow(pow(Y, -1, p - 1) * (M - r * X), 1, p - 1)
    return secret_msg


while True:
    # Закрытый ключ r
    r = number.getPrime(SIZE // 2)
    print(f"Алиса сообщает Бобу секретный ключ r\n\tr={r}")
    # Скрытое сообщение
    secret_msg = int(input("Введите сообщение для отправки Бобу: "))
    if secret_msg % 2 == 0:
        print(f"Только нечетное, попробуйте еще раз\n")
        continue
    p, g, K, M = generat_keys(secret_msg)
    X, Y = encrypt_message(p, g, r, secret_msg, M)
    print(
        f"\nАлиса отправляет Бобу через Уолтера подписанное сообщение, подпись и открытый ключ"
    )
    print(
        f"Открытый ключ:\n\tK={K}\n\tg={g}\n\tp={p}\nПодпись Эль-Гамаля:\n\tX={X}\n\tY={Y}\nИ само сообщение:\n\tM={M}\n"
    )
    to_yolter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    to_yolter.connect((SERVER_HOST, YOLTER_PORT))
    to_yolter.send(f"{K} {g} {p} {X} {Y} {M}".encode())
    to_yolter.close()
    input()