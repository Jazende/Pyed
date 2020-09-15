import pyglet

player_image = pyglet.image.load("resources\\red_circle_p_transparant.png")
player_image.anchor_x = int(player_image.width // 2)
player_image.anchor_y = int(player_image.height // 2)

shot_image = pyglet.image.load("resources\\shot_r_with_start_transparant.png")

enemy_angry_image = pyglet.image.load("resources\\boss_angry_face_transparant.png")
enemy_angry_image.anchor_x = int(enemy_angry_image.width // 2)
enemy_angry_image.anchor_y = int(enemy_angry_image.height // 2)

enemy_shocked_image = pyglet.image.load("resources\\boss_shocked_face_transparant.png")
enemy_shocked_image.anchor_x = int(enemy_shocked_image.width // 2)
enemy_shocked_image.anchor_y = int(enemy_shocked_image.height // 2)

crosshair_image = pyglet.image.load("resources\\black_crosshair_transparant.png")

buff_image = pyglet.image.load("resources\\basic_buff.png")
buff_image.anchor_x = int(buff_image.width // 2)
buff_image.anchor_y = int(buff_image.height // 2)
