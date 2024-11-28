import pygame
import random
import time

def tela_inicial(): #função para desenhar a tela inicial
    fonte_botao = pygame.font.SysFont('Comic Sans MS', 50)
    fonte_titulo = pygame.font.SysFont('Comic Sans MS', 65,True)

    tela.fill(preto)

    for i in range(30):
        for j in range(40):
            pygame.draw.rect(tela, (j*0.75,(40-j)*0.75,1.5*i), (20*j, 20*i, 20, 20))

    titulo = fonte_titulo.render("PONG", True, branco)
    titulo_rect = titulo.get_rect(center=(largura // 2, altura // 4 - 20))
    tela.blit(titulo, titulo_rect)

    iniciar_jogo = fonte_botao.render("Iniciar Jogo", True, verde)
    iniciar_jogo_rect = iniciar_jogo.get_rect(center=(largura // 2, altura // 2 - 50))
    tela.blit(iniciar_jogo, iniciar_jogo_rect)
    pygame.draw.rect(tela, branco, iniciar_jogo_rect.inflate(20, 20), 5, 15)

    sair = fonte_botao.render("Sair", True, vermelho)
    sair_rect = sair.get_rect(center=(largura // 2, altura // 2 + 50))
    tela.blit(sair, sair_rect)
    pygame.draw.rect(tela, branco, sair_rect.inflate(20, 20), 5, 15)


    #piscando os retângulos coloridos (Arco-íris) após desenhar o conteúdo
    for color in arco_iris:
        pygame.draw.rect(tela, color, (6, 6, largura-12, altura-12), 5)  #5 é a espessura
        pygame.display.update()
        time.sleep(0.1)
    pygame.display.update()

    return iniciar_jogo_rect, sair_rect #retornando os retângulos para verificar clique

def raquete_desenho(x, y, raquete_largura, raquete_altura): #função para desenhar a raquete
    pygame.draw.rect(tela, verdeagua, (x, y, raquete_largura, raquete_altura),2,5)

def bola_desenho(x, y, raio_bola): #função para desenhar a bola
    pygame.draw.circle(tela, branco, (x,y), raio_bola,2)

def pontuação_desenho(pontuação1, pontuação2):  #função para desenhar o placar
    fonte = pygame.font.SysFont('verdana', 30)
    texto_pontuação = fonte.render(f"{pontuação1} - {pontuação2}", True, branco)
    tela.blit(texto_pontuação, (largura // 1.20, 10))

def fundo_desenho(): #função para desenhar o fundo e as linhas
    for i in range(30):
        for j in range(40):
            pygame.draw.rect(tela, (j*0.75,(40-j)*0.75,1.5*i), (20*j, 20*i, 20, 20))
            pygame.draw.rect(tela, branco, (largura // 2 - 2.5, i * 20, 2.5, 20), ) #linha central

def loop_jogo(): #função para desenhar o fundo e as linhas
    #definições de parâmetros
    raquete_largura, raquete_altura = 15, 90
    raio_bola = 10
    raquete_velocidade = 10
    bola_velocidade_x = random.choice([-5,5])
    bola_velocidade_y = random.choice([-5,5])
    pontuação1 = 0
    pontuação2 = 0
    dificuldade = 1.0
    tempo_jogo = 0

    num_estrelas = 100  # Número de estrelas
    estrelas = []

    for _ in range(num_estrelas):
        x = random.randint(0, largura)
        y = random.randint(0, altura)
        tamanho = random.randint(1, 3)  # Tamanho das estrelas (1 a 3 pixels)
        velocidade12 = random.randint(1, 3)  # Velocidade da estrela
        cores_estrelas = random.choice(arco_iris) # cores das estrelas
        estrelas.append([x, y, tamanho, velocidade12, cores_estrelas])

    #posições iniciais
    player1_x, player1_y = 30, altura // 2 - raquete_altura // 2
    player2_x, player2_y = largura - 30 - raquete_largura, altura // 2 - raquete_altura // 2
    bola_x, bola_y = largura // 2, altura // 2

    #config da musica
    pygame.mixer.music.load('C:/Users/Laura Elisa/Documents/faculdade/theme.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.10)

    relógio = pygame.time.Clock()

    while True:
        fundo_desenho()
        
        for estrela in estrelas:
            x, y, tamanho, velocidade12, cores_estrelas = estrela
            y += velocidade12 # Move as estrelas para baixo

                # Quando uma estrela ultrapassa o limite inferior da tela, ela volta ao topo
            if y > altura:
                y = 0
                x = random.randint(0, largura)  # Nova posição X ao voltar

            estrela[1] = y  # Atualiza a posição Y

            # Desenhar a estrela
            pygame.draw.circle(tela, cores_estrelas, (x, y), tamanho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        teclas = pygame.key.get_pressed()  #controles das raquetes
        if teclas[pygame.K_w] and player1_y > 0:
            player1_y -= raquete_velocidade
        if teclas[pygame.K_s] and player1_y < altura - raquete_altura:
            player1_y += raquete_velocidade
        if teclas[pygame.K_UP] and player2_y > 0:
            player2_y -= raquete_velocidade
        if teclas[pygame.K_DOWN] and player2_y < altura - raquete_altura:
            player2_y += raquete_velocidade

        #movimento da bola
        bola_x += bola_velocidade_x
        bola_y += bola_velocidade_y

        #colisão com o topo e fundo da tela
        if bola_y - raio_bola <= 0 or bola_y + raio_bola >= altura:
            hit.play()
            bola_velocidade_y = -bola_velocidade_y

        #colisão com as raquetes
        if bola_x - raio_bola <= player1_x + raquete_largura and player1_y < bola_y < player1_y + raquete_altura:
            hit.play()
            bola_velocidade_x = -(bola_velocidade_x * (1 + dificuldade))
            bola_x = player1_x + raquete_largura + raio_bola + 1
            if raquete_altura > 15:
                raquete_altura -= 1

        if bola_x + raio_bola >= player2_x and player2_y < bola_y < player2_y + raquete_altura:
            hit.play()
            bola_velocidade_x = -(bola_velocidade_x * (1 + dificuldade))
            bola_x = player2_x - raio_bola - 1
            if raquete_altura > 15:
                raquete_altura -= 1

        #marca ponto se a bola passar de uma raquete
        if bola_x - raio_bola <= 0:
            point.play()
            pontuação2 += 1
            bola_x, bola_y = largura // 2, altura // 2
            bola_velocidade_x = 5
            bola_velocidade_y = random.choice([-5,5])
            dificuldade = 0  #resetando a dificuldade para o valor inicial
            tempo_jogo = 0  #reseta o tempo de jogo quando alguém marca
            raquete_altura = 90

        if bola_x + raio_bola >= largura:
            point.play()
            pontuação1 += 1
            bola_x, bola_y = largura // 2, altura // 2
            bola_velocidade_x = -5
            bola_velocidade_y = random.choice([-5,5])
            dificuldade = 0
            tempo_jogo = 0
            raquete_altura = 90

        #aumenta a dificuldade ao longo do tempo enquanto a bola não cair
        if tempo_jogo >= 0:
            tempo_jogo += 1  #incrementa o tempo de jogo
            dificuldade = tempo_jogo / 40000  #aumenta a dificuldade gradualmente

        #desenha os elementos na tela
        raquete_desenho(player1_x, player1_y, raquete_largura, raquete_altura)
        raquete_desenho(player2_x, player2_y, raquete_largura, raquete_altura)

        bola_desenho(bola_x, bola_y,raio_bola)
        pontuação_desenho(pontuação1, pontuação2)
        timer_desenho(tempo_jogo)

        pygame.display.flip()  #atualiza a tela
        relógio.tick(60)  #controla a taxa de quadros

def menu_inicial(): #loop principal do menu de seleção

    while True:
        iniciar_jogo_rect, sair_rect = tela_inicial()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if iniciar_jogo_rect.collidepoint(pos): #inicia Jogo se clicar no botão "Iniciar Jogo"
                    select.play()
                    loop_jogo()
                
                if sair_rect.collidepoint(pos): #sai do Jogo se clicar no botão "Sair"
                    select.play()
                    pygame.quit()
                    exit()

def timer_desenho(tempo_jogo):  #função para desenhar o timer na tela
    minutos = tempo_jogo // 60
    segundos = tempo_jogo % 60
    tempo_formatado = f"{int(minutos):02}:{int(segundos):02}"
    
    fonte = pygame.font.SysFont('verdana', 30)
    texto_tempo = fonte.render(tempo_formatado, True, branco)
    tela.blit(texto_tempo, (10, 10))  #desenha o tempo no canto superior esquerdo

pygame.init()

#cores
branco = (255, 255, 255)
preto = (0, 0, 0)
azul_claro = (0, 204, 255)
azul_escuro = (0, 51, 102)
vermelho = (139,0,0)
cinza = (100, 100, 100)
roxosla = (106, 90, 205)
azulferro = (70, 130, 180)
verdeagua = (32, 178, 170)
verde = (60,179,113)
arco_iris = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

#configuração da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong")

#configuração de audio
pygame.mixer.init()
point = pygame.mixer.Sound('C:/Users/Laura Elisa/Documents/faculdade/point.wav')
hit = pygame.mixer.Sound('C:/Users/Laura Elisa/Documents/faculdade/hit.wav')
select = pygame.mixer.Sound('C:/Users/Laura Elisa/Documents/faculdade/select.wav')

menu_inicial()