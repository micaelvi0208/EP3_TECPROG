import os
import random
from readchar import readkey, key


TETROMINOES = {
    'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
    'L': [(0, 1), (1, 1), (2, 1), (2, 2)],
    'J': [(0, 1), (1, 1), (2, 1), (2, 0)],
    'S': [(1, 0), (1, 1), (0, 1), (0, 2)],
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)]
}


class bloco:
    def __init__(self, x, y, simbolo):
        self.x = x
        self.y = y
        self.simbolo = simbolo

    def atualizaPosicao(self, prox_x, prox_y):
        self.x = prox_x
        self.y = prox_y

    def temColisao(self, lim_v, lim_h):
        if 0 <= self.x < lim_h and self.y < lim_v:
            return False
        return True


class Peca:
    def __init__(self, colunas):
        self.forma = random.choice(list(TETROMINOES.keys()))
        if self.forma == 'I':
            self.simbolo = '$'
        elif self.forma == 'O':
            self.simbolo = '&'
        elif self.forma == 'T':
            self.simbolo = '+'
        elif self.forma == 'L':
            self.simbolo = '#'
        elif self.forma == 'J':
            self.simbolo = '*'
        elif self.forma == 'S':
            self.simbolo = '%'
        else:
            self.simbolo = '@'
        self.x = int (colunas/2)
        self.y = 0
    
    def posicionarTabuleiro(self, tabuleiro):
        coord = TETROMINOES[self.forma]
        for dx, dy in coord:
            x_pos = self.x + dx
            y_pos = self.y + dy
            tabuleiro[y_pos][x_pos] = self.simbolo

    def moverPeca(self,tabuleiro,dx,dy):
        self.apagaAnterior(tabuleiro)
        self.x += dx
        self.y += dy
        self.posicionarTabuleiro(tabuleiro)

    def apagaAnterior(self, tabuleiro):
        coord = TETROMINOES[self.forma]
        for dx, dy in coord:
            x_pos = self.x + dx
            y_pos = self.y + dy
            tabuleiro[y_pos][x_pos] = ' '
   

class Partida:
    def __init__(self, linhas, colunas, jogador):
        self.grade = [[" " for _ in range(colunas)] for _ in range(linhas)]
        self.linhas = linhas
        self.colunas = colunas
        self.jogador = jogador
        self.peca_atual = Peca(colunas)
        self.jogo_ativo = True

    def jogar(self):
        #self.peca_atual = self.gerar_peca()
        while self.jogo_ativo:
            Tela.limpar_tela()  # Limpa a tela antes de exibir a atualização
            self.peca_atual.posicionarTabuleiro(self.grade)
            Tela.exibir(self.grade, 0)
        
            tecla = readkey()
            if tecla == 's':
                break
            elif tecla == key.DOWN:
                self.peca_atual.moverPeca(self.grade, 0, 1)
            elif tecla == key.RIGHT:
                self.peca_atual.moverPeca(self.grade, 1, 0)
            elif tecla == key.LEFT:
                self.peca_atual.moverPeca(self.grade, -1, 0)
            elif tecla == key.PGUP:
                print("Rotaciona horário")
            elif tecla == key.PGDN:
                print("Rotaciona antihorário")
            elif tecla == key.PGUP:
                print("Rotaciona horário")
            elif tecla == 'g':
                print("grava e sai")
            else:
                continue


class Tela:
    @staticmethod
    def limpar_tela():
        # Limpa a tela dependendo do sistema operacional
        os.system('cls||clear')

    @staticmethod
    def exibir(grade, pontuacao):
        print("—" * (len(grade[0]) + 2))
        for linha in grade:
            print("|" + "".join(linha) + "|")
        print("—" * (len(grade[0]) + 2))
        print(f"Pontuação: {pontuacao}")
        print("\nComandos: ←, →, ↓, s (sair)")
        print("<Page Down> rotaciona esquerda | <Page Up> rotaciona direita")
        print("<s> sai da partida, <g> grava e sai da partida")
        


if __name__ == "__main__":
    partida = Partida(8, 12, "Micael")
    partida.jogar()