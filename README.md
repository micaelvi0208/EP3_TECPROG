# EP3 - Tetris em Python

## AUTOR(ES)
- **Nome:** Micael Vinicius Lira Prado  
- **NUSP:** 11857991  
- **E-mail:** micael0208@usp.br  

## DESCRIÇÃO
Este projeto implementa uma versão simplificada do jogo Tetris em Python como parte do EP3 da disciplina.  

O jogo conta com:  
- Geração de peças baseadas nos tetraminós originais.  
- Movimento das peças (esquerda, direita, baixo) e rotação.  
- Verificação de colisões com o tabuleiro e outras peças.  
- Remoção de linhas completas e sistema de pontuação.  

A lógica do jogo é totalmente implementada em Python, com foco na clareza do código e facilidade de extensão.  

O projeto também inclui:  
- Um conjunto de testes automatizados escritos em `pytest`.  
- Geração de documentação automática usando o Doxygen.  
- Um arquivo `Makefile` para simplificar a execução e manutenção do projeto.  

## COMO EXECUTAR
### Requisitos
Antes de executar o programa, certifique-se de ter o **Python 3.8 ou superior** instalado.  

Além disso, recomenda-se o uso de um **ambiente virtual** para isolar as dependências do projeto.  

Dependências adicionais:  
- **Doxygen**: Para geração de documentação.  
- **pytest**: Para execução dos testes.  
- **readchar**: Para entrada de caracteres no jogo.  

Instale as dependências com os seguintes comandos:  
```bash
sudo apt install doxygen
pip install pytest
pip install readchar
```

Passos para Execução
Clone o repositório:
```
git clone [URL_DO_REPOSITORIO]
cd [PASTA_DO_REPOSITORIO]
Ative o ambiente virtual (caso esteja utilizando).
```

Para rodar o jogo:
```
make run
```
O jogo será iniciado e você poderá controlar as peças com as seguintes teclas:

Setas esquerda/direita: mover a peça.
Seta para baixo: acelerar a descida da peça.
pgdn/pgup: rotacionar a peça.

Para gerar a documentação com Doxygen:
```
make doc
```
A documentação será gerada na pasta docs/ em formato HTML.
Abra o arquivo docs/html/index.html no navegador de sua preferência para visualizar.

Para rodar os testes:
```
make test
```

Comandos disponíveis no Makefile
make run: Executa o jogo.
make doc: Gera a documentação com o Doxygen.
make test: Executa os testes automatizados.
make clean: Remove arquivos e diretórios gerados durante a execução.

##TESTES
Os testes foram implementados usando o framework pytest e cobrem as principais funcionalidades do jogo:

Geração e movimentação das peças.
Rotação e verificação de colisões.
Identificação e remoção de linhas completas.
Detecção de condições de fim de jogo.

Para executar os testes:
```
pytest testes.py/
```
Ou utilize o comando:
```
make test
```
Os resultados exibem o status de todos os testes, permitindo identificar falhas ou erros de implementação.

##DEPENDÊNCIAS
O programa foi desenvolvido e testado nas seguintes condições:

Sistema Operacional: Debian 22.04, Windows 10 (compatível com outros sistemas operacionais).
Python: Versão 3.8 ou superior.

Dependências adicionais:

pytest: Necessário para execução dos testes.
readchar: Para controle das entradas de teclado no jogo.
doxygen: Para geração da documentação.

Certifique-se de que todas as dependências estão instaladas antes de rodar o jogo, executar os testes ou gerar a documentação.
