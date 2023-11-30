import pygame
import math

pygame.init()

# tamaño de la ventana
WHDTH, HEIGHT = 800, 600
ventana = pygame.display.set_mode((WHDTH, HEIGHT))

pygame.display.set_caption("GRAVITAS")

MASA_PLANETA = 100
MASA_NAVE = 5
GRAVEDAD = 1
FPS = 60
PLANETA_SIZE = 50 #radio
NAVE_SIZE = 5
VELOCIDAD = 100

BG = pygame.transform.scale(pygame.image.load("fondo.jpg"), (WHDTH, HEIGHT))
#PLANETA = pygame.transform.scale(pygame.image.load("planeta.png"), (PLANETA_SIZE * 2, PLANETA_SIZE * 2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

class Planeta:
    def __init__(self, x:int, y:int, masa):
        self.x = x
        self.y = y
        self.masa = masa

    def draw(self):
        #ventana.blit(PLANETA, (self.x - PLANETA_SIZE, self.y - PLANETA_SIZE))
        pygame.draw.circle(ventana, GREEN, (self.x, self.y), PLANETA_SIZE )

class Nave:
    def __init__(self, x:int, y:int, vel_x, vel_y, masa):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.masa = masa
    
    def draw(self):
        pygame.draw.circle(ventana, RED, (self.x, self.y), NAVE_SIZE)
    
    def move(self, planeta = None):
        distancia = math.sqrt((self.x - planeta.x)**2 + (self.y - planeta.y)**2)
        fuerza = (GRAVEDAD * (self.masa * planeta.masa) ) / distancia**2
        aceleracion = fuerza / self.masa
        angulo = math.atan2(planeta.y - self.y, planeta.x - self.x)
        
        aceleracion_x = math.cos(angulo) * aceleracion
        aceleracion_y = math.sin(angulo) * aceleracion
        
        self.vel_x += aceleracion_x
        self.vel_y += aceleracion_y
        
        self.x += self.vel_x
        self.y += self.vel_y
        

def create_nave(localizacion, mouse):
    temp_x, temp_y = localizacion
    mouse_x, mouse_y = mouse
    velocidad_x = (mouse_x - temp_x) / VELOCIDAD
    velocidad_y = (mouse_y - temp_y) / VELOCIDAD
    nave= Nave(temp_x, temp_y, velocidad_x, velocidad_y, MASA_NAVE)
    return nave

def main():
    run = True
    clock = pygame.time.Clock()

    planeta = Planeta(WHDTH // 2, HEIGHT // 2, MASA_PLANETA)
    
    naves : list[Nave] = []
    temp_nave_pos = None

    while run:
        clock.tick(FPS)
        ventana.blit(BG, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_nave_pos:
                    temp_x, temp_y = temp_nave_pos
                    nave = create_nave(temp_nave_pos, mouse_pos)
                    naves.append(nave)
                    temp_nave_pos = None
                else:    
                    temp_nave_pos = mouse_pos

        for nv in naves[:]:
            nv.draw()
            nv.move(planeta=planeta)
            fuera_pantalla = nv.x < 0 or nv.x > WHDTH or nv.y < 0 or nv.y > HEIGHT
            choque = math.sqrt((nv.x - planeta.x)**2 + (nv.y - planeta.y)**2) < PLANETA_SIZE + NAVE_SIZE
            if fuera_pantalla or choque:
                naves.remove(nv)
        
        if temp_nave_pos:
            pygame.draw.line(ventana, WHITE, temp_nave_pos, mouse_pos, 2)
            pygame.draw.circle(ventana, RED, temp_nave_pos, NAVE_SIZE)
        
        planeta.draw()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()