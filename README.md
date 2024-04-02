# <p align="center">Projeto de Processamento de Dados<br>Bacen - PTAX</p>

<p align="center">
<img src="http://img.shields.io/static/v1?label=LICENCA&message=...&color=GREEN&style=for-the-badge"/>     
<img src="http://img.shields.io/static/v1?label=STATUS&message=N/A&color=GREEN&style=for-the-badge"/>
</p>

Este projeto visa criar um "sistema" em Python para consumir a API do Banco Central, obtendo os valores de fechamento de venda e compra de cotação de moedas estrangeiras. Utilizando a biblioteca requests para fazer as requisições HTTP e o Docker com PostgreSQL para armazenar os dados, a iniciativa busca facilitar o acesso e análise dessas informações de forma direta e eficiente.

## Diagrama de Fluxo

![Diagram](https://github.com/tonsatomicos/bacen-ptax-data-processing/blob/main/assets/diagram.png?raw=true)

Sinta-se à vontade para clonar, adaptar e ajustar o projeto conforme necessário. Consulte as instruções abaixo, se precisar. :alien:

## Dependências do Projeto

Este projeto foi desenvolvido utilizando o Poetry para gerenciamento de ambientes virtuais e bibliotecas.

### Bibliotecas Utilizadas

- pandas = "^2.2.1"
- requests = "^2.31.0"
- sqlalchemy = "^2.0.29"
- psycopg2 = "^2.9.9"

### Instalação das Dependências

Você pode instalar as dependências manualmente, ou, utilizando o Poetry ou o Pip com os seguintes comandos:

#### Utilizando Poetry

```bash
poetry config virtualenvs.in-project true
poetry env local 3.12.1
poetry install

```

#### Utilizando Pip

```bash
pip install pandas requests sqlalchemy psycopg2

```

## Configurações do Projeto

Utilizando PostgreSQL para persistência de dados, porém você tem a liberdade de optar por outras bases de dados. No entanto, caso escolha o PostgreSQL, sinta-se à vontade para seguir o guia abaixo.

### Banco de dados PostgreSQL

Você pode escolher entre utilizar o Docker para subir um banco PostgreSQL ou instalar de outras maneiras.

#### Utilizando Docker

<pre><code>docker-compose up -d</code></pre>

#### Outras maneiras

Segue tutorial aleatório da **<a href="https://youtu.be/L_2l8XTCPAE?si=-OJ21qv_48BgHFq2">Hashtag Treinamentos</a>**. <br>Script de criação da tabela disponibilizado em <code>src/sql</code>.

### Conclusão

Lembre-se sempre de verificar o usuário, senha, base, porta e tabela. Configurado logo após o início da  função <code>main</code>, altere se necessário.

<pre><code>    start_date = '02-01-2016'
    end_date = '04-01-2024'
    coin = 'EUR' # or USD
    dbuser = 'teste'
    dbpass = 'teste'
    dbname = 'teste_db'
    dblocal = 'localhost:5437'
    dbtable = 'public.ptax'</code></pre>

Isso irá garantir que as informações sejam persistidas no banco de dados PostgreSQL.</p>


## Considerações Finais

- Com esse projeto, conseguimos facilmente persistir informações de diversos tipos de moedas, contanto que estejam disponíveis na <a href="https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/Moedas#eyJmb3JtdWxhcmlvIjp7IiRmb3JtYXQiOiJqc29uIiwiJHRvcCI6MTAwfSwicHJvcHJpZWRhZGVzIjpbMCwxLDJdLCJwZXNxdWlzYWRvIjp0cnVlLCJhY3RpdmVUYWIiOiJ0YWJsZSIsImdyaWRTdGF0ZSI6ewMwAzpbewNCAyIEMAQiLANBA30sewNCAyIEMQQiLANBA30sewNCAyIEMgQiLANBA31dLAMxAzp7fSwDMgM6W10sAzMDOnt9LAM0Azp7fSwDNQM6e319LCJwaXZvdE9wdGlvbnMiOnsDYQM6e30sA2IDOltdLANjAzo1MDAsA2QDOltdLANlAzpbXSwDZgM6W10sA2cDOiJrZXlfYV90b196IiwDaAM6ImtleV9hX3RvX3oiLANpAzp7fSwDagM6e30sA2sDOjg1LANsAzpmYWxzZSwDbQM6e30sA24DOnt9LANvAzoiQ29udGFnZW0iLANwAzoiVGFibGUifX0=">base de dados</a> do Banco Central do Brasil (BACEN).

<hr>

![Image](https://i.imgur.com/p4vnGAN.gif)
