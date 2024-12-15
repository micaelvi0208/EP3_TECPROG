# Variáveis
PYTHON = python3
PYTEST = pytest
DOXYGEN = doxygen
DOXYFILE = Doxyfile
MAIN = Jogo.py
TESTES = testes.py

# Alvo para gerar tudo
all: doc tests

# Gerar documentação
doc:
	$(DOXYGEN) $(DOXYFILE)

# Rodar programa
run:
	$(PYTHON) ./$(MAIN)

# Rodar testes
tests:
	$(PYTEST) $(TESTES)/

# Limpar arquivos intermediários
clean:
	rm -rf html latex *.pyc __pycache__ .pytest_cache