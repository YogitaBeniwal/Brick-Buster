import pgzrun
import colorsys
from math import copysign
import random

WIDTH = 400
HEIGHT = 500
BALL_SIZE = 20
MARGIN = 50
BRICKS_X = 10
BRICKS_Y = 5
score = 0

BRICK_W = (WIDTH - 2 * MARGIN) // BRICKS_X
BRICK_H = 25

ball = ZRect(WIDTH / 2, HEIGHT / 2, BALL_SIZE, BALL_SIZE)
bat = ZRect(WIDTH / 2, HEIGHT - 50, 80 , 12)
bricks = []

def hsv_color(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return r * 255, g * 255, b * 255

def reset():
    global score
    score = 0
    del bricks[:]
    for x in range(BRICKS_X):
        for y in range(BRICKS_Y):
            brick = ZRect(
                (x * BRICK_W + MARGIN, y * BRICK_H + MARGIN),
                (BRICK_W - 1, BRICK_H - 1)
            )
            hue = (x + y) / BRICKS_X
            saturation = (y / BRICKS_Y) * 0.5 + 0.5
            brick.highlight = hsv_color(hue, saturation * 0.7, 1.0)
            brick.color = hsv_color(hue, saturation, 0.8)
            bricks.append(brick)

    ball.center = (WIDTH / 2, HEIGHT / 2)
    ball.vel = (random.uniform(-200, 200), 400)

reset()

def draw():
    global score
    screen.clear()
    screen.blit('background2', (0,0))
    screen.draw.text('Score : '+str(score),color='white',topleft=(10,10))

    for brick in bricks:
        screen.draw.filled_rect(brick, brick.color)
        screen.draw.line(brick.bottomleft, brick.topleft, brick.highlight)
        screen.draw.line(brick.topleft, brick.topright, brick.highlight)

    screen.draw.filled_rect(bat,'yellow')
    screen.draw.filled_circle(ball.center, BALL_SIZE // 2, 'blue')
    
def update():
  for i in range(3):
    if(len(bricks) > 40):
        update_step(1/360)
    elif(len(bricks) > 25):
        update_step(1/180)
    else:
        update_step(1/120)    

def update_step(dt):
    global score
    x, y = ball.center
    vx, vy = ball.vel

    if ball.top > HEIGHT:
        reset()
        return

    x += vx * dt
    y += vy * dt
    ball.center = (x, y)

    if ball.left < 0:
        vx = abs(vx)
        ball.left = -ball.left
    elif ball.right > WIDTH:
        vx = -abs(vx)
        ball.right -= 2 * (ball.right - WIDTH)

    if ball.top < 0:
        vy = abs(vy)
        ball.top *= -1

    if ball.colliderect(bat):
        vy = -abs(vy)
    else:
        # first collision
        idx = ball.collidelist(bricks)
        if idx != -1:
            brick = bricks[idx]
            # what side we collided on
            dx = (ball.centerx - brick.centerx) / BRICK_W
            dy = (ball.centery - brick.centery) / BRICK_H
            if abs(dx) > abs(dy):
                vx = copysign(abs(vx), dx)
            else:
                vy = copysign(abs(vy), dy)
            del bricks[idx]
            score += 1

    # updated 
    ball.center = (x, y)
    ball.vel = (vx, vy)

def on_mouse_move(pos):
  x, y = pos
  bat.centerx = x
  if(bat.left < 0):
    bat.left = 0
  elif(bat.right > WIDTH):
    bat.right = WIDTH

pgzrun.go()
