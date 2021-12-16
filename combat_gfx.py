###graphics test for combat loop
import pygame
import combat_handler
##test only
import pc
import monster
import being
import druid
import assassin
import barbarian
class combat_gfx:
	screen_width=320*4
	screen_height=200*4
	
	frame = pygame.image.load("bgrenders/frame.png")
	context_menu = pygame.image.load("fgrenders/context_menu_hq.png")
	creature_menu = pygame.image.load("fgrenders/creature_menu_hq.png")
	option_menu = pygame.image.load("fgrenders/option_menu_hq.png")

	option_text_x = 320
	option_text_y = 470
	option_text_width = 640
	option_text_height = 180
	
	pc_status_text_x = 310
	pc_status_text_y = 150
	pc_status_text_width = 260
	pc_status_text_height = 220

	monster_status_x = 710
	monster_status_y = 150
	monster_status_text_width = 260
	monster_status_text_height = 220
	
	context_text_x = 390
	context_text_y = 150
	context_text_width = 500
	context_text_height = 220

	
	combat_handler = None ## not to be in final version
	
	def __init__(self):
		print("Combat window initialized")
	
	##handles rendering to screen takes arguments from combat handler
	def drawScreen(self, screen, state, pc_status, monster_status, option_text, context_text):
		screen.fill((0, 0, 0)) ##DIGI DIGI DIGITAL BLACK fills screen
		if state==1:
			self.drawCreatureStatus(screen, pc_status, monster_status)
			self.drawOption(screen, option_text)
		elif state==2:
			self.drawContext(screen, context_text)
			self.drawOption(screen, option_text)
		elif state==3:
			self.drawContext(screen, context_text)
			self.drawOption(screen, option_text)
		elif state==4:
			self.drawContext(screen, context_text)
			self.drawOption(screen, option_text)
		elif state==7:
			self.drawContext(screen, context_text)
			self.drawOption(screen, option_text)
		##elif state==4:
		pygame.display.flip()
		
		
	##draw context window
	def drawContext(self, screen, context):
		screen.blit(self.context_menu, (0,0))
		context_font = pygame.font.Font('fonts/oldschooladventure.ttf',16)
		self.drawContextFromList(screen, context, context_font)
	
	##draw text for context menu
	def drawContextFromList(self, screen, context, font):
		x = self.context_text_x
		y = self.context_text_y
		
		for line in context:
			context_render = font.render(line, True, (255,255,255))
			screen.blit(context_render, (x,y))
			y+=30
	
	##draws option window with options
	def drawOption(self, screen, option):
		screen.blit(self.option_menu, (0,0))
		option_font = pygame.font.Font('fonts/oldschooladventure.ttf',20)
		self.drawOptionFromList(screen, option, option_font)
	
	def drawOptionFromList(self, screen, option, font):
		x = self.option_text_x
		y = self.option_text_y
		
		for action in option:
			option_render = font.render(action, True, (255,255,255))
			screen.blit(option_render, (x,y))
			y+=30
		
	
	##helpers for rendering		
	def drawCreatureStatus(self, screen, pc_status, monster_status):
		screen.blit(self.creature_menu, (0,0)) ##renders the .png of the creature_menu
		status_font = pygame.font.Font('fonts/oldschooladventure.ttf',14)
		
		self.drawPCStatusFromList(screen, pc_status, status_font)
		self.drawMonsterStatusFromList(screen, monster_status, status_font)
		
	##draws pcstatus string to screen at proper position
	def drawPCStatusFromList(self, screen, pc_status, font):
		x = self.pc_status_text_x
		y = self.pc_status_text_y
		
		for status in pc_status:
			pc_render = font.render(status, True, (255,255,255))
			screen.blit(pc_render, (x,y))
			y+=20
			
	##draws monster status string at proper position
	def drawMonsterStatusFromList(self, screen, monster_status, font):
		x = self.monster_status_x
		y = self.monster_status_y
		
		for status in monster_status:
			monster_render = font.render(status, True, (255,255,255))
			screen.blit(monster_render, (x,y))
			y+=20
	
	
def main(args):		
	##TODO: Implement treasure checks, implement spellcasting, work on 
	##char creation
	combat_render = combat_gfx()
	
	#init pygame module
	pygame.init()
	
	#load and set the logo
	logo = pygame.image.load("logo.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("Chalice II: Escape from Quadrahedron")
	
	#create a surface on screen that has the size of 1200x600
	screen_width = combat_render.screen_width
	screen_height = combat_render.screen_height
	screen = pygame.display.set_mode((screen_width, screen_height))
	
	player = assassin.assassin("Pete", 10, 15, 9)
	player2 = druid.druid("Hermetizoid", 8, 10, 14)
	player3 = barbarian.barbarian("Conan", 14, 10, 6)
	goblin = monster.monster("Goblinoid", None, 6, 10, 3,  6, 0, 0)
	lizard_man = monster.monster("Lizard-Man", None, 6, 10, 3,  6, 0, 0)
	party = [player, player3]
	monsters = [goblin]
	ch = combat_handler.combat_handler(party, monsters)
	combat_render.drawScreen(screen, ch.getState(), ch.getPartyStrList(), 
	ch.getMonsterStrList(), ch.getOptionStringList(), ch.getContextStringList())
	
	while (ch.isCombatRunning()):
		in_flag = False
		for event in pygame.event.get():
			#only do something if the event is of type quit
			if event.type == pygame.QUIT: ##like closingwindow
				ch.setCombatRunning(False)
			if event.type == pygame.KEYDOWN:
				i = 'x'
				if event.key == pygame.K_f:
					i='f'
				elif event.key == pygame.K_r:
					i='r'
				elif event.key == pygame.K_p:
					i='p'
				elif event.key == pygame.K_c:
					i='c'
				elif event.key == pygame.K_1:
					i='1'
				elif event.key == pygame.K_2:
					i='2'
				elif event.key == pygame.K_3:
					i='3'
				elif event.key == pygame.K_4:
					i='4'
				elif event.key == pygame.K_RETURN:
					i="ENTER"
				if (ch.handleInput(i)):
					ch.checkState()
					combat_render.drawScreen(screen, ch.getState(), ch.getPartyStrList(), 
	ch.getMonsterStrList(), ch.getOptionStringList(), ch.getContextStringList())
	
	party = [player, player3]
	monsters = [goblin]
	ch = combat_handler.combat_handler(party, monsters)
	combat_render.drawScreen(screen, ch.getState(), ch.getPartyStrList(), 
	ch.getMonsterStrList(), ch.getOptionStringList(), ch.getContextStringList())
	
	while (ch.isCombatRunning()):
		in_flag = False
		for event in pygame.event.get():
			#only do something if the event is of type quit
			if event.type == pygame.QUIT: ##like closingwindow
				ch.setCombatRunning(False)
			if event.type == pygame.KEYDOWN:
				i = 'x'
				if event.key == pygame.K_f:
					i='f'
				elif event.key == pygame.K_r:
					i='r'
				elif event.key == pygame.K_p:
					i='p'
				elif event.key == pygame.K_c:
					i='c'
				elif event.key == pygame.K_1:
					i='1'
				elif event.key == pygame.K_2:
					i='2'
				elif event.key == pygame.K_3:
					i='3'
				elif event.key == pygame.K_4:
					i='4'
				elif event.key == pygame.K_RETURN:
					i="ENTER"
				if (ch.handleInput(i)):
					ch.checkState()
					combat_render.drawScreen(screen, ch.getState(), ch.getPartyStrList(), 
	ch.getMonsterStrList(), ch.getOptionStringList(), ch.getContextStringList())

if __name__ == '__main__':
	##TODO reset character stats and temp bonuses and spells after 
	##combat
    import sys
    sys.exit(main(sys.argv))
