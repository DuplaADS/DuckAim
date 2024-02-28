# importando
import pygame
from sys import exit

pygame.init()
pygame.font.init()


# Variaveis:
# ----FPS----
relogio = pygame.time.Clock()
# ----Texto----
comicsans = pygame.font.SysFont("comicsans", 50)
branco = (255, 255, 255)

vida_amarelo = 3
vida_azul = 3


# ----Gravidade----
gravidade_amarelo = 0
gravidade_azul = 0


# ----Sobre_Tiros-----
balas_amarelas = []
balas_azuis = []


# Superficies:

# ---- IMAGENS ----
janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Duck Aim")

background = pygame.image.load("imagens/background.jpg")
amarelo = pygame.image.load("imagens/amarelo.png")
azul = pygame.image.load("imagens/azul.png")
tiro_amarelo = pygame.image.load("imagens/tiro_amarelo.png")
tiro_azul = pygame.image.load("imagens/tiro_azul.png")

# -----Retangulos (HitBox)----
rect_amarelo = pygame.Rect(700, 631, 40, 64)
rect_azul = pygame.Rect(40, 631, 40, 64)

# Funções:

def desenhar(tiros_amarelos, tiros_azuis, disparo_am, disparo_az, hp1, hp2):
    janela.blit(background, (0, 0))
    janela.blit(amarelo, rect_amarelo)
    janela.blit(azul, rect_azul)

    for balas in tiros_amarelos:
        janela.blit(disparo_am, balas)
    for balas in tiros_azuis:
        janela.blit(disparo_az, balas)

    txt_vida_amarelo = comicsans.render("HP: " + str(hp1), 1, branco)
    txt_vida_azul = comicsans.render("HP: " + str(hp2), 1, branco)
    janela.blit(txt_vida_amarelo, (670, 0))
    janela.blit(txt_vida_azul, (0, 0))

# ---- Player ----
def player(rect, left, right, down):

    if rect.bottom >= 567:
        rect.bottom = 567
    if pygame.key.get_pressed()[left]:
        rect.x -= 8
    if pygame.key.get_pressed()[right]:
        rect.x += 8
    if pygame.key.get_pressed()[down] and rect.bottom < 567:
        rect.y += 12



VelAmarelas = -12
VelAzuis = 12
# ---- Atirando ----
def atirar(listatiros, vel, inimigo, hp_inimigo):

    for b in listatiros:
        b.x += vel
        if b.colliderect(inimigo):
            listatiros.remove(b)
            hp_inimigo -= 1
        elif b.x < 0 or b.x > 800:
            listatiros.remove(b)
    return hp_inimigo


# Looping de atualização da tela (jogo em si)
while True:
    pygame.display.update()
    relogio.tick(60)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and rect_amarelo.bottom == 567:
                gravidade_amarelo = -20

            if event.key == pygame.K_w and rect_azul.bottom == 567:
                gravidade_azul = -20

            if event.key == pygame.K_RSHIFT and len(balas_amarelas) < 2:
                bala = pygame.Rect(rect_amarelo.x, rect_amarelo.y + 32, 15, 8)
                balas_amarelas.append(bala)

            if event.key == pygame.K_LSHIFT and len(balas_azuis) < 2:
                bala = pygame.Rect(rect_azul.x + 32, rect_azul.y + 32, 15, 8)
                balas_azuis.append(bala)

    # Parte Visual
    desenhar(balas_amarelas, balas_azuis, tiro_amarelo, tiro_azul, vida_amarelo, vida_azul)

# Current Game
    if vida_amarelo != 0 and vida_azul != 0:

        # Players (Gravidade e Movimentos)
        gravidade_amarelo += 1
        gravidade_azul += 1
        rect_amarelo.y += gravidade_amarelo
        rect_azul.y += gravidade_azul

        # Players
        player(rect_amarelo, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN)
        player(rect_azul, pygame.K_a, pygame.K_d, pygame.K_s)

        # Atirando
        vida_azul = atirar(balas_amarelas, VelAmarelas, rect_azul, vida_azul)
        vida_amarelo = atirar(balas_azuis, VelAzuis, rect_amarelo, vida_amarelo)

        # Barreira (pato)
        if rect_amarelo.left <= 400:
            rect_amarelo.left = 400
        elif rect_amarelo.right >= 800:
            rect_amarelo.right = 800
        # Barreira (pata)
        if rect_azul.right >= 400:
            rect_azul.right = 400
        elif rect_azul.left <= 0:
            rect_azul.left = 0


    # GameOver
    else:
        if vida_amarelo == 0:
            game_over = comicsans.render("Azul venceu", 1, branco)
            janela.blit(game_over, (270, 300))
        elif vida_azul == 0:
            game_over = comicsans.render("Amarelo Venceu", 0, branco)
            janela.blit(game_over, (200, 300))
