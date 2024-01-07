import random
import sys
import pygame
from pygame.locals import *

pygame.init()
#card memory game with pygame that uses a NxN grid of cards with N pairs of cards
#the cards are shuffled and placed face down on the grid and the player flips two cards at a time
#if the cards match they stay flipped over, if not they are flipped back over
#the game is won when all cards are flipped over. A timer keeps track of how long it takes to win the game
#the game can be restarted by pressing the space bar
#N can be changed through the start menu

#clock
clock = pygame.time.Clock()

#frames per second
FPS = 60

#screen size variables
screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

#images
purple_bg = pygame.image.load('Images/purple_background.png')

#card images
circle = pygame.image.load('Images/circle.png')
cross = pygame.image.load('Images/cross.png')
diamond = pygame.image.load('Images/diamond.png')
heart = pygame.image.load('Images/heart.png')
hexagon = pygame.image.load('Images/hexagon.png')
pentagon = pygame.image.load('Images/pentagon.png')
square = pygame.image.load('Images/square.png')
star = pygame.image.load('Images/star.png')
triangle = pygame.image.load('Images/triangle.png')
backOfCards = pygame.image.load('Images/backOfCards.png')
#fonts
pixelFont = pygame.font.Font('Fonts/pixel_font.ttf', 35)

#StartMenu class
#this class is used to create the start menu
class StartMenu(pygame.sprite.Sprite):
    def __init__(self, screen, font):
        #call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        #set the screen
        self.screen = screen
        #set the font
        self.font = font
        #create the start menu
        self.create_start_menu()

    def create_start_menu(self):
        #display the title
        title = self.font.render('Card Memory Game', True, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.center = (screen_width/2, screen_height/2 - 350)
        self.screen.blit(title, title_rect)

    def delete_start_menu(self):
        #delete the start menu by drawing the background over it
        self.screen.blit(purple_bg, (0, 0))

#Card class
class Card(pygame.sprite.Sprite):
    def __init__(self, screen, card_image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.card_image = card_image
        self.x = x
        self.y = y
        self.is_flipped = False
        self.create_card()

    def create_card(self):
        self.rect = self.card_image.get_rect(topleft=(self.x, self.y))  # Create a rect attribute
        self.screen.blit(backOfCards, (self.x, self.y))  # Display the backOfCards initially

    def flip(self):
        self.is_flipped = not self.is_flipped

    def draw(self):
        if not self.is_flipped:
            self.screen.blit(backOfCards, (self.x, self.y))
        else:
            self.screen.blit(self.card_image, (self.x, self.y))


class HUD(pygame.sprite.Sprite):
    def __init__(self, screen, font, background_image):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.font = font
        self.start_time = 0
        self.background_image = background_image
        self.create_hud()

    def create_hud(self):
        # Display the timer
        self.timer_label = self.font.render('Timer: ', True, (255, 255, 255))
        self.timer_rect = self.timer_label.get_rect()
        self.timer_rect.center = (screen_width/2, screen_height/2 - 350)
        self.screen.blit(self.timer_label, self.timer_rect)

    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    def update(self):
        # Update the timer
        current_time = pygame.time.get_ticks()
        elapsed_time_in_seconds = (current_time - self.start_time) // 1000  # Convert milliseconds to seconds

        # Redraw the top 200 pixels of the background
        top_region_rect = pygame.Rect(0, 0, screen_width, 200)
        self.screen.blit(self.background_image, (0, 0), area=top_region_rect)

        timer_text = f'Timer: {elapsed_time_in_seconds}'
        timer_rendered = self.font.render(timer_text, True, (255, 255, 255))
        self.screen.blit(timer_rendered, self.timer_rect)

# Game constants
CARD_SIZE = 100
GAP_SIZE = 20
CARD_ROWS = 4  # You can adjust the grid size as needed
CARD_COLS = 4
NUM_CARD_PAIRS = 8  # Adjust this based on the number of unique cards you have

class MemoryGame:
    def __init__(self, screen, font, background_image):
        self.screen = screen
        self.font = font
        self.background_image = background_image
        self.cards = []
        self.flipped_cards = []
        self.matches_found = 0
        self.is_flipping = False
        self.start_time = 0  # Fix: Initialize start_time attribute
        self.create_cards()
        self.create_hud()
        self.is_flipping = False  # Add this line
        self.is_game_over = False  # Add this line
        self.high_score = float('inf')

    def create_cards(self):
        # Generate random pairs of cards
        all_card_images = [circle, cross, diamond, heart, hexagon, pentagon, square, star, triangle]
        card_images = random.sample(all_card_images, NUM_CARD_PAIRS) * 2
        random.shuffle(card_images)

        for row in range(CARD_ROWS):
            for col in range(CARD_COLS):
                x = col * (CARD_SIZE + GAP_SIZE) + 200
                y = row * (CARD_SIZE + GAP_SIZE) + 200
                card_image = card_images.pop()  # Use the unique card images for each card
                card = Card(self.screen, card_image, x, y)
                self.cards.append(card)

    def create_hud(self):
        self.timer_label = self.font.render('Timer: ', True, (255, 255, 255))
        self.timer_rect = self.timer_label.get_rect()
        self.timer_rect.center = (screen_width / 2, 50)

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time_in_seconds = (current_time - self.start_time) // 1000
        top_region_rect = pygame.Rect(0, 0, screen_width, 100)

        self.screen.blit(self.background_image, (0, 0), area=top_region_rect)

        timer_text = f'Timer: {elapsed_time_in_seconds}'
        timer_rendered = self.font.render(timer_text, True, (255, 255, 255))
        self.screen.blit(timer_rendered, self.timer_rect)

        # Move check_card_click before draw_cards
        current_time = pygame.time.get_ticks()

        if not self.is_flipping:
            self.check_card_click(callback=self.draw_cards)


    def draw_cards(self):
        for card in self.cards:
            card.draw()

    def flip_back_over(self):
        pygame.time.delay(1000)  # Adjust the delay duration (in milliseconds) as needed
        for card in self.flipped_cards:
            card.flip()

    def check_card_click(self, callback=None):

        pygame.time.delay(100)  # Wait for 500 milliseconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                flipped_not_matched = [card for card in self.cards if
                                       card.is_flipped and card not in self.flipped_cards]

                #if len(flipped_not_matched) < 2:
                for card in self.cards:
                    if card.rect.collidepoint(mouse_x, mouse_y) and not card.is_flipped:
                        card.flip()
                        self.flipped_cards.append(card)

                        if len(self.flipped_cards) == 2:
                            self.is_flipping = True
                            self.check_match()
                            self.is_flipping = False
                            self.flipped_cards.clear()


        if callback is not None:
            callback()

    def check_match(self):
        card1, card2 = self.flipped_cards
        if card1.card_image == card2.card_image:
            self.matches_found += 1
            if self.matches_found == NUM_CARD_PAIRS:
                #display second card before displaying "You Win!"
                card2.draw()
                self.display_game_over()
        else:
            # Cards do not match, so display them briefly before flipping back
            card1.draw()
            card2.draw()
            pygame.display.flip()
            pygame.time.delay(1000)  # Wait for an additional 0.5 seconds
            card1.flip()
            card2.flip()

    def display_game_over(self):
        # Get the current time and elapsed time
        current_time = pygame.time.get_ticks()
        elapsed_time_in_seconds = (current_time - self.start_time) // 1000

        new_high_score = False
        # Check if it's a new high score
        if elapsed_time_in_seconds < self.high_score:
            self.high_score = elapsed_time_in_seconds
            new_high_score = True

        # Clear the screen
        self.screen.blit(self.background_image, (0, 0))

        # Display "You Win!" text
        game_over_text = self.font.render('You Win!', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2-55))
        self.screen.blit(game_over_text, game_over_rect)

        # Display the amount of time it took to win the game
        time_text = f'Time: {elapsed_time_in_seconds} seconds'
        time_rendered = self.font.render(time_text, True, (255, 255, 255))
        time_rect = time_rendered.get_rect(center=(screen_width // 2, screen_height // 2-5))
        self.screen.blit(time_rendered, time_rect)

        # Display the high score
        high_score_text = f'High Score: {self.high_score} seconds'
        high_score_rendered = self.font.render(high_score_text, True, (255, 255, 255))
        high_score_rect = high_score_rendered.get_rect(center=(screen_width // 2, screen_height // 2 + 45))
        self.screen.blit(high_score_rendered, high_score_rect)

        # Display "New High Score!" text if applicable
        if new_high_score:
            new_high_score_text = self.font.render('New High Score!', True, (255, 255, 255))
            new_high_score_rect = new_high_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 95))
            self.screen.blit(new_high_score_text, new_high_score_rect)

        # Update the display
        pygame.display.update()

        # Wait for the user to click the mouse to restart the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    waiting = False
                    self.restart_game()

    def restart_game(self):
        #clear the screen and restart the game
        self.screen.blit(self.background_image, (0, 0))


        self.cards.clear()
        self.flipped_cards.clear()
        self.matches_found = 0
        self.create_cards()
        self.start_time = pygame.time.get_ticks()


# ... (existing code)

# main game loop
run = True
isGameStart = False
userEnteredPairsOfCards = False
header = None
game = None

while run:
    clock.tick(FPS)

    if not isGameStart:
        start_menu = StartMenu(screen, pixelFont)

    if not isGameStart:
        start_menu.create_start_menu()
        isGameStart = True

    elif isGameStart and not userEnteredPairsOfCards:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            pairsOfCards = 8
            userEnteredPairsOfCards = True  # Set this to True to skip the user input block

    elif isGameStart and userEnteredPairsOfCards and header is None:
        start_menu.delete_start_menu()
        header = HUD(screen, pixelFont, purple_bg)
        header.start_timer()
        game = MemoryGame(screen, pixelFont, purple_bg)

    elif game is not None and not game.is_game_over:  # Check if the game is not over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.update()

    pygame.display.update()

pygame.quit()