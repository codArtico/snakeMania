import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os

pygame.init()  # Inicia o pygame

# Função para obter o caminho relativo dos recursos (som e imagens)
def resource_path(relative_path):
    # Base path será usado para encontrar os arquivos dentro do executável ou fora
    try:
        # Quando empacotado com PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Quando rodando diretamente no Python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Musica de fundo
bgMusic = pygame.mixer.music.load(resource_path('sons/bg.mp3'))  # Carrega a musica
pygame.mixer.music.play()

# Configs de efeitos sonoros
sfxEat = pygame.mixer.Sound(resource_path('sons/smb_coin.wav'))  # Carrega o sfx de colisão
sfxLvlUp = pygame.mixer.Sound(resource_path('sons/smb_powerup.wav'))

# Configs de imagens
icon = pygame.image.load(resource_path('imagens/logo.png'))  # Icone em cima
# bg = pygame.image.load(resource_path('imagens/bgTela.png'))  # Fundo da tela (quando disponível)
fonte = pygame.font.SysFont('arial', 40, True, False)  # Fonte, tamanho, negrito, itálico
pygame.display.set_caption("Snake Mania")  # Muda o nome em cima do jogo
pygame.display.set_icon(icon)

# Configs de tela
largura = 1550
altura = 800
tela = pygame.display.set_mode((largura, altura))  # Seta o tamanho da Janela

# Configs de movimentação
xControl = 20
yControl = 0
velocidade = 5

# Relógio pra FPS
relogio = pygame.time.Clock()

# Função pra aumentar o tamanho
def comer(listaCobra):
    for XeY in listaCobra:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))

# Função pra zerar todas as variáveis, iniciando um novo jogo
def novoJogo():
    global pts, comprimento, x, y, listaCabeca, listaCobra, x_maca, y_maca, killed
    pts = 0
    comprimento = 10
    x = int(largura / 2)
    y = int(altura / 2)
    listaCabeca = [x, y]
    listaCobra = []
    x_maca = randint(40, largura - 40)
    y_maca = randint(50, altura - 50)
    killed = False


def tela_inicial():
    fonte_inicio = pygame.font.SysFont('arial', 60, True, False)
    fonte_subtitulo = pygame.font.SysFont('arial', 40, True, False)
    while True:
        tela.fill((0, 0, 0))
        mensagem = "Bem-vindo ao Snake Mania!"
        subtitulo = "Pressione Enter para começar"

        texto_inicio = fonte_inicio.render(mensagem, True, (255, 255, 255))
        texto_subtitulo = fonte_subtitulo.render(subtitulo, True, (0, 255, 0))

        ret_texto_inicio = texto_inicio.get_rect(center=(largura // 2, altura // 2 - 50))
        ret_texto_subtitulo = texto_subtitulo.get_rect(center=(largura // 2, altura // 2 + 50))

        tela.blit(texto_inicio, ret_texto_inicio)
        tela.blit(texto_subtitulo, ret_texto_subtitulo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        pygame.display.update()


tela_inicial()
novoJogo()
while True:
    relogio.tick(60)  # Ajuste de FPS
    # tela.blit(bg, (0, 0))  # Fundo da tela (quando disponível)
    tela.fill((0, 0, 0))  # Background Fill

    # Config Msg de Pontuação
    mensagem = f'Pontos: {pts}'
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))  # mensagem, cor

    for event in pygame.event.get():  # Código para o botão de fechar funcionar
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Configurando WASD
    if pygame.key.get_pressed()[pygame.K_a]:
        if xControl == velocidade:
            pass
        else:
            xControl = -velocidade
            yControl = 0
    if pygame.key.get_pressed()[pygame.K_d]:
        if xControl == -velocidade:
            pass
        else:
            xControl = velocidade
            yControl = 0
    if pygame.key.get_pressed()[pygame.K_w]:
        if yControl == velocidade:
            pass
        else:
            xControl = 0
            yControl = -velocidade
    if pygame.key.get_pressed()[pygame.K_s]:
        if yControl == -velocidade:
            pass
        else:
            xControl = 0
            yControl = velocidade

    # Configurando Setas
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if xControl == velocidade:
            pass
        else:
            xControl = -velocidade
            yControl = 0
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if xControl == -velocidade:
            pass
        else:
            xControl = velocidade
            yControl = 0
    if pygame.key.get_pressed()[pygame.K_UP]:
        if yControl == velocidade:
            pass
        else:
            xControl = 0
            yControl = -velocidade
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if yControl == -velocidade:
            pass
        else:
            xControl = 0
            yControl = velocidade

    x = x + xControl
    y = y + yControl

    # Criando objeto controlado pelo WASD (Utilizando X e Y)
    meuPersonagem = pygame.draw.rect(tela, (0, 255, 0), (x, y, 20, 20))

    # Criando objeto para colisão
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    # Comendo (Colidindo com a maçã)
    if meuPersonagem.colliderect(maca):
        x_maca = randint(40, largura - 40)
        y_maca = randint(50, altura - 50)
        pts += 1
        sfxEat.play()
        if pts % 10 == 0 and pts != 0:
            sfxLvlUp.play()
        comprimento += 1

    # Armazenando dados para onde está a cabeça da cobra
    listaCabeca = [x, y]

    # Adicionando a cabeça da cobra ao seu corpo
    listaCobra.append(listaCabeca)

    # Condição de morte
    if listaCobra.count(listaCabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'Game over! Pressione r para jogar novamente!'
        texto_formatado = fonte2.render(mensagem, True, (255, 255, 255))
        ret_texto = texto_formatado.get_rect()
        killed = True
        while killed:
            tela.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        novoJogo()
            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    # Condições para loop nas bordas
    if x > largura:
        x = 0
    if y > altura:
        y = 0
    if x < 0:
        x = largura
    if y < 0:
        y = altura
    if len(listaCobra) > comprimento:
        del listaCobra[0]

    comer(listaCobra)

    # Mostrando pontuação
    tela.blit(texto_formatado, (largura - 250, altura - 750))

    # Atualizando tela
    pygame.display.update()
