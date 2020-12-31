# quickplay discord bot
> Repositório para o bot oficial da Quick Play, desenvolvido em python.

[![python-image]][python-url]
[![discord-image]][discord-url]
[![heroku-image]][heroku-url]
[![mongodb-image]][mongodb-url]

Nesse repositório vocẽ encontra informações de instalação, comandos do bot, além de ter acesso ao código fonte, que inclui uma licença open source pra copiar (desde que use a mesma licença no seu projeto)

<remove me> ![](../header.png)
## Índice

* [Comandos](#comandos)
* [Setup & Instalação](#setup--instalação)

## Comandos  

|    Comando   |    Sintaxe    |   Descrição   |
|     :---     |     :---:     |     :---:     |
| Info | !info <membro> | Mostrar informações de um membro. |
| Regras | !regras | Mostrar todas as regras do servidor. |
| Regra | !regra <nº da regra> | Mostrar a regra solicitada. |
| Limpar | !limpar [quantidade] | [ADM] Deletar mensagens recentes. |
| Kick | !kick <membro> [razão] | [ADM] Retirar um membro do servidor. |
| Ban | !ban <membro> [razão] | [ADM] Banir um membro do servidor. |
| Brinde | !brinde [membro] | Solicitar um brinde de qBits (aleatório entre 3 e 7 qBits). |
| Enviar_qbits | !enviar_qbits <membro> <valor> | Transferência de qBits da sua conta para outro membro. |
| Depositar | !depositar <membro> <valor> | [ADM] Deposita qualquer quantia de qBits para um membro. |
| Retirar_qbits | !retirar_qbits [membro] <valor> | [ADM] Retira qualquer quantia de qBits para um membro. |


## Setup & Instalação
Primeiro é necessário instalar, configurar e ativar um ambiente virtual, para um melhor gerenciamento do projeto.

```
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

>Clone o repo
pip install requirements.txt

>Crie uma conta no discord e siga a documentação oficial para:
Criar um bot
Criar um servidor
Vincular seu bot ao servidor
https://discord.com/developers/docs/intro

>crie um arquivo ".env" no mesmo diretório que o "bot.py", contendo 2 variáveis:
DISCORD_TOKEN=219038129031290asdasduiashuidahsuidsad
DB_URL=mongodb+srv://clustername:<password>-cluster-cl.server.mongodb.net/test

>Crie uma conta grátis no https://cloud.mongodb.com
Siga a documentação oficial para:
Criar um cluster
Criar uma database
Criar uma collection
No dashboard do mongodb é possível obter o url para conectar, que vai no arquivo ".env"
https://docs.mongodb.com/

>Crie uma conta grátis no heroku
Crie uma nova aplicação no heroku
Vincule sua conta no heroku com a do github, no menu "deploy"
Acompanhe nos logs do heroku seu próximo commit
Para sua aplicação executar automaticamente, habilite o "worker" no menu "Resources"

[python-image]: https://img.shields.io/static/v1?label=python&message=3.7&color=blue
[python-url]: https://www.python.org/downloads/release/python-370/

[discord-image]: https://img.shields.io/static/v1?label=discord.py&message=rewrite+&color=lightgrey
[discord-url]: https://discord.com/developers/docs/intro

[heroku-image]: https://img.shields.io/static/v1?label=heroku&message=app&color=red
[heroku-url]: https://www.heroku.com/

[mongodb-image]: https://img.shields.io/static/v1?label=mongodb&message=atlas&color=success
[mongodb-url]: https://docs.mongodb.com/

Distribuído sob a licença `GNU GENERAL PUBLIC LICENSE`. Veja `LICENSE` para mais informações.