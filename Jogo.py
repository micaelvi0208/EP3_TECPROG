"""
Este programa é uma implementação em Python de um jogo semelhante ao Tetris chamado 'Textris'. 
O jogo é exibido no terminal e permite que o jogador mova, rotacione e manipule peças que caem 
em uma grade. Além disso, o programa suporta funcionalidades como salvar e carregar partidas, 
manter um ranking de pontuações e exibir um menu interativo.

Classes Principais:
- Peca: Representa uma peça do jogo, incluindo seu tipo, posição, e lógica para movimento e rotação.
- Partida: Gerencia uma partida individual do jogo, incluindo a lógica de atualização da grade, 
  remoção de linhas completas e pontuação.
- Tela: Responsável por exibir a interface do jogo no terminal e limpar a tela.
- Jogo: Gerencia o fluxo principal do jogo, incluindo o menu principal, iniciar novas partidas 
  e carregar partidas salvas.

Constantes:
- TETROMINOES: Define as formas das peças do jogo em termos de coordenadas relativas.

Dependências:
- readchar: Biblioteca usada para detectar entradas de teclado de forma interativa.
- os: Usada para limpar a tela do terminal dependendo do sistema operacional.
- random: Utilizada para selecionar peças aleatórias.
- datetime: Utilizada para manipular datas e horários
"""

import os
import random
from readchar import readkey, key
import datetime



# Definição das formas das peças (Tetrominoes) com coordenadas relativas
TETROMINOES = {
    'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
    'L': [(0, 1), (1, 1), (2, 1), (2, 2)],
    'J': [(0, 1), (1, 1), (2, 1), (2, 0)],
    'S': [(1, 0), (1, 1), (0, 1), (0, 2)],
    'Z': [(0, 0), (0, 1), (1, 1), (1, 2)]
}


# Classe que representa uma peça no jogo
class Peca:
    """
    Representa uma peça Tetromino no jogo, com funcionalidade para posicionamento, 
    movimento e rotação.
    """
    def __init__(self, colunas):
        """
        Inicializa uma peça com forma e símbolo aleatórios.
        A peça começa no topo central da grade.

        Args:
        - colunas (int): Número de colunas na grade do jogo.
        """
        self.forma = random.choice(list(TETROMINOES.keys()))

        """Define o símbolo da peça com base em sua forma."""
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
        
        """ Coordenadas do centro superior da grade """
        self.x = int (colunas/2)
        self.y = 0
    
    def posicionarTabuleiro(self, tabuleiro):
        """
        Posiciona a peça na grade do tabuleiro.

        Args:
        - tabuleiro (list): Matriz representando a grade do jogo.

        Returns:
        - bool: True se o posicionamento for bem-sucedido, False caso contrário.
        """
        coord = TETROMINOES[self.forma] # Coordenadas relativas
        for dx, dy in coord:
            # Coordenadas na grade
            x_pos = self.x + dx
            y_pos = self.y + dy
            # Verifica se a posição está disponível
            if tabuleiro[y_pos][x_pos] != ' ':
                return False
        for dx, dy in coord:
            # Insere no tabuleiro
            x_pos = self.x + dx
            y_pos = self.y + dy
            tabuleiro[y_pos][x_pos] = self.simbolo
        return True

    def moverPeca(self,tabuleiro,dx,dy):
        """
    Move a peça no tabuleiro na direção especificada.

    Args:
        tabuleiro (list[list[str]]): Representação do tabuleiro.
        dx (int): Deslocamento na direção horizontal.
        dy (int): Deslocamento na direção vertical.
    """
        self.apagaAnterior(tabuleiro) # Remove a peça na posição atual
        self.x += dx # Atualiza posição horizontal
        self.y += dy # Atualiza posição vertical
        self.posicionarTabuleiro(tabuleiro) # Insere no tabuleiro na nova posição

    def apagaAnterior(self, tabuleiro):
        """
    Remove a peça da posição atual no tabuleiro, substituindo por espaços vazios.

    Args:
        tabuleiro (list[list[str]]): Representação do tabuleiro.
    """
        coord = TETROMINOES[self.forma] # Obtém as coordenadas relativas da peça
        for dx, dy in coord:
            # Calcula posições no tabuleiro
            x_pos = self.x + dx
            y_pos = self.y + dy
            tabuleiro[y_pos][x_pos] = ' ' # Substitui por espaços vazios
    
    def podeMover(self, tabuleiro, dx, dy):
        """
    Verifica se a peça pode se mover para a nova posição sem colisões ou ultrapassar os limites do tabuleiro.

    Args:
        tabuleiro (list[list[str]]): Representação do tabuleiro.
        dx (int): Deslocamento na direção horizontal.
        dy (int): Deslocamento na direção vertical.

    Returns:
        bool: True se o movimento for válido, False caso contrário.
    """
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
        """
    Rotaciona a peça no tabuleiro, caso possível.

    Args:
        tabuleiro (list[list[str]]): Representação do tabuleiro.
        sentido_horario (bool): Se True, rotaciona no sentido horário; se False, anti-horário.
    """
        if self.forma == 'O':  # O não precisa rotacionar
            return

        # Calcular novas coordenadas para a rotação
        novas_coordenadas = []
        for dx, dy in TETROMINOES[self.forma]:
            if sentido_horario:
                novas_coordenadas.append((-dy, dx))  # Rotação no sentido horário
            else:
                novas_coordenadas.append((dy, -dx))  # Rotação no sentido anti-horário)

        backup = novas_coordenadas
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
            TETROMINOES[self.forma] = backup


class Partida:
    """
    Representa uma partida do jogo Textris. Gerencia a lógica do jogo, incluindo
    a grade, peças, pontuação e controles do jogador.
    """
    def __init__(self, linhas, colunas, jogador, mapa, pontuacao):
        """
        Inicializa uma partida com grade, jogador e pontuação.

        Args:
        - linhas (int): Número de linhas na grade.
        - colunas (int): Número de colunas na grade.
        - jogador (str): Nome do jogador.
        - mapa (list): Estado da grade (None para nova partida).
        - pontuacao (int): Pontuação inicial (None para 0).
        """
        # Distingue se é nova partida ou se está carregando uma partida antiga
        if mapa == None:
            self.grade = [[" " for _ in range(colunas)] for _ in range(linhas)]
        else:
            self.grade = mapa
        self.linhas = linhas
        self.colunas = colunas
        self.jogador = jogador
        self.peca_atual = Peca(colunas)
        self.jogo_ativo = True
        # Distingue se é nova partida ou se está carregando uma partida antiga
        if pontuacao == None:
            self.pontuacao = 0
        else:
            self.pontuacao = pontuacao

    def jogar(self):
        #self.peca_atual = self.gerar_peca()
        while self.jogo_ativo:
            Tela.limpar_tela()  # Limpa a tela antes de exibir a atualização

            # Verifica se não é possível posicionar nova peça no tabuleiro.
            # Essa situação implica que a partida acabou
            if not self.peca_atual.posicionarTabuleiro(self.grade):
                self.jogo_ativo = False
                Tela.limpar_tela()
                Tela.exibir(self.grade, self.pontuacao)
                print("Game Over!")
                return self.pontuacao

            # Exibe tela atualizada
            Tela.exibir(self.grade, self.pontuacao)

            # Laço para receber comandos na partida enquanto a peça não atinge o chão
            while self.peca_atual.podeMover(self.grade, 0, 1):
                tecla = readkey() # Leitura da tecla
                if tecla == 's':
                    # Sair do jogo
                    return self.pontuacao
                elif tecla == key.DOWN:
                    # Mover para baixo
                    if self.peca_atual.podeMover(self.grade, 0, 1):
                        self.peca_atual.moverPeca(self.grade, 0, 1)
                elif tecla == key.RIGHT:
                    # Mover para a direita
                    if self.peca_atual.podeMover(self.grade, 1, 0):
                        self.peca_atual.moverPeca(self.grade, 1, 0)
                elif tecla == key.LEFT:
                    # Mover para a esquerda
                    if self.peca_atual.podeMover(self.grade, -1, 0):
                        self.peca_atual.moverPeca(self.grade, -1, 0)
                elif tecla == key.PAGE_UP:
                    # Rotaciona sentido horário
                    self.peca_atual.rotacionar(self.grade, sentido_horario=True)
                elif tecla == key.PAGE_DOWN:
                    # Rotaciona sentido anti-horário
                    self.peca_atual.rotacionar(self.grade, sentido_horario=False)
                elif tecla == 'g':
                    # Grava partida e sai do jogo
                    self.peca_atual.apagaAnterior(self.grade)
                    self.salvar_jogo()
                    return self.pontuacao
                else:
                    # Tecla sem comando
                    continue
                Tela.limpar_tela()
                Tela.exibir(self.grade, self.pontuacao)

                # Verifica se completou uma ou mais linhas
                if not self.peca_atual.podeMover(self.grade, 0, 1):
                    self.peca_atual.posicionarTabuleiro(self.grade)
                    linhas_removidas = self.removerLinhas()
                    self.pontuacao += linhas_removidas * 100
                    self.peca_atual = Peca(self.colunas)
    
    def removerLinhas(self):
        # Remoção de linhas completas

        # Filtra as linhas do tabuleiro, mantendo apenas aquelas que contêm espaços vazios (' ').
        novas_linhas = [linha for linha in self.grade if " " in linha]
        # Calcula a quantidade de linhas removidas ao comparar o tamanho original com o novo.
        linhas_removidas = len(self.grade) - len(novas_linhas)
        # Adiciona linhas vazias no topo para manter o tamanho original do tabuleiro.
        self.grade = [[" " for _ in range(self.colunas)] for _ in range(linhas_removidas)] + novas_linhas
        return linhas_removidas # retorna o número de linhas removidas

    def salvar_jogo(self):
        """
        Salva o estado atual do jogo em um arquivo cujo nome segue o formato:
        [nome do jogador] + [data e hora da gravação].txt.

        O arquivo contém as informações essenciais para retomar o jogo:
        - Dimensões do tabuleiro (linhas e colunas).
        - Nome do jogador.
        - Pontuação atual.
        - Estado do tabuleiro (grade).
        """
        # Gerar o nome do arquivo com base no nome do jogador e data/hora atual
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"{self.jogador}_{timestamp}.txt"

        # Abrir o arquivo no modo de escrita e salvar as informações do jogo
        with open(nome_arquivo, "w") as f:
            f.write(f"{self.linhas}\n")  # Número de linhas do tabuleiro
            f.write(f"{self.colunas}\n")  # Número de colunas do tabuleiro
            f.write(f"{self.jogador}\n")  # Nome do jogador
            f.write(f"{self.pontuacao}\n")  # Pontuação atual

            # Salvar o estado do tabuleiro (grade)
            for linha in self.grade:
                f.write("".join(linha) + "\n")
    
        print(f"Jogo salvo em: {nome_arquivo}")


class Tela:
    """
    Classe utilitária para exibir e atualizar a interface do jogo no terminal.
    """
    @staticmethod
    def limpar_tela():
        # Limpa a tela dependendo do sistema operacional
        os.system('cls||clear')

    @staticmethod
    def exibir(grade, pontuacao):
        """
        Exibe a grade do jogo no terminal, junto com a pontuação.

        Args:
        - grade (list): Matriz representando a grade do jogo.
        - pontuacao (int): Pontuação atual do jogador.
        """
        print("—" * (len(grade[0]) + 2))
        for linha in grade:
            print("|" + "".join(linha) + "|")
        print("—" * (len(grade[0]) + 2))
        print(f"Pontuação: {pontuacao}")
        print("\nComandos: ←, →, ↓, s (sair)")
        print("<Page Down> rotaciona esquerda | <Page Up> rotaciona direita")
        print("<s> sai da partida, <g> grava e sai da partida")
        

class Jogo:
    """
    Gerencia o fluxo principal do jogo, incluindo menu e ranking.
    """
    def __init__(self):
        self.ranking = Ranking()
    
    def menu(self):
        """Exibe o menu principal do jogo."""
        while True:
            Tela.limpar_tela()  # Limpa a tela antes de exibir o menu
            print("*** Jogo Textris - um Tetris em modo texto ***")
            print("Opções do jogo:")
            print("- <i> para iniciar uma nova partida")
            print("- <c> para carregar uma partida gravada e continuá-la")
            print("- <p> para ver as 10 melhores pontuações")
            print("- <s> para sair do jogo")
            opcao = input("Digite a opção desejada: ").strip().lower()

            if opcao == "i":
                # INICIAR PARTIDA
                self.iniciar_partida()
            elif opcao == "c":
                # CARREGAR PARTIDA
                nome_arquivo = input("Digite o nome do arquivo: ").strip()
                self.carregarPartida(nome_arquivo)
            elif opcao == "p":
                # EXIBIÇÃO DO TOP 10 DO RANKING
                self.ranking.exibir()
            elif opcao == "s":
                # SAIR DO JOGO
                print("Saindo do jogo. Até logo!")
                break
            else:
                # Tecla sem função
                print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

    def iniciar_partida(self):
        # Função que inicia nova partida

        # Insere os valores para construir a partida
        nome_jogador = input("Digite o nome do jogador: ").strip()
        linhas = int(input("Digite o número de linhas da tela do jogo: "))
        colunas = int(input("Digite o número de colunas da tela do jogo: "))
        jogador = Jogador(nome_jogador)

        # Construção da partida
        partida = Partida(linhas, colunas, jogador.nome, None, None)

        # Inicia a partida
        jogador.pontuacao = partida.jogar()

        # Adiciona a pontuação ao ranking e o salva
        self.ranking.adicionar(jogador.nome, jogador.pontuacao)
        self.ranking.salvar()

    def carregarPartida(self, nome_arquivo):
        """
    Carrega o estado de um jogo salvo a partir de um arquivo.

    Argumentos:
        nome_arquivo (str): Nome do arquivo onde o jogo foi salvo.
    
    O método restaura as dimensões do tabuleiro, nome do jogador, pontuação
    e o estado do tabuleiro.
    """
        
        # Tenta abrir o arquivo em questão
        try:
            with open(nome_arquivo, "r") as f:
                # Pega os valores na ordem em que foram gravados
                linhas = int(f.readline().strip())
                colunas = int(f.readline().strip())
                jogador = Jogador(None)
                jogador.nome = str(f.readline().strip())
                jogador.pontuacao = int(f.readline().strip())

                # Inicia o tabuleiro
                grade = []
                # Pega as linhas que compõem o tabuleiro
                for linha in f:
                    linha = linha.rstrip('\n')  # Remove o '\n'
                    # Inicia cada linha do tabuleiro
                    nova_linha = []
                    for char in linha:  # Lê cada caractere individualmente
                        nova_linha.append(char)
                    grade.append(nova_linha)  # Adiciona a nova linha formatada à grade
        except FileNotFoundError:
            # Caso o arquivo não for encontrado
            print("Nenhuma partida salva encontrada.")
        
        # Construção da partida
        partida = Partida(linhas, colunas, jogador.nome, grade, jogador.pontuacao)
        # Inicia partida
        jogador.pontuacao = partida.jogar()
        # Adiciona pontuação ao ranking e o salva
        self.ranking.adicionar(jogador.nome, jogador.pontuacao)
        self.ranking.salvar()


class Jogador:
    """
    Classe para gravar informações pertinentes ao Jogador: nome e pontuação
    """
    def __init__(self, nome):
        self.nome = nome
        self.pontuacao = 0


class Ranking:
    """
    Classe para gravar o Ranking de pontuações
    """

    # Construção a partir de arquivo ranking.txt
    def __init__(self, caminho_arquivo='ranking.txt'):
        self.pontuacoes = self.carregar(caminho_arquivo)

    # Adiciona nova pontuação ao ranking
    def adicionar(self, nome, pontuacao):
        # Garantir que a pontuação seja um número inteiro
        if not isinstance(pontuacao, int):
            raise ValueError(f"Pontuação inválida: {pontuacao}. Deve ser um inteiro.")

        self.pontuacoes.append((nome, pontuacao))
    
        # Verificar consistência dos dados antes de ordenar
        for item in self.pontuacoes:
            if not isinstance(item[1], int):
                raise ValueError(f"Pontuação inválida no ranking: {item}. Deve ser um inteiro.")

        # Ordenar a lista com segurança
        self.pontuacoes.sort(key=lambda x: x[1], reverse=True)

    # Salva o top 10 do ranking atualizado no arquivo ranking.txt
    def salvar(self):
        with open("ranking.txt", "w") as f:
            for nome, pontuacao in self.pontuacoes[:10]:
                f.write(f"{nome},{pontuacao}\n")

    # Carrega os dados do ranking salvis
    def carregar(self, caminho_arquivo):
        # tenta abrir o arquivo
        try:
            with open(caminho_arquivo, 'r') as arquivo:
                # inicia a lista de pontuações
                pontuacoes = []
                for linha in arquivo:
                    # Pega os dados do arquivo: nome e pontuação
                    dados = linha.strip().split(',')
                    if len(dados) != 2:
                        raise ValueError(f"Formato inválido no arquivo: {linha}")

                    nome = dados[0]
                    try:
                        pontuacao = int(dados[1])  # Converter pontuação para inteiro
                    except ValueError:
                        raise ValueError(f"Pontuação inválida no arquivo: {dados[1]}. Deve ser um número inteiro.")

                    pontuacoes.append((nome, pontuacao))

                # Ordenar o ranking ao carregar
                pontuacoes.sort(key=lambda x: x[1], reverse=True)
                return pontuacoes
        # Caso não encontrar o arquivo
        except FileNotFoundError:
            print(f"Arquivo {caminho_arquivo} não encontrado. Criando um novo ranking.")
            return []

    # Exibição do Ranking
    def exibir(self):
        if not self.pontuacoes:
            print("Nenhuma pontuação registrada ainda.")
        else:
            print("Ranking:")
            for i, (nome, pontuacao) in enumerate(self.pontuacoes[:10], 1):
                print(f"{i}. {nome} - {pontuacao} pontos")
        input("Pressione Enter para continuar...")


# Execução da main
if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu()

