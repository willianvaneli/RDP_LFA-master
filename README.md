# LFA-DSL

[Especificações do trabalho](lfa-trab-final-2019-1.pdf)

## Grupo:
- Ewerson Vieira Nascimento (ewersonv@gmail.com)
- Paulo Ricardo Viana Ferreira (paulo_ricardosf@outlook.com)
- Willian Bruschi Vaneli (willianvaneli@gmail.com)

## Ambiente de desenvolvimento:
- Programa desenvolvido em Python (3.6.7) 
- Biblioteca [Ply](https://www.dabeaz.com/ply/)
- Visual studio code
- Windows


## Justificativa uso da biblioteca Ply:
A biblioteca Ply apresenta facilidade de declaração dos tokens e EBNF, onde é possível separar cada declaração e trata-la de modo exclusivo.


## Tabela com Operadores e Expressões:

Operador | Descrição
--------- | ------
=              | Atribuição. Ex.: <variável> = <conteúdo>;
==,>,<,>=,<=   | Comparadores lógicos
{ }            | Delimitadores de bloco, podem ser usados em IF, While, declaração de função ou em chamada de função;
+,-,*,/,^,//,% | Operadores aritiméticos;
    
    
Expressão | Descrição
--------- | ------
def         | Expressão que define uma função. Ex.: def <nome-do-método>(<argumentos>){ };
if          | Expressão que indica uma estrutura de seleção. Ex.: if (<condição>){<bloco>};
while       | Expressão que indica um loop. Ex.: while (<condição>){<operações>*};

## Estrutura da aplicação

```
trabalho-final-lfa-DHM
|_ DSL-ply
  |_ ply (pasta da biblioteca ply)
  |_parser.out
  |_parser.py
  |_parsertab.py
|_ Testes
  |_ 
|_ Readme.md
|_ relatório.pdf
```

### Descrição dos arquivos:

Arquivo | Descrição
--------- | ------
[parser.py](DSL-ply/parser.py)    | Arquivo contendo a gramática em EBNF da linguagem e demais funções desenvolvidas em python. 
[pasrsetab.py](DSL-ply/parsetab.py)    | Arquivo gerado automaticamente pelo Ply contendo informações de execução do parser.
[parser.out](DSL-ply/parser.out) | Arquivo gerado pelo Ply contendo informações sobre a gramática e os estados do parser.


#### Para a execução do parser é necessário instalar o python e a biblioteca ply.  

## Instalando python.  

### _Windows_  
Acessar o site oficial do [python](https://www.python.org/downloads/) realizar o download,  
Antes de iniciar a instalação selecione a opção de configurar o path, avance e aguarde o fim da instalação.  

### _Ubuntu_  
#### _Passo 1 - Pré requisitos_

Execute na linha de comando:

``$ sudo apt-get install build-essential checkinstall``

``$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \ libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev``

#### _Passo 2 - Download do python 3.7_

Execute na linha de comando:

``$ cd /usr/src``

``$ sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz``

Agora extraia o pacote com o comando:

``$ sudo tar xzf Python-3.7.3.tgz``

#### _Passo 3 instale o python_

Execute na linha de comando:
``$ cd Python-3.7.3``

``$ sudo ./configure --enable-optimizations``

``$ sudo make altinstall``

#### _Passo 4 cheque a instalação do python_  

Execute na linha de comando:  

``$ python3 --version``

Caso retorne ``Python-3.7.3`` a instalação foi realizada com sucesso.


## _Instalando biblioteca ply_  

Após fazer o download no [site](http://www.dabeaz.com/ply/) basta extrair o conteudo do arquivo compactado e acessar a pasta ply-3.11, onde está localizado o arquivo ``setup.py`` por linha de comando e executar o seguinte comando:

``$ python setup.py install``

dependendo do SO pode ser que seja necessário usar

``$ python3 setup.py install``
