import pygame
import random
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run and Shoot")

# Colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLACK = (0, 0, 0)
BULLET_COLOR = (0, 200, 255)
PLAYER_COLOR = (50, 255, 50)

# Game constants
PLAYER_RADIUS = 20
ENEMY_RADIUS = 20
BULLET_RADIUS = 5
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 4
ENEMY_SHOOT_INTERVAL = 120  # frames

clock = pygame.time.Clock()
FPS = 100

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.radius = PLAYER_RADIUS
        self.alive = True

    def move(self, keys):
        # Use WASD instead of arrow keys
        if keys[pygame.K_a] and self.x - self.radius > 0:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.x + self.radius < WIDTH:
            self.x += PLAYER_SPEED
        if keys[pygame.K_w] and self.y - self.radius > 0:
            self.y -= PLAYER_SPEED
        if keys[pygame.K_s] and self.y + self.radius < HEIGHT:
            self.y += PLAYER_SPEED

    def draw(self, win):
        pygame.draw.circle(win, PLAYER_COLOR, (self.x, self.y), self.radius)



# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = ENEMY_RADIUS
        self.shoot_timer = random.randint(0, ENEMY_SHOOT_INTERVAL)

    def draw(self, win):
        pygame.draw.circle(win, RED, (self.x, self.y), self.radius)

    def shoot(self, player_pos):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        vx = ENEMY_BULLET_SPEED * dx / dist
        vy = ENEMY_BULLET_SPEED * dy / dist
        return Bullet(self.x, self.y, vx, vy, False)

# Bullet class


class Bullet:
    def __init__(self, x, y, vx, vy, from_player):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = BULLET_RADIUS
        self.from_player = from_player

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, win):
        # Draw blue for player, red for enemy
        color = (0, 200, 255) if self.from_player else (255, 0, 0)
        pygame.draw.circle(win, color, (int(self.x), int(self.y)), self.radius)

    def off_screen(self):
        return (self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT)



def collide(obj1, obj2):
    dist = math.hypot(obj1.x - obj2.x, obj1.y - obj2.y)
    return dist < (obj1.radius + obj2.radius)


def main():
    run = True
    player = Player()
    enemies = []
    bullets = []
    score = 0

    # Spawn three enemies at random positions at the top
    for _ in range(3):
        x = random.randint(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS)
        y = random.randint(ENEMY_RADIUS, HEIGHT // 3)
        enemies.append(Enemy(x, y))

    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)

        shoot_pressed = False  # Track if LMB is pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shoot_pressed = True



        keys = pygame.key.get_pressed()
        if player.alive:
            player.move(keys)
            # Shoot bullet towards mouse with LMB, allow spamming (no delay)
            if pygame.mouse.get_pressed()[0]:  # LMB held or clicked
                mx, my = pygame.mouse.get_pos()
                dx = mx - player.x
                dy = my - player.y
                dist = math.hypot(dx, dy)
                if dist != 0:
                    vx = BULLET_SPEED * dx / dist
                    vy = BULLET_SPEED * dy / dist
                    bullets.append(Bullet(player.x, player.y, vx, vy, True))


        # Enemy logic
        for enemy in enemies:
            enemy.shoot_timer -= 1
            if enemy.shoot_timer <= 0 and player.alive:
                bullets.append(enemy.shoot((player.x, player.y)))
                enemy.shoot_timer = ENEMY_SHOOT_INTERVAL

        # Move and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(WIN)
            if bullet.off_screen():
                bullets.remove(bullet)
                continue
            if bullet.from_player:
                for enemy in enemies[:]:
                    if collide(bullet, enemy):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 1
                        # Respawn enemy
                        x = random.randint(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS)
                        y = random.randint(ENEMY_RADIUS, HEIGHT // 3)
                        enemies.append(Enemy(x, y))
                        break
            else:
                if player.alive and collide(bullet, player):
                    player.alive = False
                    bullets.remove(bullet)

        # Draw everything
        player.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

        if not player.alive:
            over_text = font.render("GAME OVER! Press R to Restart", True, WHITE)
            WIN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
            if keys[pygame.K_r]:
                main()
                return

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
