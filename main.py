import pygame
from sys import exit
from paddle import Paddle
from blocks import Blocks
from ball import Ball


def create_blocks(start_x_pos, start_y_pos, cols):
    block_colors = ['red', 'red', 'orange', 'orange', 'green', 'green', 'yellow', 'yellow']
    block_width = 80
    block_height = 20
    row_spacing = block_height + 10
    col_spacing = block_width + 10
    for color_index, color in enumerate(block_colors):
        for col_index, col in enumerate(range(cols)):
            x_pos = start_x_pos + col_index * col_spacing
            y_pos = start_y_pos + color_index * row_spacing
            blocks.add(Blocks(x_pos, y_pos, width=block_width, height=block_height, color=color))


def collision_checker():
    global score
    global ball_x_direction
    global ball_y_direction
    # ball collision with blocks
    blocks_hit = pygame.sprite.spritecollide(ball.sprite, blocks, True)
    if blocks_hit:
        for block in blocks_hit:
            score += block.value
        if ball.sprite.rect.bottom >= block.rect.top:
            # ball collided with top side of block
            ball_y_direction *= -1
        elif ball.sprite.rect.top <= block.rect.bottom:
            # ball collided with bottom side of block
            ball_y_direction *= -1
        elif ball.sprite.rect.right >= block.rect.left:
            # ball collided with left side of block
            ball_x_direction *= -1
        elif ball.sprite.rect.left <= block.rect.right:
            # ball collided with right side of block
            ball_x_direction *= - 1
        # if all blocks in the group have been destroyed, generate a fresh set of aliens
        if not blocks:
            create_blocks(start_x_pos=10, start_y_pos=60, cols=11)
            alien_direction = 1

    # ball collision with wall
    if ball.sprite.rect.left <= 0:
        # left side of ball collided with left wall
        ball_x_direction *= -1
    if ball.sprite.rect.right >= screen_width:
        # right side of ball collided with right wall
        ball_x_direction *= -1
    if ball.sprite.rect.top <= 0:
        # top of ball collided with top wall
        ball_y_direction *= -1

    # ball collision with player
    paddle_hit = pygame.sprite.spritecollide(ball.sprite, paddle, False)
    if paddle_hit:
        if ball.sprite.rect.bottom >= paddle.sprite.rect.top:
            # ball collided with top of paddle:
            ball_y_direction *= -1
        if ball.sprite.rect.left <= paddle.sprite.rect.right:
            # left side of ball collided with right side of paddle
            ball_x_direction *= -1
        if ball.sprite.rect.right >= paddle.sprite.rect.left:
            # right side of ball collided with left side of paddle
            ball_x_direction *= -1


def display_score():
    score_text = test_font.render(f'Score: {score}', True, (255, 255, 255))
    score_text_rect = score_text.get_rect(midleft=(10, 20))
    screen.blit(score_text, score_text_rect)


def display_lives():
    for life in range(lives):
        x = lives_x_start_pos + (life * (live_surf.get_size()[0] + 15))
        screen.blit(live_surf, (x, 18))
        screen.blit(life_text, life_text_rect)


def check_lives():
    global lives
    global game_active
    if ball.sprite.rect.bottom >= screen_height:
        # bottom of the ball has touched the bottom part of the screen, player loses a life
        lives -= 1
        # respawn ball
        ball.sprite.rect.x = paddle.sprite.rect.centerx  # find current position of paddle and spawn ball at mid-point
        ball.sprite.rect.y = screen_height - 50
        if lives <= 0:
            game_active = False

pygame.init()
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeled.ttf', 20)
score = 0


game_active = True

# player group
paddle = pygame.sprite.GroupSingle()
paddle.add(Paddle(x_pos=screen_width/2, y_pos=screen_height-10, width=200, height=15, screen_width=screen_width))

# block group
blocks = pygame.sprite.Group()
# draw blocks
create_blocks(start_x_pos=10, start_y_pos=60, cols=11)

# ball group
ball = pygame.sprite.GroupSingle()
ball.add(Ball(x_pos=screen_width/2, y_pos=screen_height-50, radius=10, color='white'))
ball_x_direction = -3
ball_y_direction = -3

#life setup
lives = 3
live_surf = ball.sprite.image
lives_x_start_pos = screen_width - live_surf.get_size()[0] * lives - 60
life_text = test_font.render('Lives:', True, (255, 255, 255))
life_text_rect = life_text.get_rect(midright=(lives_x_start_pos-10, 25))

# Game Over Screen
game_over_font = pygame.font.Font('font/Pixeled.ttf', 50)
game_over_text = game_over_font.render('GAME OVER', False, (255, 255, 255))
game_over_text_rect = game_over_text.get_rect(center=(screen_width/2, 200))

play_again_font = pygame.font.Font('font/Pixeled.ttf', 30)
play_again_text = play_again_font.render('PLAY AGAIN?', False, (255, 255, 255))
play_again_text_rect = play_again_text.get_rect(center=(screen_width/2, 400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        # Fill the screen with a black background
        screen.fill((0, 0, 0))

        # draw player object
        paddle.draw(screen)
        paddle.update()

        # draw blocks
        blocks.draw(screen)

        # draw ball
        ball.draw(screen)
        ball.update(x_direction=ball_x_direction, y_direction=ball_y_direction)

        # collision checker
        collision_checker()

        # display score
        display_score()

        # display lives
        display_lives()

        # check lives
        check_lives()

    else:
        screen.fill((0, 0, 0))
        # display game over text
        screen.blit(game_over_text, game_over_text_rect)
        # display player score
        player_score_text = test_font.render(f'Your Score: {score}', False, (255, 255, 255))
        player_score_text_rect = player_score_text.get_rect(center=(screen_width / 2, 300))
        screen.blit(player_score_text, player_score_text_rect)
        # ask if user would like to play again
        screen.blit(play_again_text, play_again_text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button is clicked
            mouse_pos = pygame.mouse.get_pos()
            if play_again_text_rect.collidepoint(mouse_pos):
                # "PLAY AGAIN" button is clicked
                game_active = True
                # reset score
                score = 0

                # remove remaining blocks
                blocks.empty()

                # draw new blocks
                create_blocks(start_x_pos=10, start_y_pos=60, cols=11)

                # reset paddle position
                paddle.empty()
                paddle.add(Paddle(x_pos=screen_width / 2, y_pos=screen_height - 10, width=200, height=15,
                                  screen_width=screen_width))

                # reset ball position
                ball.empty()
                ball.add(Ball(x_pos=screen_width / 2, y_pos=screen_height - 50, radius=10, color='white'))

                # reset lives to 3
                lives = 3

                # reset ball speed and direction
                ball_x_direction = -3
                ball_y_direction = -3

    pygame.display.update()
    clock.tick(60)

