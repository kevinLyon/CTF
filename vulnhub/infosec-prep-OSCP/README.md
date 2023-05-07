<div style="text-align: center;">

## Está maquina foi cirada por FalconSpy com o intuito de se preparar para OSCP

</div>


<div style="text-align: center;">

### Enumerando

</div>

<p style="margin-top: 10px">
Temos um novo alvo, como de costume não temos qualquer informação sobre sobre tal.</br>
Um bom começo é enumerar suas portas para descobrir com o que estamos lidando
</p>

![nmap](oscp\images\nmap.PNG "nmap scan")
>Neste ponto vale resaltar que foi feito um scan em todas as 65535 portas e de cara vemos o mysql rodando em um porta alta, por este motivo sempre preso por rodar um scan em todas as portas possíveis.

<p>
Agora que temos uma boa noção do que está rodando, vou direto para a porta 80, em busca de um vetor de ataque facíl, afinal estamos falando da OSCP, uma prova com duração de 24h além de exaustante cada minuto pode contar.
</p>



<div style="text-align: center;">

### Enumerando o site

</div>

<div style="text-align: center;">

![banner](oscp\images\banner.png "banner")

</div>

<p>
Como não sou muito fã de scaner de vulnerabilidade ou de ir direto para força bruta, a primeira coisa que faço é abir o Burp suite e navegar pelo site, assim gerando tráfego o suficiente para analize.<br>
Em meio a navegação testo o famoso "robots.txt" e temos algo interessante no retorno
</p>

>O arquivo do Burp vai estar disponível para download nesta seção.

<div style="text-align: center;">

![banner](oscp\images\robot.png "banner")
![banner](oscp\images\secret.png "banner")
</div>

<p>
Ao ir atrás desse diretório vemos que não esta vazio e para nossa alegria parece se tratar de algo que foi empacotado com base64
</p>

<div style="text-align: center;">

![banner](oscp\images\base64.png "banner")
</div>

<p>
Por fim eu estava certo, e a surpresa foi melhor do que o esperado pois agora temos uma chave privada RSA</br>
Mas antes de ir para o SSH e tentar uma conexão preferi terminar minha lição de casa e ver o resto do site
</p>

<p>
Ainda com o Burp, analizando o comportamento do site encontrei mais algumas falhas.
Vamos começar pelo painel de login adiministrador que foi uma das mais critícas, de cara temos um painel desprotegido, ou seja qualquer usuário pode acessar o painel de adiministração sem muito esforço, além disso o painel não tinha qualquer criptografia TLS, neste caso pensando em uma cenário que o atacante estivesse na sua LAN, basta ter paciência que uma hora a senha do adiministrador ia passar por nossos olhos.<br>
Além destes problemas o painel continha uma vulnerabilidade que permitia enumerar todos os usuários.
</p>

<div style="text-align: center;">

![banner](oscp\images\admin.png "banner")
</div>

<p>
Caso o atacante não estivesse com paciênsia para enumerar os usuários por forca bruta ainda havia mais uma falha, esta já é conhecida pelo comunidade por se tratar de uma falha no wordpress que já teve sua correção.
Uma explicação rápida no meio das chamadas de API do wordpress havia um endpoint que mostrava todos os usuários.
</p>

<div style="text-align: center;">

![banner](oscp\images\usuarios.png "banner")
</div>

>Nesta situação tinhamos apenas um usuário disponivel

<p>
Bom lição feita hora de passar o pente fino...</br>
Por se tratar de um site wordpress é comum encontrarmos plugins com falhas já catalogadas, pensando nisso decidi rodar o wpscan, uma ferramenta própria para isto, uma exelente ferramenta para terminarmos a analize do site.
</p>

<div style="text-align: center;">

![banner](oscp\images\wpscan.PNG "banner")
</div>

<p>
Bom neste ponto me depraro com um grande problema, o wpscan estava nos dizendo que havia encontrado mais de 28 vulnerabilidades, estamos falando da OSCP a chanse de todas as falhas apresentadas serem falsos prositivos é bem grande, mas a chanse de nos darmos mal por não analizar pede ser bem maior hahah.
</p>

>Neste ponto eu analizei vulnerabilidade por vulnerabilidade e foi como eu havia mencionado, eram todas falsas, agora você deve estar se perguntando "mas se você já desconfiava por que perdeu mais de 4 horas analizando" bom imagine comigo, eu contrato você para fazer uma auditoria em minha empresa, você realiza encontra vetores de ataque e reporta tudo perfeitamente para mim mas... você fez um scan com wscan e não testou se era verdade ou não o output do wpsacan, por estar com preguiça ou por estar deconfiado que não se trata de algo legítimo. Bom na semana seguinte minha empresa recebe um ataque de Ransomware que me leva a falência pois dentro destas 28 vulnerabilidades uma delas era real. E então você ainda não perderia várias horas para testar se é algo verdadeiro ou não? *__Semptre teste todos os vetores de ataque!__*


<div style="text-align: center;">

### Enumerando o servidor

</div>
<p>
Acabou a diversão hora de entrarmos...
</p>

<div style="text-align: center;">

![banner](oscp\images\init.png "banner")
</div>



<p>
A chave privada nos deu acesso direto ao alvo, hora de varrer o servidor.<br>
Aqui foram mais algumas horas verrendo o servidor, buscando e juntando o máximo de informação possível. e de novo muitos falsos positivos, além das falhas que não eram possível explorar em tal situação, pois necessitavam compilar os exploits e não tinhamos um compilador disponível.
</p>

<p>
Durante e exploração achei usuário e senha pra o banco de dado, o que me animou bastante, pois o caminho www/html inteiro estava com permisão de root, pensando em uma revers shell pelo site isto nos traria uma shell como root logo de cara, porém ao entrar no banco de dados além de estar bem configurado as senhas dos usuários estava protegida por uma criptografia bem forte então fim da linha meu parceiro hahah
</p>

<div style="text-align: center;">

![banner](oscp\images\mysql.png "banner")
</div>


<p>
Neste ponto eu já estava quase sem ideias, pois o servidor era bem limitado a explorações. então pensei que era hora de apelar hahah, antes uma breve explicação...<br>
Toda vez que o servidor inicia ele roda um precesso inteiro pelo systemd que coleta o IP da máquina e nos mostra na tela, até ai tudo OK porém o último script chamado pelo systemd era uma scirpt chamado de "ip", este script estava em nossa área de trabalho e para ajudar tinha permições de root, o grande ponto aqui era que o script que chamava esse "ip" fazia exatamente isso, buscava apenas o scrit "ip" não havia qualqer validação se era o script correto ou não, neste ponto ficou bem fácil, pois bastava substituir esse script "ip" por um nosso e dentro colocarmos o que quisermos que seria executado como root.
</p>

>Caso se pergunte por que de eu não ter só editado o script original, bom eu não tinha permissão para editar o script :)

<p>
Em minhas escalações de privílegio gosto bastante e sempre que possível atribuir a premisão SUID para o /bin/bash assim sempre que eu executar o bash com suas premissões de natureza vai me retornar uma shell como root, e foi exatamente o que eu fiz, criei o novo script "ip" e dentro dele coloquei o código que daria tal permissão, logo após a máquina reiniciar temos uma surpresa boa.
</p>

<div style="text-align: center;">

![banner](oscp\images\bash.png "banner")
</div>

<p>
Agora que temos tal permissão basta executar o bash e pegar nosso tão esperado ROOT
</p>

<div style="text-align: center;">

![banner](oscp\images\root.png "banner")
</div>