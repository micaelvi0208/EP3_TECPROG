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
            if tabuleiro[y_pos][x_pos] != ' ':
                return False
        for dx, dy in coord:
            x_pos = self.x + dx
            y_pos = self.y + dy
            tabuleiro[y_pos][x_pos] = self.simbolo
        return True

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
    
    def podeMover(self, tabuleiro, dx, dy):
        # Coordenadas da peça atual
        coord_atual = TETROMINOES[self.forma]

        # Verificar a nova posição
        for dx_, dy_ in coord_atual:
            x_pos = self.x + dx + dx_
            y_pos = self.y + dy + dy_

            # Verifica limites do tabuleiro
            if x_pos < 0 or x_pos >= len(tabuleiro[0]) or y_pos >= len(tabuleiro):
                return False

            # Ignora verificações para partes fora do tabuleiro (acima)
            if y_pos < 0:
                continue

            # Verifica colisões com peças fixadas no tabuleiro
            if tabuleiro[y_pos][x_pos] != ' ':
                # Garante que a posição atual da peça não seja considerada como obstáculo
                if (x_pos, y_pos) not in [(self.x + dx_, self.y + dy_) for dx_, dy_ in coord_atual]:
                    return False

        return True
    
    def rotacionar(self, tabuleiro, sentido_horario=True):
        if self.forma == 'O':  # O não precisa rotacionar
            return

        # Calcular novas coordenadas para a rotação
        novas_coordenadas = []
        for dx, dy in TETROMINOES[self.forma]:
            if sentido_horario:
                novas_coordenadas.append((-dy, dx))  # Rotação no sentido horário
            else:
                novas_coordenadas.append((dy, -dx))  # Rotação no sentido anti-horário)

        # Validar se a rotação é possível
        for dx, dy in novas_coordenadas:
            x_pos = self.x + dx
            y_pos = self.y + dy

            # Verificar limites do tabuleiro
            if x_pos < 0 or x_pos >= len(tabuleiro[0]) or y_pos < 0 or y_pos >= len(tabuleiro):
                return  # Rotação inválida

            # Verificar colisão com peças já fixas no tabuleiro
            if tabuleiro[y_pos][x_pos] != ' ':
                return  # Rotação inválida

            # Apagar a posição anterior da peça no tabuleiro
            self.apagaAnterior(tabuleiro)

            # Atualizar as coordenadas da peça com a rotação válida
            TETROMINOES[self.forma] = novas_coordenadas
            self.posicionarTabuleiro(tabuleiro)


class Partida:
    def __init__(self, linhas, colunas, jogador):
        self.grade = [[" " for _ in range(colunas)] for _ in range(linhas)]
        self.linhas = linhas
        self.colunas = colunas
        self.jogador = jogador
        self.peca_atual = Peca(colunas)
        self.jogo_ativo = True
        self.pontuacao = 0

    def jogar(self):
        #self.peca_atual = self.gerar_peca()
        while self.jogo_ativo:
            Tela.limpar_tela()  # Limpa a tela antes de exibir a atualização

            if not self.peca_atual.posicionarTabuleiro(self.grade):
                self.jogo_ativo = False
                Tela.limpar_tela()
                Tela.exibir(self.grade, self.pontuacao)
                print("Game Over!")
                return

            
            Tela.exibir(self.grade, self.pontuacao)

            sair = False
            while self.peca_atual.podeMover(self.grade, 0, 1) and sair == False:
                tecla = readkey()
                if tecla == 's':
                    sair = True
                elif tecla == key.DOWN:
                    if self.peca_atual.podeMover(self.grade, 0, 1):
                        self.peca_atual.moverPeca(self.grade, 0, 1)
                elif tecla == key.RIGHT:
                    if self.peca_atual.podeMover(self.grade, 1, 0):
                        self.peca_atual.moverPeca(self.grade, 1, 0)
                elif tecla == key.LEFT:
                    if self.peca_atual.podeMover(self.grade, -1, 0):
                        self.peca_atual.moverPeca(self.grade, -1, 0)
                elif tecla == key.PAGE_UP:
                    self.peca_atual.rotacionar(self.grade, sentido_horario=True)
                elif tecla == key.PAGE_DOWN:
                    self.peca_atual.rotacionar(self.grade, sentido_horario=False)
                elif tecla == 'g':
                    self.peca_atual.apagaAnterior(self.grade)
                    self.salvar_jogo()
                    sair = True
                else:
                    continue
                Tela.limpar_tela()
                Tela.exibir(self.grade, self.pontuacao)

                if not self.peca_atual.podeMover(self.grade, 0, 1):
                    self.peca_atual.posicionarTabuleiro(self.grade)
                    linhas_removidas = self.removerLinhas()
                    self.pontuacao += linhas_removidas * 100
                    self.peca_atual = Peca(self.colunas)
    
    def removerLinhas(self):
        novas_linhas = [linha for linha in self.grade if " " in linha]
        linhas_removidas = len(self.grade) - len(novas_linhas)
        self.grade = [[" " for _ in range(self.colunas)] for _ in range(linhas_removidas)] + novas_linhas
        return linhas_removidas

    def salvar_jogo(self):
        with open("save_game.txt", "w") as f:
            f.write(f"{self.pontuacao}\n")
            for linha in self.grade:
                f.write("".join(linha) + "\n")

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