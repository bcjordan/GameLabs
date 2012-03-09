import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_2_START_X = SCREEN_WIDTH - PADDLE_START_X
PADDLE_2_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16
PING_SOUND = "ping.wav"

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
ping_sound = pygame.mixer.Sound(PING_SOUND)

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2_rect = pygame.Rect((PADDLE_2_START_X, PADDLE_2_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
score_2 = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT
			if paddle2_rect.top < 0:
				paddle2_rect.top = 0
			elif paddle2_rect.bottom >= SCREEN_HEIGHT:
				paddle2_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_w] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	if pygame.key.get_pressed()[pygame.K_UP] and paddle2_rect.top > 0:
		paddle2_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle2_rect.bottom < SCREEN_HEIGHT:
		paddle2_rect.top += BALL_SPEED
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()

	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	"""Ball collision with rails"""

	# Ball hits top/bottom
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]

	# Ball hit right wall
	if ball_rect.right >= SCREEN_WIDTH:
		score += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
		ball_speed[0] = BALL_SPEED
		pygame.time.wait(500)

	# Ball hit left wall
	if ball_rect.left <= 0:
		score_2 += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
		ball_speed[0] = -BALL_SPEED
		pygame.time.wait(500)

	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		ping_sound.play()

	if paddle2_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		ping_sound.play()

	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Left paddle
	pygame.draw.rect(screen, (0, 0, 0), paddle2_rect) # Right paddle
	
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball

	pygame.draw.line(screen, (255,0,0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), (SCREEN_WIDTH / 2, 0))

	# Check for winner
	winner = None
	if score_2 >= 11:
		winner = 2
		location = (SCREEN_WIDTH * 3 / 4)
	elif score >= 11:
		winner = 1
		location = (SCREEN_WIDTH / 4)

	if(winner):
		score_text = font.render("Player {0} wins!".format(winner), True, (0, 0, 0))

		screen.blit(score_text, (location - font.size(str(score))[0] / 2,
								 (SCREEN_HEIGHT / 2))) # The score

	score_text = font.render(str(score), True, (0, 0, 0))
	screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score

	score_text = font.render(str(score_2), True, (0, 0, 0))
	screen.blit(score_text, ((SCREEN_WIDTH * 3 / 4) - font.size(str(score))[0] / 2, 5)) # The score

	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)

	if(winner):
		pygame.time.wait(500)
		score = 0
		score_2 = 0
		winner = None
