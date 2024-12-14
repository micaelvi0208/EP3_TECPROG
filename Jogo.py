## @package Jogo
#Este programa é uma implementação em Python de um jogo semelhante ao Tetris chamado 'Textris'. 
#O jogo é exibido no terminal e permite que o jogador mova, rotacione e manipule peças que caem 
#em uma grade. Além disso, o programa suporta funcionalidades como salvar e carregar partidas, 
#manter um ranking de pontuações e exibir um menu interativo.
#
#Classes Principais:
#- Peca: Representa uma peça do jogo, incluindo seu tipo, posição, e lógica para movimento e rotação.
#- Partida: Gerencia uma partida individual do jogo, incluindo a lógica de atualização da grade, 
#  remoção de linhas completas e pontuação.
#- Tela: Responsável por exibir a interface do jogo no terminal e limpar a tela.
#- Jogo: Gerencia o fluxo principal do jogo, incluindo o menu principal, iniciar novas partidas 
#  e carregar partidas salvas.
#
#Constantes:
#- TETROMINOES: Define as formas das peças do jogo em termos de coordenadas relativas.
#
#Dependências:
#- readchar: Biblioteca usada para detectar entradas de teclado de forma interativa.
#- os: Usada para limpar a tela do terminal dependendo do sistema operacional.
#- random: Utilizada para selecionar peças aleatórias.
#- datetime: Utilizada para manipular datas e horários

import os
import random
from readchar import readkey, key
import datetime


## Constante Tetrominoes
# Definição das formas das peças (Tetrominoes) com coordenadas relativas"""
TETROMINOES = {
    'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
    'L': [(0, 1), (1, 1), (2, 1), (2, 2)],
    'J': [(0, 1), (1, 1), (2, 1), (2, 0)],
    'S': [(1, 0), (1, 1), (0, 1), (0, 2)],
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)]
}


## @class Peca
#  @brief Representa uma peça Tetromino no jogo, com funcionalidades para posicionamento, movimento e rotação.
class Peca:
    ## @brief Construtor da classe Peca.
    #  Inicializa uma peça com forma e símbolo aleatórios. A peça começa no topo central da grade.
    #  @param colunas Número de colunas na grade do jogo.
    def __init__(self, colunas):
        ## Forma do tetromino
        self.forma = random.choice(list(TETROMINOES.keys()))

        if self.forma == 'I':
            ## Símbolo usado para a forma em questão
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
        
        ## Coordenada horizontal inicial da peça
        self.x = int (colunas/2)
        ## Coordenada vertical inicial da peça
        self.y = 0
    
    ## @brief Posiciona a peça na grade do tabuleiro.
    #  @param tabuleiro Matriz representando a grade do jogo.
    #  @return True se o posicionamento for bem-sucedido, False caso contrário.
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

    ## @brief Move a peça no tabuleiro na direção especificada.
    #  @param tabuleiro Matriz representando o tabuleiro.
    #  @param dx Deslocamento na direção horizontal.
    #  @param dy Deslocamento na direção vertical.
    def moverPeca(self,tabuleiro,dx,dy):
        self.apagaAnterior(tabuleiro) 
        self.x += dx
        self.y += dy
        self.posicionarTabuleiro(tabuleiro) 

    ## @brief Remove a peça da posição atual no tabuleiro.
    #  Substitui as posições ocupadas pela peça por espaços vazios.
    #  @param tabuleiro Matriz representando o tabuleiro.
    def apagaAnterior(self, tabuleiro):
        coord = TETROMINOES[self.forma] 
        for dx, dy in coord:
            x_pos = self.x + dx
            y_pos = self.y + dy
            tabuleiro[y_pos][x_pos] = ' ' 
    
    ## @brief Verifica se a peça pode se mover para uma nova posição.
    #  @param tabuleiro Matriz representando o tabuleiro.
    #  @param dx Deslocamento na direção horizontal.
    #  @param dy Deslocamento na direção vertical.
    #  @return True se o movimento for válido, False caso contrário.
    def podeMover(self, tabuleiro, dx, dy):
    
        coord_atual = TETROMINOES[self.forma]

        for dx_, dy_ in coord_atual:
            x_pos = self.x + dx + dx_
            y_pos = self.y + dy + dy_

            if x_pos < 0 or x_pos >= len(tabuleiro[0]) or y_pos >= len(tabuleiro):
                return False

            if y_pos < 0:
                continue

            if tabuleiro[y_pos][x_pos] != ' ':
                if (x_pos, y_pos) not in [(self.x + dx_, self.y + dy_) for dx_, dy_ in coord_atual]:
                    return False

        return True
    
    ## @brief Rotaciona a peça no tabuleiro, se possível.
    #  @param tabuleiro Matriz representando o tabuleiro.
    #  @param sentido_horario Se True, rotaciona no sentido horário; caso contrário, rotaciona no sentido anti-horário.
    def rotacionar(self, tabuleiro, sentido_horario=True):
        ## Forma da peça vigente
        forma = self.forma
        if forma == 'O':  
            return

        novas_coordenadas = []
        for dx, dy in TETROMINOES[self.forma]:
            if sentido_horario:
                novas_coordenadas.append((-dy, dx))  
            else:
                novas_coordenadas.append((dy, -dx))  

        backup = novas_coordenadas
        for dx, dy in novas_coordenadas:
            x_pos = self.x + dx
            y_pos = self.y + dy

            if x_pos < 0 or x_pos >= len(tabuleiro[0]) or y_pos < 0 or y_pos >= len(tabuleiro):
                return  

            if tabuleiro[y_pos][x_pos] != ' ':
                return  

            self.apagaAnterior(tabuleiro)

            TETROMINOES[self.forma] = novas_coordenadas
            self.posicionarTabuleiro(tabuleiro)
            TETROMINOES[self.forma] = backup


## @package partida
#  Módulo para gerenciar partidas do jogo Textris.
#
#  Contém a classe `Partida` para lidar com a lógica de jogo, incluindo controle
#  das peças, grade, pontuação e ações do jogador.

## Classe que representa uma partida do jogo Textris.
#
#  Gerencia a lógica do jogo, incluindo a grade, peças, pontuação e controles do jogador.
class Partida:
    ## O construtor.
    #  @param self O objeto da classe.
    #  @param linhas Número de linhas na grade.
    #  @param colunas Número de colunas na grade.
    #  @param jogador Nome do jogador.
    #  @param mapa Estado inicial da grade (None para nova partida).
    #  @param pontuacao Pontuação inicial (None para iniciar com 0).
    def __init__(self, linhas, colunas, jogador, mapa, pontuacao):
        if mapa == None:
            ## Grade da nova partida ou de partida pré-carregada
            self.grade = [[" " for _ in range(colunas)] for _ in range(linhas)]
        else:
            self.grade = mapa
        ## Número de linhas da grade
        self.linhas = linhas
        ## Número de colunas da grade
        self.colunas = colunas
        ## Nome do jogador da partida
        self.jogador = jogador
        ## Peça atual que o jogador controla
        self.peca_atual = Peca(colunas)
        ## Estado do jogo
        self.jogo_ativo = True
        if pontuacao == None:
            ## Pontuação da partida
            self.pontuacao = 0
        else:
            self.pontuacao = pontuacao

    ## Inicia o loop principal do jogo.
    #
    #  O jogo continua até que o jogador encerre manualmente ou uma condição
    #  de Game Over seja atingida.
    #  @param self O objeto da classe.
    #  @return Pontuação final do jogador.
    def jogar(self):
        while self.jogo_ativo:
            Tela.limpar_tela()  

            if not self.peca_atual.posicionarTabuleiro(self.grade):
                self.jogo_ativo = False
                Tela.limpar_tela()
                Tela.exibir(self.grade, self.pontuacao)
                print("Game Over!")
                return self.pontuacao

            Tela.exibir(self.grade, self.pontuacao)

            while self.peca_atual.podeMover(self.grade, 0, 1):
                tecla = readkey() 
                if tecla == 's':
                    return self.pontuacao
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
                    return self.pontuacao
                else:
                    continue
                Tela.limpar_tela()
                Tela.exibir(self.grade, self.pontuacao)

                if not self.peca_atual.podeMover(self.grade, 0, 1):
                    self.peca_atual.posicionarTabuleiro(self.grade)
                    linhas_removidas = self.removerLinhas()
                    self.pontuacao += linhas_removidas * 100
                    self.peca_atual = Peca(self.colunas)
    
    ## Remove linhas completas do tabuleiro.
    #
    #  Filtra as linhas do tabuleiro para manter apenas as que contêm espaços vazios.
    #  Linhas completas são substituídas por novas linhas vazias no topo do tabuleiro.
    #  @param self O objeto da classe.
    #  @return Número de linhas removidas.
    def removerLinhas(self):

        novas_linhas = [linha for linha in self.grade if " " in linha]
        linhas_removidas = len(self.grade) - len(novas_linhas)
        self.grade = [[" " for _ in range(self.colunas)] for _ in range(linhas_removidas)] + novas_linhas
        return linhas_removidas 

    ## Salva o estado atual do jogo em um arquivo.
    #
    #  O arquivo de salvamento inclui as dimensões do tabuleiro, o nome do jogador,
    #  a pontuação atual e o estado do tabuleiro.
    #  @param self O objeto da classe.
    #  @note O estado do tabuleiro é salvo linha por linha.
    def salvar_jogo(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"{self.jogador}_{timestamp}.txt"

        with open(nome_arquivo, "w") as f:
            f.write(f"{self.linhas}\n")  
            f.write(f"{self.colunas}\n") 
            f.write(f"{self.jogador}\n")  
            f.write(f"{self.pontuacao}\n")  

            for linha in self.grade:
                f.write("".join(linha) + "\n")
    
        print(f"Jogo salvo em: {nome_arquivo}")


## @package tela
#  Módulo utilitário para exibir e atualizar a interface do jogo no terminal.
#
#  Contém a classe `Tela` para manipulação da exibição da grade do jogo e da pontuação.

## Classe utilitária para gerenciar a interface do jogo no terminal.
#
#  Oferece métodos estáticos para limpar a tela e exibir a grade do jogo e a pontuação.
class Tela:
    ## Limpa a tela do terminal.
    #
    #  Executa o comando apropriado para limpar a tela, dependendo do sistema operacional.
    @staticmethod
    def limpar_tela():
        os.system('cls||clear')

    ## Exibe a grade do jogo no terminal junto com a pontuação.
    #
    #  Desenha a grade com bordas, mostra a pontuação atual e exibe os comandos disponíveis.
    #  @param grade Matriz representando a grade do jogo.
    #  @param pontuacao Pontuação atual do jogador.
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
        

## @package jogo
#  Módulo para gerenciar o fluxo principal do jogo, incluindo menu e ranking.
#
#  A classe `Jogo` oferece funcionalidades para iniciar, carregar e gerenciar o jogo, 
#  além de exibir o menu principal e o ranking de pontuações.

## Classe para gerenciar o fluxo principal do jogo, incluindo menu e ranking.
#
#  Esta classe gerencia as operações principais do jogo, como iniciar novas partidas, 
#  carregar partidas salvas e exibir o ranking.
class Jogo:
    ## Construtor da classe Jogo.
    #
    #  Inicializa o ranking do jogo.
    def __init__(self):
        ## Ranking do Jogo atual
        self.ranking = Ranking()
    
    ## Exibe o menu principal do jogo.
    #
    #  O método exibe as opções para iniciar uma nova partida, carregar uma partida salva,
    #  ver as 10 melhores pontuações ou sair do jogo.
    def menu(self):
        while True:
            Tela.limpar_tela()  
            print("*** Jogo Textris - um Tetris em modo texto ***")
            print("Opções do jogo:")
            print("- <i> para iniciar uma nova partida")
            print("- <c> para carregar uma partida gravada e continuá-la")
            print("- <p> para ver as 10 melhores pontuações")
            print("- <s> para sair do jogo")
            opcao = input("Digite a opção desejada: ").strip().lower()

            if opcao == "i":
                self.iniciar_partida()
            elif opcao == "c":
                nome_arquivo = input("Digite o nome do arquivo: ").strip()
                self.carregarPartida(nome_arquivo)
            elif opcao == "p":
                self.ranking.exibir()
            elif opcao == "s":
                print("Saindo do jogo. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    ## Inicia uma nova partida.
    #
    #  Solicita o nome do jogador, o número de linhas e colunas da tela do jogo,
    #  cria o jogador e inicia a partida.
    def iniciar_partida(self):
        
        nome_jogador = input("Digite o nome do jogador: ").strip()
        linhas = int(input("Digite o número de linhas da tela do jogo: "))
        colunas = int(input("Digite o número de colunas da tela do jogo: "))
        jogador = Jogador(nome_jogador)

        partida = Partida(linhas, colunas, jogador.nome, None, None)

        jogador.pontuacao = partida.jogar()

        self.ranking.adicionar(jogador.nome, jogador.pontuacao)
        self.ranking.salvar()

    ## Carrega o estado de uma partida salva a partir de um arquivo.
    #
    #  O método restaura as dimensões do tabuleiro, nome do jogador, pontuação
    #  e o estado do tabuleiro a partir de um arquivo salvo.
    #
    #  @param nome_arquivo Nome do arquivo onde a partida foi salva.
    def carregarPartida(self, nome_arquivo):
        try:
            with open(nome_arquivo, "r") as f:
                linhas = int(f.readline().strip())
                colunas = int(f.readline().strip())
                jogador = Jogador(None)
                jogador.nome = str(f.readline().strip())
                jogador.pontuacao = int(f.readline().strip())

                grade = []
                for linha in f:
                    linha = linha.rstrip('\n') 
                    nova_linha = []
                    for char in linha:  
                        nova_linha.append(char)
                    grade.append(nova_linha)  
        except FileNotFoundError:
            print("Nenhuma partida salva encontrada.")
        
        partida = Partida(linhas, colunas, jogador.nome, grade, jogador.pontuacao)
        jogador.pontuacao = partida.jogar()
        self.ranking.adicionar(jogador.nome, jogador.pontuacao)
        self.ranking.salvar()


## @package jogador
#  Módulo que define a classe Jogador.
#
#  A classe `Jogador` é responsável por armazenar o nome e a pontuação de um jogador no jogo.

## Classe para gravar informações pertinentes ao Jogador: nome e pontuação.
#
#  A classe `Jogador` armazena o nome e a pontuação do jogador, permitindo que essas informações
#  sejam manipuladas durante o fluxo do jogo.
class Jogador:
    ## Construtor da classe Jogador.
    #
    #  Inicializa o nome e a pontuação do jogador.
    #
    #  @param nome (str): Nome do jogador.
    def __init__(self, nome):
        ## Nome do Jogador
        self.nome = nome
        ## Pontuação do Jogador
        self.pontuacao = 0


## @package ranking
#  Módulo que define a classe Ranking.
#
#  A classe `Ranking` é responsável por armazenar e manipular as pontuações dos jogadores, além de
#  salvar e carregar o ranking a partir de um arquivo.

## Classe para gravar o Ranking de pontuações.
#
#  A classe `Ranking` gerencia as pontuações dos jogadores, armazenando as pontuações em um arquivo e
#  permitindo que o ranking seja exibido, salvo e carregado.

class Ranking:
    ## Construtor da classe Ranking.
    #
    #  Inicializa o ranking carregando as pontuações do arquivo especificado ou cria um novo ranking.
    #
    #  @param caminho_arquivo (str): Caminho do arquivo onde o ranking é armazenado. O valor padrão é 'ranking.txt'.
    def __init__(self, caminho_arquivo='ranking.txt'):
        ## Pontuações do ranking
        self.pontuacoes = self.carregar(caminho_arquivo)

    ## Adiciona nova pontuação ao ranking.
    #
    #  Adiciona uma nova pontuação ao ranking e ordena as pontuações em ordem decrescente.
    #
    #  @param nome (str): Nome do jogador.
    #  @param pontuacao (int): Pontuação do jogador. Deve ser um número inteiro.
    def adicionar(self, nome, pontuacao):
        if not isinstance(pontuacao, int):
            raise ValueError(f"Pontuação inválida: {pontuacao}. Deve ser um inteiro.")

        ## Pontuações do ranking
        self.pontuacoes.append((nome, pontuacao))

        pontuacoes = self.pontuacoes
    
        for item in pontuacoes:
            if not isinstance(item[1], int):
                raise ValueError(f"Pontuação inválida no ranking: {item}. Deve ser um inteiro.")

        self.pontuacoes.sort(key=lambda x: x[1], reverse=True)

    ## Salva o top 10 do ranking no arquivo ranking.txt.
    #
    #  O ranking é salvo no arquivo, com as 10 melhores pontuações.
    def salvar(self):
        with open("ranking.txt", "w") as f:
            for nome, pontuacao in self.pontuacoes[:10]:
                f.write(f"{nome},{pontuacao}\n")

    ## Carrega os dados do ranking a partir de um arquivo.
    #
    #  Tenta abrir o arquivo especificado e carregar os dados do ranking. Caso o arquivo não seja encontrado,
    #  um novo ranking vazio é criado.
    #
    #  @param caminho_arquivo (str): Caminho do arquivo onde o ranking é armazenado.
    #
    #  @returns list: Uma lista de tuplas contendo o nome e a pontuação dos jogadores, ordenada por pontuação.
    def carregar(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r') as arquivo:
                pontuacoes = []
                for linha in arquivo:
                    dados = linha.strip().split(',')
                    if len(dados) != 2:
                        raise ValueError(f"Formato inválido no arquivo: {linha}")

                    nome = dados[0]
                    try:
                        pontuacao = int(dados[1]) 
                    except ValueError:
                        raise ValueError(f"Pontuação inválida no arquivo: {dados[1]}. Deve ser um número inteiro.")

                    pontuacoes.append((nome, pontuacao))

                pontuacoes.sort(key=lambda x: x[1], reverse=True)
                return pontuacoes
        except FileNotFoundError:
            print(f"Arquivo {caminho_arquivo} não encontrado. Criando um novo ranking.")
            return []

    ## Exibe o ranking atual.
    #
    #  Exibe as 10 melhores pontuações ou uma mensagem indicando que não há pontuações registradas.
    def exibir(self):
        if not self.pontuacoes:
            print("Nenhuma pontuação registrada ainda.")
        else:
            print("Ranking:")
            for i, (nome, pontuacao) in enumerate(self.pontuacoes[:10], 1):
                print(f"{i}. {nome} - {pontuacao} pontos")
        input("Pressione Enter para continuar...")


if __name__ == "__main__":
    ## Objeto Jogo
    jogo = Jogo()
    jogo.menu()

