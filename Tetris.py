import pygame
import random


colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class tetromino:
    x = 0
    y = 0

    # Liste des tetrominos et leurs différentes rotations représentées dans une grille 4X4 
    # (pièces en forme de I, Z, S, L, L inversé, T et O)
    tetrominos = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]



    def __init__(self, x, y):
        self.x = x #position de la pièce sur la largeur du jeu 
        self.y = y #position de la pièce sur la longueur du jeu
        self.type = random.randint(0, len(self.tetrominos)-1) #type de la pièce entre 1 et 6
        self.color = random.randint(0, len(colors)-1) #couleur de la pièce
        self.rotation = 0 #rotation de la pièce

    
    def piece(self):
        return self.tetrominos[self.type][self.rotation]
    

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tetrominos[self.type])



class Tetris:
    def __init__(self, height, width): #initialisation du jeu 
        self.score = 0 #score du jeu 
        self.state = "start" #état du jeu (gameover si le jeu est fini)
        self.field = [] # grille de jeu
        self.height = height #hauteur du jeu
        self.width = width #largeur du jeu 
        self.x = 100
        self.y = 60
        self.piece = None
        self.zoom = 20 # Inutile pour nous: contrôle la taille des pièces par rapport à celle dans la grille dans pygame
        self.level = 2 # Pareil

        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

        
    def new_piece(self):
        self.piece = tetromino(3, 0)

        
    def intersects(self): 
        """Méthode s'assurant si un tétromino entre en contacts avec une pièce de l'état actuel du jeu."""
        
        intersection = False
        for i in range(4):  #Ici, on utilise la représentation 4x4 du nouveau tétromino
            for j in range(4):
                if i * 4 + j in self.piece.piece(): # On vérifie si la combinaison d'indices (i,j) correspond bien à une case occupée par la nouvelle pièce
                    if i + self.piece.y > self.height - 1 or \
                                j + self.piece.x > self.width - 1 or \
                                j + self.piece.x < 0 or \
                                self.field[i + self.piece.y][j + self.piece.x] > 0: # Ici, on vérifie si la nouvelle pièce entre en contact avec les bords de la partie ou une autre pièce
                            intersection = True
        return intersection
        

    def break_lines(self):
        """ Méthode parcourant l'ensemble de la grille et détruisant les lignes complètes si elles existent."""
        
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0: # Cela revient à vérifier si une ligne est complète
                lines += 1
                for k in range(i, 1, -1): # Ici on ramène les pièces au dessus de la ligne détruite en bas
                    for j in range(self.width):
                        self.field[k][j] = self.field[k - 1][j]
        self.score += lines

    def freeze(self):
        """Méthode permettant de fixer l'état du jeu, après que la nouvelle pièce entre en contact avec le reste du jeu, 
        et de faire descendre une nouvelle pièce."""
        
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.piece.piece():
                    self.field[i + self.piece.y][j + self.piece.x] = self.piece.color
        self.break_lines()
        self.new_piece()
        if self.intersects(): # Cette condition vérifie si la nouvelle pièce créée entre en contact directement avec une autre. Dans ce cas, la partie est perdue.
            self.state = "gameover"
    
    
    def go_space(self):
        """Méthode descendant la pièce jusqu'en bas"""

        while not self.intersects():
            self.piece.y += 1
        self.piece.y -= 1
        self.freeze()

    
    def go_down(self): # Ne sert que pour la simulation sur pygame (inutile pour nous)
        self.piece.y += 1
        if self.intersects():
            self.piece.y -= 1
            self.freeze()
    
    def go_side(self, dx):
        """Méthode déplaçant la pièce à droite (dx>0) ou à gauce (dx<0)"""
        
        old_x = self.piece.x
        self.piece.x += dx
        if self.intersects():
            self.piece.x = old_x

    def rotate(self):
        """Méthode effectuant la rotation sur une nouvelle pièce"""
        
        old_rotation = self.piece.rotation
        self.piece.rotate()
        if self.intersects():
            self.piece.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.piece is None:
        game.new_piece()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.piece is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.piece.piece():
                    pygame.draw.rect(screen, colors[game.piece.color],
                                     [game.x + game.zoom * (j + game.piece.x) + 1,
                                      game.y + game.zoom * (i + game.piece.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()