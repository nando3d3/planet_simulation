from pickle import FALSE
from turtle import update
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Definição das cores em RGB
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
ORANGE = (241, 108, 0)
GREY = (80, 80, 80)
LIGHT_YELLOW = (245, 255, 204)

FONT = pygame.font.SysFont("comicsans", 16)

# Criando os planetas


class Planet:
    # Unidade Astronômica
    AU = 1.496e11  # metros
    # Constante gravitacional
    G = 6.674184e-11  # m3/kg*s2
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 8.64e4  # segundos em 1 dia

    def __init__(self, x, y, radius, color, mass):
        # Características dos planteras
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        # Velocidade dos planetas nas direções x e y
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        """ if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2)) """
        
        

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x, distance_y = other_x - self.x, other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        #Força gravitacional
        force = self.G * self.mass * other.mass / distance ** 2
        
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y

    #Atualizar a posição dos planetas considerando a atração 
    # de todos os outros corpos
    def update_postion (self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction (planet)
            total_fx += fx
            total_fy += fy

        # v = F*t/m
        #Att a velocidade
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        #Att a posição
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 3.3e23)
    mercury.y_vel = -47400 #m/s

    venus = Planet(0.723 * Planet.AU, 0, 14, LIGHT_YELLOW, 4.8685e24)
    venus.y_vel = -35020 #m/s

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742e24)
    earth.y_vel = 29783 #m/s

    mars = Planet(-1.524 * Planet.AU, 0, 12, ORANGE, 6.39e23)
    mars.y_vel = 24077 #m/s

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        WIN.fill((0, 0 ,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_postion(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
