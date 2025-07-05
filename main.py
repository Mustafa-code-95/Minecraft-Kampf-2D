from ursina.prefabs.audio import Audio
from ursina import camera
from ursina import time
from ursina import application
from ursina import Ursina
from ursina import Entity
from ursina import Text
from ursina import invoke
from ursina import Button
from ursina import color
from ursina import scene
from ursina import clamp
from ursina import destroy
from ursina import held_keys
import random
import threading


rid = 0
score_thread_started = False
game_win = False
d = 0.6
game_over = False
leben = 3
s = 59
y = random.randint(-7, 7)
x = random.randint(-4, 4)
r = 0
er = 0
min_x = -10
max_x = 10
min_y = -6
max_y = 6
name = None
direction = None
herzen = 10
t = ['e', 'm', 'c', 'd']
z = 0
e = ['a', 'b', 'r.jpg', 's', 'f', 'g', 'q', 'k', 'l', 'o', 'p', 'z', 'y', 'v', 'rt', 'r.png', 'mob.gif']
app = Ursina()
boxes = []
camera.orthographic = True
camera.fov = 20
camera.position = 0, -3
music = Audio('', loop=True, autoplay=True)


def random_name():
    global name
    ran = ['a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü']
    kon = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    name = f'{kon[random.randint(0, len(kon)-1)] + ran[random.randint(0, len(ran)-1)] + kon[random.randint(0, len(kon)-1)] + ran[random.randint(0, len(ran)-1)] + kon[random.randint(0, len(kon)-1)]}'

her = Text('', origin=(0,6), scale=1.2, color=color.white)
leben_text = Text('', origin=(0,2), scale=1.2, color=color.black)
game_over_text = Text('', origin=(0,-1), scale=2.8, color=color.gray)

player = Entity(model='cube', color=color.white, scale=1, position=(-9, 5), collider='box', texture='e.jpg')


def update_score():
    if not game_over:
        global rid
        rid += 1
        invoke(update_score, delay=1)


def add_mob(texture, position, name):
    boxes.append(
        Button(
            parent=scene,
            model='cube',
            origin=0.1,
            color=color.white,
            scale=1,
            position=position,
            texture=texture,
            name=name
        )
    )


background = Entity(
    model='quad',
    texture='feld.jpg',
    scale=(20, 12),
    z=1
    )

asa = random.randint(10, 20)

for _ in range(asa):
    y = random.randint(-7, 7)
    x = random.randint(-4, 4)
    random_name()
    add_mob(texture=e[random.randint(0, len(e)-1)], position=(y, x), name=name)


def update():
    global r, game_over, player, direction, leben, d, game_win, t, z, score_thread_started, rid, s, er, leben_text, game_over_text, her, name
    leben_text.text = f"leben:{leben}"
    r = time.dt
    if not score_thread_started:
        threading.Thread(target=update_score, daemon=True).start()
        score_thread_started = True
    if game_win == True and game_over == False:
        er += 1
        for _ in range(30):
            for mob in boxes:
                mob.position += 1, 0 * time.dt * 3
        game_over_text.text = 'The victory\nYou have one min. survived\nClkick (q) for quit'
        if held_keys['q']:
            application.quit()
    if game_over == False and game_win == False:
        if held_keys['a']:
            player.x -= 5 * time.dt
        if held_keys['d']:
            player.x += 5 * time.dt
        if held_keys['s']:
            player.y -= 5 * time.dt
        if held_keys['w']:
            player.y += 5 * time.dt
        if rid > s:
            game_win = True
        for mob in boxes:
            direction = (player.position - mob.position).normalized()
            mob.position += direction * time.dt * d
            if player.intersects(mob).hit:
                her.text = f'{mob.name} hat dich erfolgreich an gegrifen.'
                leben -= 1
                leben_text.text = f"leben:{leben}"
                y = random.randint(-7, 7)
                x = random.randint(-4, 4)
                mob.position = (y, x)
                if leben == 0:
                    her.text = f'{mob.name} hat dich erfolgreich erledigt.'
                    game_over = True
                    player.texture = mob.texture
    if game_over == True and game_win == False:
        for _ in range(30):
            for mob in boxes:
                mob.position += direction * time.dt * 0.7
                player.texture = mob.texture
        game_over_text.text = 'The End\nYou are now a deamon'
        leben_text.text = 'Click (r) for restart and (q) to quit game'
        if held_keys['q']:
            application.quit()
        if held_keys['r']:
            her.text = ''
            for mob in boxes:
                boxes.remove(mob)
                destroy(mob)
            asa = random.randint(10, 20)
            for _ in range(asa):
                y = random.randint(-7, 7)
                x = random.randint(-4, 4)
                random_name()
                add_mob(texture=e[random.randint(0, len(e)-1)], position=(y, x), name=name)
            player.texture = 'e.jpg'
            player.position = (-9, 5)
            game_over_text.text = ''
            game_over = False
            leben = 3
            leben_text.text = f'leben: {leben}'
            rid = 0
    player.x = clamp(player.x, min_x + 0.5, max_x - 0.5)
    player.y = clamp(player.y, min_y + 0.5, max_y - 0.5)

app.run()
