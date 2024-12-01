import os
import sys

class Jogo:
    def __init__(self):
        self.ranking = Ranking()

    def iniciar(self):
        while True:
            print("\n*** Jogo Textris - um tetris em modo texto ***")
            print("Opções do jogo:")
            print("- <i> para iniciar uma nova partida")
            print("- <c> para carregar uma partida gravada e continuá-la")
            print("- <p> para ver as 10 melhores pontuações")
            print("- <s> para sair do jogo")
            opcao = input("Digite a opção desejada: ").strip().lower()

            match opcao:
                case "i":
                    self.iniciar_partida()
                case "c":
                    self.carregar_partida()
                case "p":
                    self.mostrar_ranking()
                case "s":
                    print("Saindo do jogo. Até mais!")
                    sys.exit(0)
                case _:
                    print("Opção inválida. Tente novamente.")

    def iniciar_partida(self):
        try:
            nome_jogador = input("Digite o nome do jogador: ").strip()
            linhas = int(input("Digite o número de linhas da tela do jogo: ").strip())
            colunas = int(input("Digite o número de colunas da tela do jogo: ").strip())
        
            if linhas <= 0 or colunas <= 0:
                print("Linhas e colunas devem ser maiores que zero.")
                return
        
            partida = Partida(linhas, colunas, nome_jogador)
            partida.exibir_grade()
            partida.gerar_peca()
            partida.exibir_grade()
            partida.finalizar_jogo()
        except ValueError:
            print("Por favor, insira valores válidos para linhas e colunas.")

    def carregar_partida(self):
        print("Carregando partida salva...")
        # Aqui você pode implementar lógica para carregar uma partida de um arquivo
        pass

    def mostrar_ranking(self):
        print("Exibindo ranking das melhores pontuações:")
        self.ranking.mostrar_top_10()

class Ranking:
    def __init__(self):
        self.pontuacoes = []

    def adicionar_pontuacao(self, jogador, pontos):
        self.pontuacoes.append((jogador, pontos))
        self.pontuacoes.sort(key=lambda x: x[1], reverse=True)

    def mostrar_top_10(self):
        print("Ranking:")
        for idx, (jogador, pontos) in enumerate(self.pontuacoes[:10], start=1):
            print(f"{idx}. {jogador}: {pontos} pontos")
        if not self.pontuacoes:
            print("Nenhuma pontuação registrada ainda.")

class Partida:
    def __init__(self, linhas, colunas, jogador):
        """
        Inicializa uma nova partida.
        
        :param linhas: Número de linhas da grade do jogo.
        :param colunas: Número de colunas da grade do jogo.
        :param jogador: Nome do jogador.
        """
        self.linhas = linhas
        self.colunas = colunas
        self.jogador = jogador
        self.grade = [[" " for _ in range(colunas)] for _ in range(linhas)]  # Cria a grade vazia
        self.pontuacao = 0  # Inicializa a pontuação do jogador
        self.peca_atual = None  # Nenhuma peça no início do jogo
        self.jogo_ativo = True  # Estado do jogo

    def exibir_grade(self):
        """
        Exibe a grade do jogo no terminal.
        """
        print("—" * (self.colunas + 2))  # Borda superior
        for linha in self.grade:
            print("|" + "".join(linha) + "|")
        print("—" * (self.colunas + 2))  # Borda inferior

    def gerar_peca(self):
        """
        Gera uma nova peça no topo da tela.
        """
        self.peca_atual = Peça.criar_aleatoria(self.colunas)
        self.inserir_peca_na_grade()

    def inserir_peca_na_grade(self):
        """
        Insere a peça atual no topo da grade.
        """
        if self.peca_atual:
            for linha, coluna in self.peca_atual.coordenadas:
                self.grade[linha][coluna] = self.peca_atual.simbolo

    def mover_peca(self, direcao):
        """
        Move a peça atual para a esquerda, direita ou para baixo.

        :param direcao: Direção do movimento ("esquerda", "direita", "baixo").
        """
        # Implementação do movimento será detalhada conforme as regras do jogo.
        pass

    def finalizar_jogo(self):
        """
        Finaliza a partida.
        """
        self.jogo_ativo = False
        print(f"Jogo encerrado! Pontuação final: {self.pontuacao}")

import random

class Peça:
    def __init__(self, simbolo, coordenadas):
        """
        Inicializa uma peça.
        
        :param simbolo: Caractere que representa a peça.
        :param coordenadas: Lista de tuplas (linha, coluna) representando a posição da peça.
        """
        self.simbolo = simbolo
        self.coordenadas = coordenadas

    @staticmethod
    def criar_aleatoria(colunas):
        """
        Cria uma peça aleatória na parte superior da grade.
        
        :param colunas: Número de colunas da grade.
        :return: Objeto Peça.
        """
        simbolos = ["#", "*", "%", "$"]
        formatos = [
            [(0, 0), (1, 0), (1, 1), (1, 2)],  # Peça "J"
            [(0, 0), (0, 1), (0, 2), (1, 1)],  # Peça "T"
            [(0, 0), (1, 0), (0, 1), (1, 1)],  # Peça "Quadrado"
        ]
        simbolo = random.choice(simbolos)
        formato = random.choice(formatos)

        # Centraliza a peça horizontalmente na grade
        deslocamento = (colunas // 2) - 1
        coordenadas = [(linha, coluna + deslocamento) for linha, coluna in formato]
        return Peça(simbolo, coordenadas)


# Execução do jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciar()