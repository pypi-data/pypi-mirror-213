# SPLN-TP2 Template Multi-file

**Daniel Faria PG50306**

**Hugo Brandão PG50418**

**João Cerquido PG50469**

Projeto desenvolvido no âmbito da UC de SPLN.
Permite a criação de uma estrutura de ficheiros e pastas, a partir de um ficheiro de template, podendo ser especificado o conteúdo de cada ficheiro criado.
Também é possível realizar o processo inverso, ou seja, a partir de uma estrutura de ficheiros e pastas, criar um ficheiro de template.

## Utilização:
utilização: Templater [-h] -i INPUT -t TYPE [-o OUTPUT] [-v [VARIABLES [VARIABLES ...]]]

Programa simples que lê um ficheiro de template e cria a estrutura de pastas e ficheiros com base no template. Também
pode ser feito o inverso, pode ler uma estrutura de pastas e criar um ficheiro de template com base nela.

    optional arguments:
        -h, --help            mostra esta mensagem de ajuda e sai
        -i INPUT, --input INPUT
            Input file ou folder
        -t TYPE, --type TYPE  
            Tipo de operação. Pode ser template (gera template segundo uma diretoria) ou create (gera diretoria de um template file)
        -o OUTPUT, --output OUTPUT
            Output file ou folder
        -v [VARIABLES [VARIABLES ...]], --variables [VARIABLES [VARIABLES ...]]
            Variaveis a serem substituidas no template


## Formato do template:
O template deverá ser constituído por 3 partes:
- metadata
- tree
- files

### Metadata
Os metadados deverão ser enumerados com o padrão nome: valor, e deverão ser escritos um em cada linha.

Exemplo:

    === meta
    name:             
    author: JJoao

### Tree
A árvore do projeto deverá ser escrita com as seguintes regras:
- Cada pasta deverá ser identificada com o seu nome seguido de uma barra
- Cada ficheiro que pertença a uma pasta deverá ser escrita após a pasta, com um tab de identação
- Os tabs deverão ser de 4 espaços

Exemplo:

    === tree
    pyproject.toml
    {{name}}/
        __init__.py
        {{name}}.md
    exemplo/
    README.md
    tests/
        test-1.py
        unit/
            test-2.py

### Files
Os ficheiros deverão ser escritos com o seguinte formato:
- O nome do ficheiro deverá ser precedido de ===
- O nome do ficheiro deverá conter o caminho relativo à pasta principal do projeto
- E o seu conteúdo deverá ser escrito nas linhas seguintes, até encontrar outro ficheiro ou o fim do ficheiro de template

Exemplo:

    === pyproject.toml
    [build-system]
    requires = ["flit_core >=3.2,<4"]
    build-backend = "flit_core.buildapi"

    [project]
    name = "{{name}}"
    authors = [ {name = "{{author}}", email = "FIXME"}]
    license = {file = "LICENSE"}
    dynamic = ["version", "description"]
    dependencies = [ ]
    readme = "{{name}}.md"

    [project.scripts]
    ## script1 = "{{name}}:main"

    === {{name}}/{{name}}.md

    # NAME

    {{name}} - FIXME the fantastic module for...

    === {{name}}/__init__.py
    """ FIXME: docstring """
    __version__ = "0.1.0"

    === tests/test-1.py
    import pytest
    import {{name}} 

    def test_1():
        assert "FIXME" == "FIXME"