import socket
from time import sleep

from PIL import Image, ImageOps
from pyzbar.pyzbar import decode


ip = '172.18.4.3'
port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

print(client.recv(1024).decode())
client.send(b"Ok")

print("\n")
while 1:
    sleep(1)
    data_raw = client.recv(100000).decode()
    print(data_raw)
    data = data_raw.replace(" ", "").split(";")

    qrcode = Image.new("RGB", (len(data), len(data)))
    data.pop(-1)
    for l in range(len(data)):
        data[l] = data[l].split("),(")
        for j in range(len(data)):
            data[l][j] = tuple(map(int, data[l][j].replace("(", "").replace(")", "").split(",")))
            pixel = data[l][j]
            qrcode.putpixel((l, j), pixel)


    qrcode = ImageOps.expand(qrcode, border=3, fill="white")
    client.send(decode(qrcode)[0][0])


