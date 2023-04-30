# Começando as aventuras

Primeiro desafio da CTF de 2019!

Espero ajudar iniciantes com este projeto, lembrando que estes repositórios são um complemento explicativo aos vídeos disponíveis em meu canal, Divirtam-se :) !

[![Youtube Badge](https://img.shields.io/badge/-Youtube-red)](https://www.youtube.com/channel/UC9tSm6hsH2c5atpEObIaD8Q)

# Arquivos

Os arquivos coletados ou criados durante o desafio também estarão disponíveis.

## Coletando informações
Como qualquer Pentest seja em uma CTF ou em uma bug bounty a primeira coisa a se fazer é escanear as portas do alvo, para saber o que seu alvo esta rodando

![nmap](https://github.com/kevinLyon/CTF-Solyd_2019/blob/main/Come%C3%A7ando-suas-Aventuras/Imagens/nmap.jpg)

Como podemos ver o alvo contem as portas [21, 22, 80] abertas
A primeira coisa que gosto de fazer é olhar a porta 80 que no caso seria uma aplicação web.

Ao abrirmos vemos um site bem simples:

![site](Imagens/olhando_site.jpg)

O mesmo com o Source:
![html](Imagens/html.jpg)

Como o site era simples de mais, sem nenhuma informação útil, decido dar uma olhada na porta 21 que no caso esta rodando um protocolo FTP.
Porem isso não é tudo, como podemos ver no scan que fiz do NMAP ele nos diz que há um usuário (anonymous) 

[Mais informações sobre usuários Anonymous](http://penta2.ufrgs.br/Roseclea/anonymous.html)
![anonymous](Imagens/anonymous.jpg)

Apos nos conectarmos com o usuário anonymous encontramos um arquivo oculto contendo nossa primeira FLAG e informações muito interessantes:
![img](Imagens/pluginn.jpg)

Após um simples Brute force de diretórios em nosso alvo encontramos o site wordpress que aviam mencionado:
![wordpress](Imagens/wordpress.jpg)

__Infelizmente tive vários problemas com a gravação deste desafio a imagem a seguir se trata de um scan que fiz com o Wpscan__ [Mais informações sobre Wpscan](https://wpscan.com/wordpress-security-scanner).
 Com nosso scan pronto encontramos um plugin com varias vulnerabilidades já descobertas:
![vul](Imagens/vul.jpg)

Com uma breve pesquisa descobrimos que o mesmo plugin contem uma vulnerabilidade de SQL injection:
![exploit](Imagens/exploit.jpg)

# Exploração

Após uma longa faze de captura de informações passamos a explorar o Exploit, onde conseguimos fazer o dump do banco de dados, junto com nossa segunda FLAG:
[Mais informações sobre SQLmap](http://sqlmap.org/)

__NOTA: A gravação da exploração também foi corrompida, a exploração completa do SQLI levou quase 4 horas, por isso há apenas algumas partes no video!__
![sql](Imagens/sql.jpg)

Apos o crack da senha do estagiário conseguimos um login no site, e por sorte nosso estagiário dissídio que seria uma boa deixar a mesma senha em seu SSH, por tanto ao quebrar a hash tínhamos um login no site com permissão ADMIN e um login no SSH:
![ssh](Imagens/ssh.jpg)

Após uma breve exploração no servidor achamos varias informações e nossa terceira FLAG, faltando apenas uma:
![flag](Imagens/flag.jpg)

Mais um pouco de exploração e encontramos os arquivos de usuários e senhas(passwd/shadow),
que nos permitira fazer um Brut force na senha do usuário ROOT, porem é algo que complica muito pois dificilmente um usuário ROOT teria uma senha fraca:
![shadow](Imagens/shadow.jpg)

Graças a uma chave RSA copiada junta com o backup conseguimos nossa tão aguardada escalação de privilégio :):

[Mais sobre chave RSA](https://cloud.ibm.com/docs/ssh-keys?topic=ssh-keys-generating-and-using-ssh-keys-for-remote-host-authentication&locale=pt-BR)

![rsa](Imagens/rsa.jpg)

Ai ficou fácil pegar nossa última FLAG:
![fim](Imagens/fim.jpg)

# Espero que tenham gostado e aprendido com nosso primeiro desafio :)
