# libpythonpessoa
Módulo para exemplificar construção de projetos Python no curso Pytools

Nesse curso é ensinado como contribuir com projetos de codigo aberto

Link do curso [Python Pro](https://www.python.pro.br/)

[![Build Status](https://travis-ci.com/pessoasnil/libpythonpessoa.svg?branch=main)](https://travis-ci.com/pessoasnil/libpythonpessoa)
[![Updates](https://pyup.io/repos/github/pessoasnil/libpythonpessoa/shield.svg)](https://pyup.io/repos/github/pessoasnil/libpythonpessoa/)

Suportada a versão 3.8 de Pyyhon

Tópicos a serem Abordados:

    1. git
    2. Virtualenv
    3.Pip
    4.Travis 



Comando importantes do Pyenv:

    1. pyenv  install -l (checar as Versõs do Python)
    2. pyenv install (a versão escolhida)
    3. pyenv versions (Versões disponiveis nele)
    4. pyenv global (Versão escolhida)

Comando importantes do Pip, python e linux:

    1. pip  freeze(checar bibliotecas instaladas )
    2. pip  freeze > requiremensts.txt(arquivo para ficar na raiz que vai difinir dependencias do projeto )
    3. pip  install -r  requiremensts.txt(Cria o arquivo de dependencias se for preciso )
    3. pip  uninstalled requests  (desistala uma biblioteca)
    4. python3 -m venv .venv (crinado um venv local para testar os codigos )
    5. source .venv/bin/activate (ativando a .venv para testes)
    6. ls |grep lib (para ver onde esta meu projeto)
    7. pip install -e ./libpythonpessoa/(para instalar aqui a biblioteca e editar e testar)
    8. python setup.py sdist(Crita um diretorio com a minha distribuição)
    9. pip install twine(lib para fazer a fazer a publicação dp projeto no pypi.org)
    10.twine upload dist/*( para mandar tudo que eu tendro do meu projeto)


Comando importantes dentro do.venv:

    1. deactivate (sair do anbiante virtal )
    2. source .venv/bin/activate (entra no anbiante virtal )




 links relevantes: 

 [Dados Minha conta](https://api.github.com/users/pessoasnil)

 [Repositorio pip install](https://pypi.org/)

[Automatiza processso de integração de Dependencias](https://pyup.io/)



 