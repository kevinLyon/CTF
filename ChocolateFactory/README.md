# Chocolate Factory Resolução

![banner](https://i.imgur.com/rT335UA.png)

Como qualquer CTF vamos começar com um scan de portas:

![nmap](imagens/nmap.png)
![nmap2](imagens/nmap2.png)

Logo de cara recebemos muitas informações na tela, mas vamos por partes. <br>
Para começar dou uma olhada no serviço de FTP o NMAP Conseguiu fazer login com um usuário público, e nos mostra que ha uma foto no servidor FTP, vamos baixa-la.

![ftp](imagens/ftp.png)

Após baixa-la tento extrair algo com `steghide` consigo um arquivo `b64.txt` sem senha alguma, é possível fazer o decode do conteudo com `cat b64.txt | base64 -d`

![bs64](imagens/bs64.png)

Recebemos uma hash, próximo passo seria quebra a hash com o `john` ou `hashcat` <br>
Após a quebra da hash temos enfim uma senha:
![hash](imagens/hash.png)

Pelo formato do arquivo somos induzidos a pensar que a senha é de um usuário SSH, porém não temos sucesso com o login, agora que analisei tudo que era possível no FTP e em seus arquivos, vou para o sevidor Apache:

Logo de cara temos uma página de login, já temos uma credencial que não era de um SSH então vamos testar aqui:
![home](imagens/home.png)

sucesso, estamos logado, e de cara o site nos solicita um comando, podemos tentar um simples `ls`
![logged](imagens/logged.png)

![ls](imagens/ls.png)
>Temos um RCE (REMOTE CODE EXECUTION) confirmado.

A partir dai fica fácil pegar uma Revers shell, mas antes, ha um arquivo que me chama a atenção `key_rev_key`, este mesmo arquivo aparece no NMAP:
![key_rev](imagens/key_rev.png)

um simples `cat` neste arquivo já serve, porem podemos baixar em `http://< IP >/key_rev_key`, fica a escolha:
![myst](imagens/myst.png)

Temos uma nova *string* misteriosa, vamos guardá-la e partir para uma revers shell. <br>
Procurando um pouco pelo servidor podemos encontrar uma `id_rsa` que pode ser bem util para elevar um pouco nosso previlégio:

![id_rsa](imagens/id_rsa.png)
>* Lembrando que para utilizar uma chave rsa ela deve estar com as permissões certas.
>* `chmod 600 id_rsa` <br>
>* `ssh -i id_rsa user@ip`

Agora que temos um novo usuário, uma das primeiras coisas ha se fazer é dar uma olhada nas permissões :

![vi](imagens/vi-sudo.png)

Vemos que o usuário tem a permissões  de utilizar o `/usr/bin/vi` como root sem precisar de senhas e ao olharmos o site [GFTobins](https://gtfobins.github.io/) vemos que é bem fácil pegar uma shell como root utilizando o `vi`. <br>
Enfim chegamos na parte mais complicada do desafio, temos uma shell como root mas não temos a última flag e no `/root` temos um `root.py` que nos pede um uma key.
>Código fonte:
![root.py](imagens/root-py.png)

Tentei algumas palavras aleatórias mas percebi que não levaria a nada, o código fonte também não nos diz muita coisa, foi então que me lebrei da key dentro do arquivo `key_rev_key` ao olhar a key novamente percebi que a key tinha um `b'key'`, quem já tem o básico de python sabe que para transformar uma *string* em *bytes* basta passar um `b'string'` antes da *string* então porque não testar...
>key:

![key](imagens/key.png)

Sucesso temos nossa última flag:

![root-flag](imagens/root-flag.png)