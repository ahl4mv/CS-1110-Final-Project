"""
Rebecca Little (rl9ng)
Abbie Levine (ahl4mv)

Galaga-type game

Required features:
    User input - player must press the space bar to shoot and the left and right keys move the ship
    Graphics/images - image of space ship and enemy ships coming from the top of the screen, as well
        as coins to be collected
    Start Screen - black screen with white text giving instructions and "Press space to begin."

Optional features:
    Enemies - coming from the top of the screen that the ship must shoot and not get hit by either
        the enemy ship or the enemy ships' bullets
    Collectibles - coins coming from the top of the screen that the ship can shoot for extra points
        for every 5 coins collected a new life is given
    Health meter - the ship has three lives and each time the ship gets shot or the enemies collide
        with the ship, a life is lost
        **once all lives are lost, the game is over**
    Running score - keeps a count of the score based on the amount of enemies shot
    Pause/Play feature
        game pauses when you press p and plays/resumes when you press r
"""


import pygame
import gamebox
import random
camera = gamebox.Camera(800, 600)
game_on = False
TICKS_PER_SECOND = 30

# title screen creation
title = gamebox.from_text(400, 150, "OH SHIP!", 120, "yellow")
names = gamebox.from_text(400, 200, 'Rebecca Little (rl9ng) and Abbie Levine (ahl4mv)', 30, "white")
instructions1 = gamebox.from_text(400, 250, "How to play: ", 50, "white")
instructions2 = gamebox.from_text(400, 275, "Use the space bar to shoot from your ship at enemy ships.", 25, "white")
instructions3 = gamebox.from_text(400, 300, "Use the left and right arrow keys to move your ship.", 25, "white")
instructions4 = gamebox.from_text(400, 325, "The object of the game is to shoot as many enemy ships as possible.", 25, "white")
instructions5 = gamebox.from_text(400, 350, "You have three lives! Collect 5 coins to gain a life.", 25, "white")
instructions6 = gamebox.from_text(400, 375, "Press SPACE to start, P to pause, and R to resume", 25, "white")

# ship creation
ship = gamebox.from_image(400, 550, "ship.png")
ship.velocity = 0
ship.xspeed = 0
ship.yspeed = 0

# initial variables
enemies = []
bullets = []
ebullets = []
collectables = []
collected = 0
coin_total = 0
ticker = 0
ticker1 = 0
ticker2 = 0
lives = 3
pause = False
die = False

# life count / score creation
life_count = gamebox.from_text(50, 575, 'Lives: ' + str(lives), 25, 'yellow')
score = 0
score_total = gamebox.from_text(700, 575, "Score: " + str(score), 25, "white", bold=True)
background = gamebox.from_image(400, 300, 'background.jpg')

def galaga(keys):
#global variables
    global game_on
    global ticker
    global ticker1
    global ticker2
    global lives
    global life_count
    global collected
    global coin_total
    global score
    global score_total
    global pause
    global die
    camera.clear("black")

    die = False
# title screen
    if game_on is False:
        camera.draw(background)
        camera.draw(instructions1)
        camera.draw(instructions2)
        camera.draw(instructions3)
        camera.draw(instructions4)
        camera.draw(instructions5)
        camera.draw(instructions6)
        camera.draw(names)
        camera.draw(title)

# turning game on
    if pygame.K_SPACE in keys:
        game_on = True

    if pygame.K_p in keys:
        pause = True

    if pygame.K_r in keys:
        pause = False

# moving ship
    if pause == False:
        if game_on:
            camera.draw(background)
            camera.draw(life_count)
            ship.move_speed()
            if pygame.K_RIGHT in keys:
                ship.xspeed = 10
                ship.move_speed()
                ship.xspeed = 0
                ship.move_speed()
            if ship.left > camera.right:
                ship.x = 0
            if pygame.K_LEFT in keys:
                ship.xspeed = -10
                ship.move_speed()
                ship.xspeed = 0
                ship.move_speed()
            if ship.right < camera.left:
                ship.x = 800

# making the ship shoot
        if game_on:
            if pygame.K_SPACE in keys:
                bullet = gamebox.from_text(ship.x, ship.y, 'I', 16, 'white', bold=True)
                bullet.yspeed = -10
                bullets.append(bullet)
                keys.remove(pygame.K_SPACE)
            for bullet in bullets:
                bullet.move_speed()
                camera.draw(bullet)

# draw enemies
            x = random.randrange(0,27)
            if ticker1 == x:
                enemy_ship = gamebox.from_image(random.randrange(0,800), 0, "enemy_ship.png")
                camera.draw(enemy_ship)
                enemies.append(enemy_ship)
            ticker1 = 0

# moving/removing ships and keeping score
            for enemy_ship in enemies:
                camera.draw(enemy_ship)
                enemy_ship.yspeed = 5
                if ticker % 10 == 0:
                    enemy_ship.xspeed = random.randrange(-10, 10)
                enemy_ship.move_speed()
                if enemy_ship.top > camera.bottom:
                    enemies.remove(enemy_ship)
                for bullet in bullets:
                    if bullet.touches(enemy_ship):
                        enemies.remove(enemy_ship)
                        bullets.remove(bullet)
                        score += 100
                        score_total = gamebox.from_text(700, 575, "Score: " + str(score), 25, "white", bold=True)

# making enemies shoot
                a = random.randrange(25,60)
                if ticker % a == 4:
                    ebullet = gamebox.from_text(enemy_ship.x, enemy_ship.y, 'I', 16, 'white', bold=True)
                    ebullet.yspeed = 5
                    ebullets.append(ebullet)
                for ebullet in ebullets:
                    camera.draw(ebullet)
                    ebullet.move_speed()

# removing lives when hit by an enemy ship or its bullet
                if lives != 0:
                    if enemy_ship.touches(ship):
                        die = True
                        enemies.clear()
                        bullets.clear()
                        lives -= 1
                        ship.x = 400
                        life_count = gamebox.from_text(50, 575, 'Lives: ' + str(lives), 25, 'yellow')
                    for ebullet in ebullets:
                        if ebullet.touches(ship):
                            die = True
                            enemies.clear()
                            bullets.clear()
                            lives -= 1
                            ship.x = 400
                            life_count = gamebox.from_text(50, 575, 'Lives: ' + str(lives), 25, 'yellow')
                    if lives != 0:
                        camera.draw(life_count)

# ending games when lives are out
                if lives == 0:
                    camera.draw(background)
                    end = gamebox.from_text(400, 300, 'YOU LOSE!', 150, 'red', bold=True)
                    camera.draw(end)
                    gamebox.pause()

# collectables
            y = random.randrange(0, 500)
            if ticker2 == y:
                collectable = gamebox.from_image(random.randrange(0, 800), 0, "coin.png")
                camera.draw(collectable)
                collectables.append(collectable)
            ticker2 = 0
            if lives != 0:
                collect_count = gamebox.from_text(150, 575, "Coins: " + str(coin_total), 25, "white")
                camera.draw(collect_count)

# moving/removing collectables
            for collectable in collectables:
                if lives != 0:
                    camera.draw(collectable)
                collectable.yspeed = 5
                collectable.move_speed()
                if collectable.top > camera.bottom:
                    collectables.remove(collectable)
                if ship.touches(collectable):
                    collectables.remove(collectable)
                    collected += 1
                    coin_total += 1
                if collected == 5:
                    lives += 1
                    coin_total = 0
                    life_count = gamebox.from_text(50, 575, 'Lives: ' + str(lives), 25, 'yellow')
                    collected = 0
                    camera.draw(life_count)

#pause/play
    if pause:
        pauses = gamebox.from_text(400,300, 'PAUSE', 100, 'yellow', bold=True)
        camera.draw(background)
        for enemy_ship in enemies:
            camera.draw(enemy_ship)
        for ebullet in ebullets:
            camera.draw(ebullet)
        for bullet in bullets:
            camera.draw(bullet)
        for collectable in collectables:
            camera.draw(collectable)
        camera.draw(pauses)


# drawing everything
    if game_on:
        if lives != 0:
            for ebullet in ebullets:
                camera.draw(ebullet)
                ebullet.move_speed()
            if die:
                ebullets.clear()
            if pause:
                for ebullet in ebullets:
                    ebullet.yspeed = 0
                    ebullet.move_speed()
            if not pause:
                for ebullet in ebullets:
                    ebullet.yspeed = 5
                    ebullet.move_speed()
    camera.draw(ship)
    camera.draw(score_total)
    camera.display()
    ticker += 1
    ticker1 += 1
    ticker2 += 1


gamebox.timer_loop(TICKS_PER_SECOND, galaga)
