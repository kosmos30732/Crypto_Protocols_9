import socket

SERVER_HOST = "127.0.0.1"
ALICE_PORT = 1234
BOB_PORT = 1235


def check_yolter(K, g, p, X, Y, M):
    if (pow(K, X, p) * pow(X, Y, p)) % p == pow(g, M, p):
        return True
    return False


def wait_alice_msg():
    from_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    from_alice.bind((SERVER_HOST, ALICE_PORT))
    from_alice.listen()
    print(f"Уолтер ждет сообщение от Алисы...\n")
    alice_client, addr = from_alice.accept()
    print(f"Алиса подключилась: {addr}\n")
    data = alice_client.recv(1024).decode()
    K = int(data.split(" ")[0])
    g = int(data.split(" ")[1])
    p = int(data.split(" ")[2])
    X = int(data.split(" ")[3])
    Y = int(data.split(" ")[4])
    M = int(data.split(" ")[5])
    alice_client.close()
    from_alice.close()
    return K, g, p, X, Y, M


def send_to_bob(K, g, p, X, Y, M):
    to_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    to_bob.connect((SERVER_HOST, BOB_PORT))
    to_bob.send(f"{K} {g} {p} {X} {Y} {M}".encode())
    to_bob.close()


while True:
    K, g, p, X, Y, M = wait_alice_msg()
    print(f"Уолтер принял от Алисы:")
    print(
        f"Открытый ключ:\n\tK={K}\n\tg={g}\n\tp={p}\nПодпись Эль-Гамаля:\n\tX={X}\n\tY={Y}\nИ само сообщение:\n\tM={M}\n"
    )
    print(f"Уолтер проверяет подпись Эль-Гамаля")
    print(f"Уолтер проверил, верна ли подпись Эль-Гамаля: {check_yolter(K,g,p,X,Y,M)}")
    send_to_bob(K, g, p, X, Y, M)
    input()
