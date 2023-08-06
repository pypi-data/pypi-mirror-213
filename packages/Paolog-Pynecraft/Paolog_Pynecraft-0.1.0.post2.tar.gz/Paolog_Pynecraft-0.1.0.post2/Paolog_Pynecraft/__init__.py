from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.window import *
import os
import sys
from math import *
import time

app = Ursina()
player = FirstPersonController()
spawn_position = player.position #get spawn position
pycr_version = "Pynecraft 0.1.0"
HB = HealthBar(bar_color=color.red, scale=(0.6, 0.05), max_value=20)
HB.position = (-.6,-.35,0)
#SB = HealthBar(bar_color=color.lime, scale=(0.6, 0.05), max_value=10)
#SB.position = (0,-.35,0)
ra_texture = load_texture('assets/rs/images/ra2')
sky_day_texture = load_texture('assets/rs/images/skybox_day.png')
sky_night_texture = load_texture('assets/rs/images/skybox_night.png')
arm_texture = load_texture('assets/rs/images/arm_texture.png')
nothing_texture = load_texture('invalid/directory/for/put/nothing')
cross_cursor = load_texture('assets/rs/images/cursor')
invisible = load_texture('assets/rs/images/nothing')
grass_texture = load_texture('assets/rs/images/grass_block.png')
stone_texture = load_texture('assets/rs/images/stone_block.png')
brick_texture = load_texture('assets/rs/images/brick_block.png')
dirt_texture = load_texture('assets/rs/images/dirt_block.png')
bedrock_texture = load_texture('assets/rs/images/bedrock_block.png')
glass_texture = load_texture('assets/rs/images/glass_block.png')
basic_wood_texture = load_texture('assets/rs/images/basic_wood_block')
basic_wood_planks_texture = load_texture('assets/rs/images/basic_wood_planks_block')
error_texture = load_texture('assets/rs/images/error_debug_block')
water_texture = load_texture('assets/rs/images/water_block')
pycr_logo_texture = load_texture('assets/rs/images/pycr_logo.png')
punch_sound = Audio('assets/rs/sounds/punch_sound',loop = False, autoplay = False)
glass_sound = Audio('assets/rs/sounds/glass_sound',loop = False, autoplay = False)
boss1_sound = Audio('assets/rs/sounds/boss1', loop = True, autoplay = True)
kill_sound = Audio('assets/rs/sounds/kill', loop = False, autoplay = False)
crash_sound = Audio('assets/rs/sounds/kill', loop = True, autoplay = False)
block_pick = 1
block_texture = grass_texture
sky_texture = sky_day_texture
global escmenuenabled
escmenuenabled = False
global isplayerkilled
isplayerkilled = False
global retb
retb = False
global cameraposition
cameraposition = "normal"
window.fps_counter.enabled = True
window.exit_button.visible = False
window.title = pycr_version
window.icon = 'game_assets/icon.ico'
window.borderless = False
window.show_cursor = False
camera.z -= 5
gravity = 1

render_distance = 25


def crash():
	def loop():
		time.sleep(3)
		crash_sound.play()
		time.sleep(3)
		crash_sound.play()
		time.sleep(1)
		crash_sound.play()
		time.sleep(0.5)
		crash_sound.play()
		loop()
	loop()
	time.sleep(20)
	application.quit

def kill():
	global isplayerkilled
	global respawnb
	global quitb
	isplayerkilled = True
	if isplayerkilled == True:	
		execatonce = False
		player.enabled = False
		quitb=Button(text="Quit The Game", color=color.lime, text_color=color.gray, scale=.25, position=(.0,-.2))
		quitb.tooltip=Tooltip("Click here for quit the game")
		quitb.on_click = application.quit
		respawnb=Button(text="Respawn", color=color.lime, text_color=color.gray, scale=.25, position=(.0,.2))
		respawnb.tooltip=Tooltip("Click here for respawn")
		respawnb.on_click = respawn
		kill_sound.play()
	
def damage(power):
	HB.value = HB.value - power
	
def heal(power):
	HB.value = HB.value + power

def sprint_damage(power):
	SB.value = SB.value - power
	
def sprint_heal(power):
	SB.value = SB.value + d
	
def returntogame():
	global escmenuenabled
	player.enabled = True
	escmenuenabled = False
	retb = True
	destroy(escmenuquitb)
	destroy(escmenuretb)
	
def respawn():
	global isplayerkilled
	global quitb
	global respawnb
	player.enabled = True
	HB.value = 20
	isplayerkilled = False
	destroy(quitb)
	destroy(respawnb)
	player.position = spawn_position
	  
def update():
	global block_pick
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "--noboss":
			print("No Boss,OK")
		if sys.argv[1] == "--boss":
			move_entity(speed=1.5, knowback=False, gravity=-1)
			move_entity(e1=mra, speed=2, gravity=-1)
	
	if HB.value == 0:
		kill()

	if player.enabled == True:
		if held_keys['left mouse'] or held_keys['right mouse']:
			hand.active()
		else:
			hand.passive()
	
	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4
	if held_keys['5']: block_pick = 5
	if held_keys['6']: block_pick = 6
	if held_keys['7']: block_pick = 7
	if held_keys['8']: block_pick = 8
	if held_keys['9']: block_pick = 9
#mob	
#set mob to an acronyme for move_entity
#mob code
class RickAstley(Entity):
	def __init__(self, position = (0,3,0)):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/rs/objects/default_obj',
			texture = ra_texture,
			scale = 10,
			collider = "box")
ra = RickAstley(position=(10, 0, 20))
boss1_sound.play()			

class MiniRickAsltey(Entity):
	def __init__(self, position = ra.position):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/rs/objects/default_obj',
			texture = ra_texture,
			scale = 2.75,
			collider = "box")
mra = MiniRickAsltey()
			
#show player
class CameraPlayer(Entity):
	def __init__(self, position = (0,0,0)):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/rs/objects/default_obj',
			scale = player.scale,
			texture = invisible)
	def update(self):
		caplpos = player.position + Vec3(0, player.height, 0)
		self.position = caplpos
		self.rotation = player.rotation
		
#blocks	
deactivated_blocks = []
all_blocks = []
prev_player_position = player.position
refresh_rate = render_distance / 2

class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/rs/objects/block.obj',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			highlight_color = color.lime,
			scale = 0.5,
			collider = 'box')
		all_blocks.append(self)
			
		if self.texture == water_texture:
			self.collision = False
			
	#def update(self):
	#	for block in all_blocks:
	#		dist = distance(block.position, player.position)
	#		if dist < render_distance:
	#			if block.position in deactivated_blocks:
	#				deactivated_blocks.remove(block.position)
	#			block.visible = True
	#			block.ignore = False
	#			block.enabled = True
	#		else:
	#			if block.position not in deactivated_blocks:
	#				deactivated_blocks.append(block.position)
	#			block.visible = False
	#			block.ignore = True
	#			block.enabled = False
	def update(self):
		global prev_player_position
		if player.position is None or distance(player.position, prev_player_position) > refresh_rate:
			prev_player_position = player.position
			for block in all_blocks:
				dist = distance(block.position, player.position)
				if dist < render_distance:
					if block.position in deactivated_blocks:
						deactivated_blocks.remove(block.position)
					block.visible = True
					block.ignore = False
					block.enabled = True
				else:
					if block.position not in deactivated_blocks:
						deactivated_blocks.append(block.position)
					block.visible = False
					block.ignore = True
					block.enabled = False

	def input(self,key):
		if self.hovered:
			if key == 'right mouse down':
				if player.enabled == True:
					punch_sound.play()
					if block_pick == 1: block_texture = grass_texture
					if block_pick == 2: block_texture = stone_texture
					if block_pick == 3: block_texture = brick_texture
					if block_pick == 4: block_texture = dirt_texture
					if block_pick == 5: block_texture = bedrock_texture
					if block_pick == 6: block_texture = glass_texture
					if block_pick == 7: block_texture = basic_wood_texture
					if block_pick == 8: block_texture = basic_wood_planks_texture
					if block_pick == 9: block_texture = water_texture
					voxel = Voxel(position = self.position + mouse.normal, texture = block_texture)
							
			if key == 'left mouse down':
				if player.enabled == True:
					if self.texture == bedrock_texture:
						punch_sound.play()
					else:
						if self.texture == glass_texture:
							punch_sound.play()
							destroy(self)
							glass_sound.play()
						else:
							if self.texture == error_texture:
								print("Pynecraft.Block.error_debug_block asked for show 'pycr_infos'")
								print("Memory Device Founded at \\;\Pynecraft.dir\Program.OS\Devices\Memory.Device")
								print("Processor Device Founded at \\;\Pynecraft.dir\Program.OS\Devices\Processor.Device")
								print("GPU Founded at \\;\Pynecraft.dir\Program.OS\Devices\GPU")
								print("Game Founded at \\;\Pynecraft.dir\Game.dir")
								print("pycr Founded at \\;\Pynecraft.Root.Dir\Pynecraft")
								print("pycr_modules Founded at \\;\Pynecraft.Mounted_dir\pycr\modules")
								print("pycr_infos Founded at \\;\Pynecraft.Mounted_dir\pycr\OS.dir\pycr_mounted\infos")
								print("Dependances Founded at \\;\Pynecraft.dir\Python.dir\Dependances.mount\Dependances_dir")
								print("Textures Founded at ./rs/images/")
								print("Objects Founded at ./object")
								print("Sounds Founded at ./sound")
								damage(1)
							else:
								if self.texture == water_texture:
									punch_sound.play()
									destroy(self)
								else:
									punch_sound.play()
									destroy(self)
#add a BoxCollider for collision to entity and voxel
#ra.collider = BoxCollider(ra, center=(0, 0.5, 0), size=(0.5, 1, 0.5))
#Voxel.collider = 'assets/rs/objects/block'
#EscMenu
def input(key):
	if key == 'escape':
		if isplayerkilled == False:
			global escmenuenabled
			global escmenuquitb
			global escmenuretb
			global retb
			if escmenuenabled == False:
				player.enabled = False
				escmenuenabled = True
				escmenuquitb=Button(text="Quit The Game", color=color.lime, text_color=color.gray, scale=.25, position=(.0,-.2))
				escmenuquitb.tooltip=Tooltip("Click here for quit the game")
				escmenuquitb.on_click = application.quit
				escmenuretb=Button(text="Return to The Game", color=color.lime, text_color=color.gray, scale=.25, position=(.0,.2))
				escmenuretb.tooltip=Tooltip("Click here for return to the game")
				escmenuretb.on_click = returntogame
				escmenuenabled = True
			else:
				player.enabled = True
				retb = True
				escmenuenabled = False
				destroy(escmenuquitb)
				destroy(escmenuretb)
	if key == 'c':
		crash()	

#Sky
class Sky(Entity):
	def __init__(self):
		super().__init__(
		parent = scene,
		model = 'sphere',
		texture = sky_texture,
		scale = 150,
		double_sided = True)
	def update(self):
		self.position = player.position
#Hand
class Hand(Entity):
	def __init__(self):
		super().__init__(
		parent = camera.ui,
		model = 'assets/rs/objects/arm',
		texture = arm_texture,
		scale = 0.2,
		rotation = Vec3(150,-10,0),
		position = Vec2(0.4,-0.6))
		
	def active(self):
		self.position = Vec2(0.3,-0.5)
		
	def passive(self):
		self.position = Vec2(0.4,-0.6)

#world gen		
for z in range(50):
		for x in range(50):
			voxel = Voxel(position = (x,0,z))
			
def move_entity(e1=ra, e2=player, speed=1.5, gravity=-0.1, y_velocity=0, power=1, isdamaging=True, knowback=True, collisions=True):
	if player.enabled == True:
		direction = (e2.position - e1.position).normalized()
		distance = (e2.position - e1.position).length()
		e1.rotation_y = atan2(direction.x, direction.z) * 180 / pi
		if distance > 1:
			e1.position += direction + Vec3(0, gravity, 0)* speed * time.dt
		if distance < 1:
			if isdamaging == True:
				damage(power)
				if knowback == True:
					e1.position = e1.position + Vec3(1, 0.5, 1)
		if collisions == True:
			hit_info = e1.intersects()
			if hit_info.hit:
				e1.position = e1.position + Vec3(0, 0.1, 0)
				print("AAAH, BBBBBBBh")
	
camera.position = player.position
camera.rotation = player.rotation
		
sky = Sky()
hand = Hand()
capl = CameraPlayer()

app.run()
