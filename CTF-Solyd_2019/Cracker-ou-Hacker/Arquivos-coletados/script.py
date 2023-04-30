###############################
# Desenvolvido pro Blakc Mask #
#        for study            #
###############################
import socket
from time import sleep
import re


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target = ('172.18.1.3', 50123)
client.connect(target)

sleep(1)
data_rec = client.recv(2024).decode()

proc = re.findall(r'\d+', data_rec)

str_for_int = []
soma = 0
for number in proc:
   n = int(number)
   soma += n
   str_for_int.append(n)

encode = bytes(soma)

client.sendall(encode)
recv = client.recv(2024).decode()
print(recv)
