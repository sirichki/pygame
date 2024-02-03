import pygame
import random
import math
import time
import os


# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Little Simu Test")


# Set up colors
BGCOLOR = (140, 184, 119) #(151, 193, 169)
HPBAREDGE = (225, 225, 225)
HPBARBG = (200, 200, 200)

RED = (255, 90, 80)
GREEN = (90, 255, 80)
BLUE = (75, 150, 225)
EDGE = 50

characters = []
class Character:
    def __init__(self, team, x, y):
        self.sprite = 42
        self.team = team
        self.atk = random.randint(10, 20)
        self.max_hp = random.randint(50, 99)
        self.hp = self.max_hp
        self.movespeed = random.uniform(1.0, 2.0)
        self.attack_speed = 1.0  # attacks per second
        self.attack_cooldown = 0
        self.width = 24  # Character width
        self.height = 30  # Character height
        self.x = x
        self.y = y
        self.dead = False
        self.act = 0
        self.direction = random.choice(['right','left'])  # Initial direction
        self.target = []

    def update_attack_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1 / 30  # Update based on frames per second

    def draw_health_bar(self):
        health_percentage = self.hp / self.max_hp
        bar_width = self.sprite - 4
        bar_height = 4
        pygame.draw.rect(window, HPBAREDGE, (self.x - bar_width // 2 - 2, self.y + 23, bar_width + 4, bar_height + 4), 0, 3, 3, 3)
        pygame.draw.rect(window, HPBARBG, (self.x - bar_width // 2, self.y + 25, bar_width, bar_height), 0, 2, 2, 2)
        pygame.draw.rect(window, self.team, (self.x - bar_width // 2, self.y + 25, bar_width * health_percentage, bar_height), 0, 2, 2, 2)

        # Show current HP in the health bar
        font = pygame.font.Font(None, 12)
        hp_text = font.render(str(int(self.hp)) + " / " + str(int(self.max_hp)), True, (0, 0, 0))
        window.blit(hp_text, (self.x-12, self.y + 23))


    def draw_character(self, frame):
        character_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images','Soldier1.png')).convert_alpha()
        frame_width = character_image.get_width() // 4
        frame_height = character_image.get_height() // 4
        frame_x = (frame % 4) * frame_width
        frame_y = self.act * frame_height
        if self.direction == 'left':
            image_copy = pygame.transform.flip(character_image, True, False)
            window.blit(image_copy, (self.x - frame_width // 2, self.y - frame_height // 2),
                    (character_image.get_width()// 4 * 3 - frame_x, frame_y, frame_width, frame_height))
        else:
            window.blit(character_image, (self.x - frame_width // 2, self.y - frame_height // 2),
                    (frame_x, frame_y, frame_width, frame_height))
        
    def move_towards(self, target):
        if not self.dead and not target.dead:
            dx = target.x - self.x
            dy = target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > self.sprite:
                self.act = 1
                move_distance = min(self.movespeed, distance)
                new_x = self.x + (dx / distance) * move_distance
                new_y = self.y + (dy / distance) * move_distance
                self.x = new_x
                self.y = new_y

            # Update direction based on target direction
            if dx > 0:
                self.direction = 'right'
            elif dx < 0:
                self.direction = 'left'
    
    def attack(self, target):
        if not self.dead and not target.dead:
            distance = math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
            if distance < self.sprite and self.attack_cooldown <= 0:
                self.act = 2
                target.hp -= self.atk
                if target.hp < 0:
                    target.hp = 0
                    target.dead = True
                self.attack_cooldown = 1.0 / self.attack_speed
                return self.atk
        return 0

def spawn_characters():
    for _ in range(4):
        x = random.randint(EDGE, WIDTH - EDGE)
        y = random.randint(EDGE, HEIGHT - EDGE)
        characters.append(Character(RED, x, y))
        x = random.randint(EDGE, WIDTH - EDGE)
        y = random.randint(EDGE, HEIGHT - EDGE)
        characters.append(Character(GREEN, x, y))
        x = random.randint(EDGE, WIDTH - EDGE)
        y = random.randint(EDGE, HEIGHT - EDGE)
        characters.append(Character(BLUE, x, y))

def display_winner(winner_team):
    postextx = 130
    postexty = 105
    fontsize = 50
    if winner_team == RED:
        winnerband = 'Red'
    elif winner_team == GREEN:
        winnerband = 'Green'
    elif winner_team == BLUE:
        winnerband = 'Blue'
    font = pygame.font.Font(None, fontsize)
    winner_text = font.render(f"" + winnerband + " Team Wins!", True, (44, 44, 44))
    window.blit(winner_text, (WIDTH // 2 - postextx + 2, HEIGHT // 2 - postexty + 2))
    font = pygame.font.Font(None, fontsize)
    winner_text = font.render(f"" + winnerband + " Team Wins!", True, winner_team)
    window.blit(winner_text, (WIDTH // 2 - postextx, HEIGHT // 2 - postexty))

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
spawn_characters()

damage_texts = []
frame_counter = 0
frame_percnt = 300
clock_cnt = 0
clock_tick_cnt = 30
win_cnt = 0
win_wait = 5

while True:
    window.fill(BGCOLOR)

    alive_characters = [character for character in characters if not character.dead]
    alive_teams = {character.team for character in alive_characters}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Check for alive characters and teams
    alive_characters = [character for character in characters if not character.dead]
    alive_teams = {character.team for character in alive_characters}

    for character in alive_characters:
        character.draw_health_bar()

    for character in alive_characters:
        character.update_attack_cooldown()
        #character.draw_death_animation()
        character.draw_character(frame_counter)

    # Draw damage pop-ups
    for damage_text in damage_texts:
        window.blit(damage_text['text'], (damage_text['pos_x'],damage_text['pos_y'] + damage_text['duration']))
        damage_text['duration'] -= 1
        if damage_text['duration'] <= 0:
            damage_texts.remove(damage_text)

    for character in characters:
        if character.hp <= 0:
            character.dead = True
            character.act = 3
    # Increment frame counter for animation
    if clock_cnt > (frame_percnt*4-clock_tick_cnt):
        clock_cnt = 0
    else:
        clock_cnt = clock_cnt + clock_tick_cnt
    frame_counter = (clock_cnt // frame_percnt)


    if len(alive_teams) == 1:
        if win_cnt == 0:
            for character in alive_characters:
                character.act = 0     
        win_cnt += 30
        display_winner(alive_teams.pop())
        if(win_cnt > win_wait * 1000):
            pygame.quit()
            exit()
    else:
        # Random target for character
        for character in alive_characters:
            if character.target and character.target[0].dead == True:
                character.target.remove(character.target[0])
            if not character.target:
                target_team = random.choice([team for team in alive_teams if team != character.team])
                target = min((c for c in alive_characters if c.team == target_team), key=lambda c: math.sqrt((character.x - c.x)**2 + (character.y - c.y)**2))
                character.target.append(target)
            target = character.target[0]
            character.move_towards(target)
            damage_dealt = character.attack(target)
            if damage_dealt > 0:
                font = pygame.font.Font(None, 16)
                damage_text = font.render(f"-{damage_dealt}", True, character.team)
                damage_texts.append({'text': damage_text, 'pos_x': target.x, 'pos_y': target.y - 30, 'duration': 2 * 30})  # 2 seconds

    pygame.display.flip()
    # Set the frames per second
    clock.tick(30)
