import pygame
import combat_gfx
import explore_combo
import explore_gfx
import combat_handler
import pc
import assassin
import druid
import monster
class screen_machine:
	screen_width=320*4
	screen_height=200*4
	
	state = 0
	
	combat_render = None
	ch = None ##combat handler
	explore_module = None
	
	party = []
	creature_group = []
	monster1 = monster.monster("Lizard-Man", None, 6, 10, 3,  6, 0, 0)
	
	gameFlag = True
	
	enterFlag = False ##flag for checking if you hit enter
	
	def __init__(self):
		#init pygame module
		pygame.init()
		
		#load and set the logo
		logo = pygame.image.load("logo.png")
		pygame.display.set_icon(logo)
		pygame.display.set_caption("Chalice II: Dodecahedronite")
		
		#create a surface on screen that has the size of 400x300
		screen_width = self.screen_width
		screen_height = self.screen_height
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		
		self.explore_module = explore_combo.explore_handler()
		self.combat_render = combat_gfx.combat_gfx() ##WORKS
		
	
		
		self.party.clear()
		self.creature_group.clear()
	
		player = druid.druid("Player", 10, 15, 9)
		self.party.append(player)
		
		self.explore_module.setPc(player)
	
	def render(self):
		if self.state==0:
			self.explore_module.render(self.screen)
		elif self.state==1:
			self.combat_render.drawScreen(self.screen, self.ch.getState(), self.ch.getPartyStrList(), 
	self.ch.getMonsterStrList(), self.ch.getOptionStringList(), self.ch.getContextStringList())
		elif self.state==2:
			self.explore_module.render_attack_popup(self.screen, self.generateCombatString())
			
		
	def handle_input(self, i):
		if self.state==0:
			return self.explore_module.handleInput(i)
		elif self.state==1:
			return self.ch.handleInput(i)
		elif self.state==2:
			if i=="ENTER":
				self.enterFlag=True
				return True
	def getMonsterForLevel(self):
		self.creature_group.clear()
		##print("Ran get monster for level!")
		monster1 = monster.monster("Lizard-Man", None, 6, 10, 3,  6, 0, 0)
		self.creature_group.append(monster1)
	
	def generateCombatHandler(self):
		self.getMonsterForLevel()
		self.ch = combat_handler.combat_handler(self.party, self.creature_group)
		
	def checkState(self):
		if self.state==0:
			if self.explore_module.hasRandomEncounter():
				self.generateCombatHandler()
				self.state=2
			elif self.explore_module.hasFoundExit():
				self.gameFlag = False
		elif self.state==1:
			self.ch.checkState()
			if not self.ch.isCombatRunning():
				self.state=0
			if self.ch.isGameOver():
				self.gameFlag=False
		elif self.state==2: ##menu module for printing "You've been attacked!"
			if self.enterFlag:
				self.state=1
				self.enterFlag=False
	
	##generates string to display that you have been attacked!!!
	def generateCombatString(self):
		outStr = ["You have been attacked by a..."]
		if len(self.creature_group)>1:
			outStr.append("group of " + self.creature_group[0].getName() + "s!")
		else:
			outStr.append("a " + self.creature_group[0].getName())
		return outStr
			
def main(args):
	self = screen_machine()
	in_flag = True
	while (self.gameFlag):
		if (in_flag):
			self.render()
		in_flag = False
		for event in pygame.event.get():
			#only do something if the event is of type quit
			if event.type == pygame.KEYDOWN:
				i = 'x'
				if event.key == pygame.K_q:
					i = 'q'
				if event.key == pygame.K_e:
					i = 'e'			
				if event.key == pygame.K_w:
					i = 'w'	
				if event.key == pygame.K_s:
					i = 's'			
				if event.key == pygame.K_d:
					i = 'd'			
				if event.key == pygame.K_a:
					i = 'a'			
				elif event.key == pygame.K_f:
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
				if (self.handle_input(i)):
					in_flag = True
					self.checkState()
					
   

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
