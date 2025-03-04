import pygame
 
# Globals
HEIGHT = 720                                            # Screen height
WIDTH = 1280                                            # Screen width
screen = pygame.display.set_mode((WIDTH, HEIGHT))       # Screen
pygame.display.set_caption("Gobble")                    # Window title
clock = pygame.time.Clock()                             # Clock

SMALL_RADIUS = 15                                       # Small piece Radius
MED_RADIUS = 30                                         # Medium piece Radius
BIG_RADIUS = 45                                         # Big piece Radius

# Color Scheme Used in the Game
L_BLU = (134, 214, 254)
D_BLU = (66,120,255)
VD_BLU = (31,38,107)
BG_COL = (52, 68, 140)
WHITE = (255, 255, 255)
GREY = (42, 43, 66)

class Board(pygame.sprite.Sprite):
    """
    A Class to represent the 3X3 Game Board Where the Gobble pieces will be placed.
    
    Attributes:
        image: Surface object representing the board
        rect: Rect object representing the dimensions of the board
        Grid: 2D list representing the 3X3 grid of the board
        board: Surface object representing the board with grid squares
    """
    def __init__(self):
        """Constructor for the Board class."""
        super().__init__()
        self.image = pygame.Surface((400, 400)).convert()
        self.image.fill(GREY)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.Grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.GridSquaresInit()
        
    def GridSquaresInit(self):
        """
        A classmethod Used to initialize the 3X3 grid squares on the board.
        
        Parameters:
            None
            
        Returns:
            None
        """
        for i in range(3):
            for j in range(3):
                self.Grid[i][j] = pygame.Rect((50+i*100, 50+j*100), (100, 100))
                pygame.draw.rect(self.image, D_BLU, self.Grid[i][j], 2, border_radius=2)

class Piece(pygame.sprite.Sprite):
    """
    A Class to represent the Gobble pieces.
    
    Attributes:
        image: Surface object representing the piece
        rect: Rect object representing the dimensions of the piece
        color: Tuple representing the color of the piece
        status: Integer representing the status of the piece (0 - Unpicked, 1 - Picked)
    """
    def __init__(self, side, x, y, size):
        """
        Constructor for the Piece class.
        
        Parameters:
            side: String representing the side of the player
            x: Integer representing the x-coordinate of the piece
            y: Integer representing the y-coordinate of the piece
            size: Integer representing the size of the piece
        """
        super().__init__()
        self.side = side
        self.color = ()
        self.__set_color()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color
        self.rect = self.image.get_rect(center=(x, y))
        pygame.draw.circle(self.image, self.color, (50, 50), size)  # Draw circle at the center of the surface
        self.status = 0
    
    def __set_color(self):
        """
        A classmethod to set the color of the piece.
        
        Parameters:
            side: String representing the side of the player
            color: Tuple representing the color of the piece
            
        Returns:
            None
        """
        if self.side == "left":
            self.color = L_BLU
        elif self.side == "right":
            self.color = VD_BLU

    def piece_picked(self):
        """
        Changes piece status to picked.

        Parameters:
            None.
        """
        self.status = 1

    def piece_unpicked(self):
        """
        Changes piece status to unpicked.
        
        Parameters:
            None.
        """
        self.status = 0

class Player(pygame.sprite.Sprite):
    """
    A Class to represent the Player.
    Contains Pieces that the player can pick and place on the board.
    
    Attributes:
        image: Surface object representing the player
        rect: Rect object representing the dimensions of the player
        color: Tuple representing the color of the player
        x_pos: Integer representing the x-coordinate of the player
        pieces: 2D list representing the pieces of the player
    """
    def __init__(self, side):
        """
        Constructor for Player class.
        
        Parameters:
            side: String representing the side of the player
        """
        super().__init__()
        self.color = ()
        self.x_pos = 0
        self.__set_x_and_color(side)
        self.pieces = [[0,0],[0,0],[0,0]]
        self.image = pygame.Surface((200, 300)).convert()
        self.image.fill(BG_COL)
        self.rect = self.image.get_rect(center=(self.x_pos, HEIGHT//2))
        self.__init_pieces(side)
    
    def __set_x_and_color(self, side):
        """
        Private method to set the x-coordinate and color of the player.
        
        Parameters:
            side: String representing the side of the player
        """
        if side == "left":
            self.color = L_BLU
            self.x_pos = WIDTH//8
        elif side == "right":
            self.color = VD_BLU
            self.x_pos = WIDTH - WIDTH//8
            
    def __init_pieces(self, side):
        """
        Private method to initialize the pieces of the player
        
        Parameters:
            None
        """
        for i in range(3):
            for j in range(2):
                self.pieces[i][j] = Piece(side, self.rect.x + 50 + j*100, self.rect.y + 50 + i*100, (i+1)*15)


def main():
    
    # Initialize Sprites Group
    all_sprites_list = pygame.sprite.Group()
    
    # Background Surface
    bg_surface = pygame.Surface((WIDTH,HEIGHT)).convert()
    bg_surface.fill(D_BLU)
    
    # Define Sprites
    board = Board()
    P1 = Player(side="left")
    P2 = Player(side="right")
    
    # Add Sprites to Group
    all_sprites_list.add(P1)
    all_sprites_list.add(P2)
    for piece in P1.pieces, P2.pieces:
        all_sprites_list.add(piece)
    all_sprites_list.add(board)
    
    offset_x, offset_y = 0, 0
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
                 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            if event.type == pygame.MOUSEMOTION:
                for i in range(2):
                    for j in range(3):
                        if P1.pieces[j][i].status == 1:
                            mouse_x, mouse_y = event.pos
                            P1.pieces[j][i].rect.x = mouse_x + offset_x
                            P1.pieces[j][i].rect.y = mouse_y + offset_y
                        if P2.pieces[j][i].status == 1:
                            mouse_x, mouse_y = event.pos
                            P2.pieces[j][i].rect.x = mouse_x + offset_x
                            P2.pieces[j][i].rect.y = mouse_y + offset_y
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                for i in range(2):
                    for j in range(3):
                        if P1.pieces[j][i].rect.collidepoint(event.pos):
                            print("Player 1 piece", j, i)
                            P1.pieces[j][i].piece_picked()
                            print(P1.pieces[j][i].status)
                            offset_x = P1.pieces[j][i].rect.x - event.pos[0]
                            offset_y = P1.pieces[j][i].rect.y - event.pos[1]
                        if P2.pieces[j][i].rect.collidepoint(event.pos):
                            print("Player 2 piece", j, i)
                            P2.pieces[j][i].piece_picked()
                            print(P2.pieces[j][i].status)
                            offset_x = P2.pieces[j][i].rect.x - event.pos[0]
                            offset_y = P2.pieces[j][i].rect.y - event.pos[1]
                
            if event.type == pygame.MOUSEBUTTONUP:
                for i in range(2):
                    for j in range(3):
                        if P1.pieces[j][i].status == 1:
                            P1.pieces[j][i].piece_unpicked()
                            print(P1.pieces[j][i].status)
                        if P2.pieces[j][i].status == 1:
                            P2.pieces[j][i].piece_unpicked()
                            print(P2.pieces[j][i].status)
                            
        all_sprites_list.update()
        all_sprites_list.draw(bg_surface)
        screen.blit(bg_surface, (0,0))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()