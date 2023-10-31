import socket

SERVER_HOST = "127.0.0.1"
BOB_PORT = 1235


def check_bob(r, g, p, X, Y, M):
    if (pow(pow(g, r, p), X, p) * pow(X, Y, p)) % p == pow(g, M, p):
        return True
    return False


def decrypt_message(p, r, X, Y, M):
    secret_msg = pow(pow(Y, -1, p - 1) * (M - r * X), 1, p - 1)
    return secret_msg


def wait_from_yolter():
    from_yolter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    from_yolter.bind((SERVER_HOST, BOB_PORT))
    from_yolter.listen()
    print(f"Боб ждет сообщение от Уолтера от Алисы...\n")
    yolter_client, addr = from_yolter.accept()
    print(f"Уолтер подключился: {addr}\n")
    data = yolter_client.recv(1024).decode()
    K = int(data.split(" ")[0])
    g = int(data.split(" ")[1])
    p = int(data.split(" ")[2])
    X = int(data.split(" ")[3])
    Y = int(data.split(" ")[4])
    M = int(data.split(" ")[5])
    yolter_client.close()
    from_yolter.close()
    return K, g, p, X, Y, M


while True:
    r = int(input("Введите закрытый ключ от Алисы r="))
    K, g, p, X, Y, M = wait_from_yolter()
    print(f"Боб принял от Уолтера:")
    print(
        f"Открытый ключ:\n\tK={K}\n\tg={g}\n\tp={p}\nПодпись Эль-Гамаля:\n\tX={X}\n\tY={Y}\nИ само сообщение:\n\tM={M}\n"
    )
    print(
        f"Боб удеждается что сообщение точно от Алисы и Уолтер его не подделал: {check_bob(r,g,p,X,Y,M)}"
    )
    secret_msg = decrypt_message(p, r, X, Y, M)
    print(f"Боб достает секретное сообщение: {secret_msg}\n")
    input()