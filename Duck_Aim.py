# importando
import pygame
import os
from sys import exit

pygame.init()
pygame.font.init()

# --- Pegando Diretório atual ---
diretorio_atual = os.getcwd()

# Variaveis:
# ----FPS----
relogio = pygame.time.Clock()
# ----Texto----
comicsans = pygame.font.SysFont("comicsans", 50)
comicsansMenor = pygame.font.SysFont("comicsans", 30)
corBranca = (255, 255, 255)
corAmarela = (250, 241, 110) 
corRoxa = (210, 145, 250)

vida_amarelo = 3
vida_roxo = 3


# ----Gravidade----
gravidade_amarelo = 0
gravidade_roxo = 0


# ----Sobre_Tiros-----
balas_amarelas = []
balas_roxas = []

# --- SONS ---
diretorio_sons = os.path.join(diretorio_atual, "sons")

som_atirando = pygame.mixer.Sound(os.path.join(diretorio_sons, "shoot.wav"))
som_pulando = pygame.mixer.Sound(os.path.join(diretorio_sons, "jump.wav"))

# Superficies:
janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Duck Aim")

# ---- IMAGENS ----
diretorio_imagens = os.path.join(diretorio_atual, "imagens")

background = pygame.image.load(os.path.join(diretorio_imagens, "background.jpg"))
amarelo = pygame.image.load(os.path.join(diretorio_imagens, "amarelo.png"))
roxo = pygame.image.load(os.path.join(diretorio_imagens, "roxo.png"))
tiro_amarelo = pygame.image.load(os.path.join(diretorio_imagens, "tiro_amarelo.png"))
tiro_roxo = pygame.image.load(os.path.join(diretorio_imagens, "tiro_roxo.png"))

# -----Retangulos (HitBox)----
rect_amarelo = pygame.Rect(700, 631, 40, 64)
rect_roxo = pygame.Rect(40, 631, 40, 64)

# Funções:

def desenhar(tiros_amarelos, tiros_roxos, disparo_am, disparo_roxo, hp1, hp2):
    janela.blit(background, (0, 0))
    janela.blit(amarelo, rect_amarelo)
    janela.blit(roxo, rect_roxo)

    for balas in tiros_amarelos:
        janela.blit(disparo_am, balas)
    for balas in tiros_roxos:
        janela.blit(disparo_roxo, balas)

    txt_vida_amarelo = comicsans.render("HP: " + str(hp1), 1, corBranca)
    txt_vida_roxo = comicsans.render("HP: " + str(hp2), 1, corBranca)
    janela.blit(txt_vida_amarelo, (670, 0))
    janela.blit(txt_vida_roxo, (0, 0))

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
VelRoxas = 12
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

            if event.key == pygame.K_UP and rect_amarelo.bottom == 567 and vida_amarelo !=0:
                som_pulando.play()                
                gravidade_amarelo = -20

            if event.key == pygame.K_w and rect_roxo.bottom == 567 and vida_roxo != 0:
                
                som_pulando.play()
                gravidade_roxo = -20

            if event.key == pygame.K_RSHIFT and len(balas_amarelas) < 2  and vida_amarelo != 0:
                som_atirando.play()
                bala = pygame.Rect(rect_amarelo.x, rect_amarelo.y + 32, 15, 8)
                balas_amarelas.append(bala)

            if event.key == pygame.K_LSHIFT and len(balas_roxas) < 2 and vida_roxo != 0:
                som_atirando.play()
                bala = pygame.Rect(rect_roxo.x + 32, rect_roxo.y + 32, 15, 8)
                balas_roxas.append(bala)

    # Parte Visual
    desenhar(balas_amarelas, balas_roxas, tiro_amarelo, tiro_roxo, vida_amarelo, vida_roxo)

# Current Game
    if vida_amarelo != 0 and vida_roxo != 0:

        # Players (Gravidade e Movimentos)
        gravidade_amarelo += 1
        gravidade_roxo += 1
        rect_amarelo.y += gravidade_amarelo
        rect_roxo.y += gravidade_roxo

        # Players
        player(rect_amarelo, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN)
        player(rect_roxo, pygame.K_a, pygame.K_d, pygame.K_s)

        # Atirando
        vida_roxo = atirar(balas_amarelas, VelAmarelas, rect_roxo, vida_roxo)
        vida_amarelo = atirar(balas_roxas, VelRoxas, rect_amarelo, vida_amarelo)

        # Barreira (pato)
        if rect_amarelo.left <= 400:
            rect_amarelo.left = 400
        elif rect_amarelo.right >= 800:
            rect_amarelo.right = 800
        # Barreira (pata)
        if rect_roxo.right >= 400:
            rect_roxo.right = 400
        elif rect_roxo.left <= 0:
            rect_roxo.left = 0


    # GameOver
    else:
        if vida_amarelo == 0:
            game_over = comicsans.render("Roxo   venceu", 1, corRoxa)
            janela.blit(game_over, (260, 0))
        elif vida_roxo == 0:
            game_over = comicsans.render("Amarelo Venceu", 1, corAmarela)
            janela.blit(game_over, (200, 0))
        
        #Restaurando jogo
        
        balas_amarelas.clear()
        balas_roxas.clear()

        restart = comicsansMenor.render("Reiniciar? (R)", 1, corBranca)

        janela.blit(restart, (320, 300))
        if pygame.key.get_pressed()[pygame.K_r]:

            rect_amarelo = pygame.Rect(700, 631, 40, 64)
            rect_roxo = pygame.Rect(40, 631, 40, 64)
            vida_amarelo = 3
            vida_roxo = 3

