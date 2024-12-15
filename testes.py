import pytest
from Jogo import Peca, Partida, TETROMINOES

@pytest.fixture
def tabuleiro_vazio():
    colunas = 10
    linhas = 20
    return [[" " for _ in range(colunas)] for _ in range(linhas)]

@pytest.fixture
def peca(tabuleiro_vazio):
    return Peca(len(tabuleiro_vazio[0]))

@pytest.fixture
def partida():
    return Partida(20, 10, "Jogador", None, None)

### Testes para a Classe Peca ###

def test_peca_inicializacao(peca):
    assert peca.forma in TETROMINOES
    assert peca.y == 0
    assert peca.x == 10 // 2
    assert peca.simbolo in ["#", "*", "+", "$", "&", "%", "@"]

def test_peca_posicionamento_valido(peca, tabuleiro_vazio):
    assert peca.posicionarTabuleiro(tabuleiro_vazio) is True

def test_peca_posicionamento_invalido(peca, tabuleiro_vazio):
    # Bloqueando a posição inicial da peça
    tabuleiro_vazio[peca.y][peca.x] = '#'
    assert peca.posicionarTabuleiro(tabuleiro_vazio) is False

def test_peca_movimento_valido(peca, tabuleiro_vazio):
    peca.posicionarTabuleiro(tabuleiro_vazio)
    assert peca.moverPeca(tabuleiro_vazio, 0, 1) is None
    assert peca.y == 1

def test_peca_movimento_invalido(peca, tabuleiro_vazio):
    peca.posicionarTabuleiro(tabuleiro_vazio)
    peca.y = 19  # Colocar a peça no limite inferior do tabuleiro
    assert peca.moverPeca(tabuleiro_vazio, 0, 1) is False

def test_peca_rotacao(peca, tabuleiro_vazio):
    peca.posicionarTabuleiro(tabuleiro_vazio)
    peca.rotacionar(tabuleiro_vazio)
    assert peca.forma in TETROMINOES  # A rotação mantém a peça válida

### Testes para a Classe Partida ###

def test_partida_inicializacao(partida):
    assert len(partida.grade) == 20
    assert len(partida.grade[0]) == 10
    assert partida.peca_atual is not None
    assert partida.pontuacao == 0

def test_partida_remocao_linhas(partida):
    # Preencher a última linha
    partida.grade[19] = ['#' for _ in range(10)]
    partida.pontuacao = partida.removerLinhas() * 100
    assert partida.grade[19] == [' ' for _ in range(10)]
    assert partida.pontuacao > 0

def test_partida_fim_de_jogo(partida):
    # Bloquear a posição inicial da peça
    partida.grade[0][5] = '#'
    partida.grade[0][6] = '#'
    assert partida.peca_atual.posicionarTabuleiro(partida.grade) is False

def test_partida_movimentos(partida):
    peca = partida.peca_atual
    peca.posicionarTabuleiro(partida.grade)
    assert partida.peca_atual.moverPeca(partida.grade, -1, 0) is None
    assert peca.x == 4  # Verifica se a peça se moveu para a esquerda