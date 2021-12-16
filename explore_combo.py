import pygame
import random

class explore_handler():
	pygame.init()
	screen_width=320*4
	screen_height=200*4
	##CARDINAL DIRECTIONS
	NORTH=[0,-1]
	SOUTH=[0, 1]
	EAST=[1,0]
	WEST=[-1,0]
	
	##relative direction
	up=NORTH
	down=SOUTH
	left=WEST
	right=EAST
	
	#rotation ('n', 's', 'e', 'w')
	rotation=0
	
	game_map=""
	
	##camPos
	camPosX = 1
	camPosY = 1
			  #0123456789
	game_map+="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"#0
	game_map+="x.xx.....xxxx.......xx..x.e.x.cx"#1
	game_map+="x.xx..c..xxxx.xxxxxxxx..x...x..x"#2
	game_map+="x......xxxxxx..................x"#3
	game_map+="xxxxxdxx.xxxxxdxxxxxx...x...x..x"#4
	game_map+="xc.......xxxxx.xxxxxxxxxxxxxxxxx"#5
	game_map+="xxxxxxxx.xxxxx.x...............x"#6
	game_map+="x.....x..xxxx...xxxx.xxxx.x.x.xx"#7
	game_map+="x.xc...x.........x..x.x.xx.x.x.x"
	game_map+="x..x.x.xxxxxxxxx....x.x.xx.x.x.x"
	game_map+="x....x.........d....x.x........x"
	game_map+="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	
	map_width = 32
	map_height = 12
	
	turn = 1
	
	mFarWall = pygame.image.load("bgrenders/MidFarWall_hq.png")
	lFarWall = pygame.image.load("bgrenders/LefFarWall_hq.png")
	rFarWall = pygame.image.load("bgrenders/RigFarWall_hq.png")
	
	mNearWall = pygame.image.load("bgrenders/MidNearWall_hq.png")
	lNearWall = pygame.image.load("bgrenders/LefNearWall_hq.png")
	rNearWall = pygame.image.load("bgrenders/RigNearWall_hq.png")
	
	lCloseWall = pygame.image.load("bgrenders/LefCloseWall_hq.png")
	rCloseWall = pygame.image.load("bgrenders/RigCloseWall_hq.png")
	
	mCloseChest = pygame.image.load("objects/MidCloseChest.png")
	lCloseChest = pygame.image.load("objects/LefCloseChest.png")
	rCloseChest = pygame.image.load("objects/RigCloseChest.png")
	
	mNearChest = pygame.image.load("objects/MidNearChest.png")
	lNearChest = pygame.image.load("objects/LefNearChest.png")
	rNearChest = pygame.image.load("objects/RigNearChest.png")
	
	mCloseTD = pygame.image.load("objects/MidCloseTD.png")
	lCloseTD = pygame.image.load("objects/LefCloseTD.png")
	rCloseTD = pygame.image.load("objects/RigCloseTD.png")
	
	mNearTD = pygame.image.load("objects/MidNearTD.png")
	lNearTD = pygame.image.load("objects/LefNearTD.png")
	rNearTD = pygame.image.load("objects/RigNearTD.png")
	
	mFarDoor = pygame.image.load("bgrenders/MidFarDoor.png")
	lFarDoor = pygame.image.load("bgrenders/LefFarDoor.png")
	rFarDoor = pygame.image.load("bgrenders/RigFarDoor.png")
	
	lNearDoor = pygame.image.load("bgrenders/LefNearDoor.png")
	rNearDoor = pygame.image.load("bgrenders/RigNearDoor.png")
	mNearDoor = pygame.image.load("bgrenders/MidNearDoor.png")
	
	lCloseDoor = pygame.image.load("bgrenders/LefCloseDoor.png")
	rCloseDoor = pygame.image.load("bgrenders/RigCloseDoor.png")
	
	
	frame = pygame.image.load("bgrenders/frame_hq.png")
	
	popupWindow = pygame.image.load("fgrenders/explore_popup.png")
	
	popupFont = pygame.font.Font('fonts/oldschooladventure.ttf',16)
	
	pc_info_tab = pygame.image.load("fgrenders/pc_info_tabs.png")
	pc_info_font = pygame.font.Font('fonts/oldschooladventure.ttf',16)
	pc_info_list = []
	
	pc_info_x = 50
	pc_info_y = 100
	
	exitFlag = False
	popupFlag = False
	popupText = ""
	pup_x = 450
	pup_y = 290
	
	pc = None
	
	moveFlag = True
	
	##allocates rotation
	def rotate(self, i):
		self.rotation+=i
		if self.rotation>3:
			self.rotation=0
		if self.rotation<0:
			self.rotation=3
		self.setRelativeDirection()
			
	
	##returns relative direction from current rotation
	def getRelativeDirection(self, rotation):
		if rotation==0:
			return [self.NORTH, self.SOUTH, self.EAST, self.WEST]
		elif rotation==1:
			return [self.EAST, self.WEST, self.SOUTH, self.NORTH] ##issues
		elif rotation==2:
			return [self.SOUTH, self.NORTH, self.WEST, self.EAST]
		elif rotation==3:
			return [self.WEST, self.EAST, self.NORTH, self.SOUTH]
	
	##allocate relativeDirection
	def setRelativeDirection(self):
		fwd, bcwd, rigt, left = self.getRelativeDirection(self.rotation)
		
		self.up = fwd
		self.down = bcwd
		self.right = rigt
		self.left = left
	
	##retrieves sprites to be rendered
	def getRenderedSprites(self):
		outSprites = []
		
		xPos = self.camPosX
		yPos = self.camPosY
		
		closeL = [xPos+self.left[0], yPos+self.left[1]]
		closeR = [xPos+self.right[0],yPos+self.right[1]]
		
		nearM = [xPos+self.up[0], yPos+self.up[1]]
		nearL = [xPos + self.up[0] + self.left[0], yPos + self.up[1] + self.left[1]]
		nearR = [xPos + self.up[0] + self.right[0], yPos + self.up[1] + self.right[1]]
		
		farM = [xPos + 2*self.up[0], yPos + 2*self.up[1]]
		farL = [xPos + 2*self.up[0] + self.left[0], yPos + 2*self.up[1] + self.left[1]] 	
		farR = [xPos + 2*self.up[0] + self.right[0], yPos + 2*self.up[1] + self.right[1]]
		
		
		
		##check for out of bounds here
		
		##Render BG
		
		##Left Far Wall
		if (self.getTile(farL[0], farL[1])=='x'): ##wall
			outSprites.append(self.lFarWall)
		if (self.getTile(farL[0], farL[1])=='d'): ##door
			outSprites.append(self.lFarDoor)
		#Right Far Wall
		if (self.getTile(farR[0], farR[1])=='x'):
			outSprites.append(self.rFarWall)
		if (self.getTile(farR[0], farR[1])=='d'):
			outSprites.append(self.rFarDoor)
		
		##MID FAR WALL
		if (self.getTile(farM[0], farM[1])=='x'):
			outSprites.append(self.mFarWall)
		elif (self.getTile(farM[0], farM[1])=='d'):
			outSprites.append(self.mFarDoor)
			
		##LEFT NEAR WALL	
		if (self.getTile(nearL[0], nearL[1])=='x'):
			outSprites.append(self.lNearWall)
		if (self.getTile(nearL[0], nearL[1])=='d'):
			outSprites.append(self.lNearDoor)
		if (self.getTile(nearL[0], nearL[1])=='e'):
			outSprites.append(self.lNearTD)
		if (self.getTile(nearL[0], nearL[1])=='c'):
			outSprites.append(self.lNearChest)
			
			
		if (self.getTile(nearR[0], nearR[1])=='x'):
			outSprites.append(self.rNearWall)
		if (self.getTile(nearR[0], nearR[1])=='d'):
			outSprites.append(self.rNearDoor)
		if (self.getTile(nearR[0], nearR[1])=='e'):
			outSprites.append(self.rNearTD)
		if (self.getTile(nearR[0], nearR[1])=='c'):
			outSprites.append(self.rNearChest)
			
		if (self.getTile(nearM[0], nearM[1])=='x'):
			outSprites.append(self.mNearWall)
		if (self.getTile(nearM[0], nearM[1])=='d'):
			outSprites.append(self.mNearDoor)
		if (self.getTile(nearM[0], nearM[1])=='e'):
			outSprites.append(self.mNearTD)
		if (self.getTile(nearM[0], nearM[1])=='c'):
			outSprites.append(self.mNearChest)
			
		if (self.getTile(closeR[0], closeR[1])=='c'):
			outSprites.append(self.rCloseChest)		
			
		if (self.getTile(closeL[0], closeL[1])=='c'):
			outSprites.append(self.lCloseChest)
		if (self.getTile(closeL[0], closeL[1])=='x'):
			outSprites.append(self.lCloseWall)
		if (self.getTile(closeL[0], closeL[1])=='d'):
			outSprites.append(self.lCloseDoor)
		if (self.getTile(closeL[0], closeL[1])=='e'):
			outSprites.append(self.lCloseTD)	
		
			
		if (self.getTile(closeR[0], closeR[1])=='x'):
			outSprites.append(self.rCloseWall)
		if (self.getTile(closeR[0], closeR[1])=='d'):
			outSprites.append(self.rCloseDoor)
		if (self.getTile(closeR[0], closeR[1])=='e'):
			outSprites.append(self.rCloseTD)
		
		outSprites.append(self.frame)
		
		return outSprites
		
		##return [closeL, closeR, nearM, nearL, nearR, farM, farL, farR]
		
	##retrieves tile from map string
	def getTile(self, x, y):
		if (x >= 0 and x < self.map_width and y>= 0 and y < self.map_height):
			return self.game_map[y * self.map_width + x] 
		else:
			return ' '
			
	##sets tile at an x/y position		
	def setTile(self, x, y, c):
		if (x >= 0 and x < self.map_width and y>= 0 and y < self.map_height):
			index = y*self.map_width + x
			self.game_map = self.game_map[0:index] + c + self.game_map[index+1: ]
			##self.game_map[y * self.map_width + x] = c
			

	def drawScreen(self, screen, sprites):
		screen.fill((0, 0, 0))
		for sprite in sprites:
			screen.blit(sprite, (0,0))
		if self.popupFlag:
			popupText = self.popupFont.render(self.popupText, True, (255,255,255))
			screen.blit(self.popupWindow, (0,0))
			screen.blit(popupText, (self.pup_x, self.pup_y))
		screen.blit(self.pc_info_tab, (0,0))
		self.drawPcInfo(screen)
		pygame.display.flip()
		
	def render(self, screen):
		sprites = self.getRenderedSprites()
		self.drawScreen(screen, sprites)
	
	##renders popup when you're attacked!
	def render_attack_popup(self, screen, attackString):
		screen.fill((0, 0, 0))
		mod_y = 0
		screen.blit(self.popupWindow, (0,0))
		for line in attackString:
			popupText = self.popupFont.render(line, True, (255,255,255))
			screen.blit(popupText, (self.pup_x, self.pup_y+mod_y))
			mod_y+=20
		
		pygame.display.flip()
	
	##handles input
	def handleInput(self, i):
		mod = [0,0]
		collide=False
		self.setMove(True)
		in_flag = True ##whether is a valid input
		self.popupFlag = False
		if i=='q':
			self.rotate(-1)
		elif i=='e':
			self.rotate(1)
		elif i=='w':
			mod = self.up
		elif i=='s':
			mod = self.down
		elif i=='a':
			mod = self.left
		elif i=='d':
			mod = self.right
		else:
			in_flag = False
		nextX = self.camPosX+mod[0]
		nextY = self.camPosY+mod[1]
		nextTile = self.getTile(nextX, nextY)
	
		if nextTile=='x' or nextTile=='l':
			collide=True
		elif nextTile=='c':
			self.allocateGoldChest(1)
			self.setTile(nextX, nextY, '.')
		elif nextTile=='e':
			self.setExitFlag(True)
		if (collide==False):
			self.camPosX = (self.camPosX + mod[0]) 
			self.camPosY = (self.camPosY + mod[1]) 
			self.turn+=1
		return in_flag
	
	##game code
	
	##sets player character
	def setPc(self, pc):
		self.pc = pc
		self.pc_info_list= [self.pc.getName(), self.pc.getJob(), "level:", "str:", "dex:", "int:", "hp:", "gp:", "ac:"]
		
	def getPcInfo(self):
		self.pc_info_list[2] = "level:" + str(self.pc.getLevel())
		self.pc_info_list[3] = "str:" + str(self.pc.getStr())
		self.pc_info_list[4] = "dex:" + str(self.pc.getDex())
		self.pc_info_list[5] = "int:" + str(self.pc.getInt())
		self.pc_info_list[6] = "hp:" + str(self.pc.getHp())
		self.pc_info_list[7] = "gp:" + str(self.pc.getGp())
		self.pc_info_list[8] = "ac:" + str(self.pc.getAc())
	
	def drawPcInfo(self, screen):
		mod_y = 0
		self.getPcInfo()
		for line in self.pc_info_list:
			pc_info_text = self.pc_info_font.render(line, True, (255,255,255))
			screen.blit(pc_info_text, (self.pc_info_x, self.pc_info_y+mod_y))
			mod_y+=50
		
	
	def hasRandomEncounter(self):
		print("rolling for random encounter!")
		if (self.turn%6==1):
			dice = random.randint(1, 6)
			print(str(dice))
			if dice==1:
				self.setMove(False)
				return True
			else:
				return False
		else:
			return False
	
	##return gold from chest
	def getGoldChest(self, level):
		dice = random.randint(1, 6)
		gold = dice * pow(2, level)
		return gold
		
	def allocateGoldChest(self, level):
		dice = random.randint(1, 6)
		gold = dice * pow(2, level)
		self.pc.addGp(gold)
		self.setPopup("You found " + str(gold) + " gp!") 
	
	##sets exit flag when you find trapdoor
	def setExitFlag(self, state):
		self.exitFlag=state
	
	##checks whether exit has been found
	def hasFoundExit(self):
		return self.exitFlag
	
	##sets popup text and sets popup flag to true
	def setPopup(self, text):
		self.popupText=text
		self.popupFlag=True
	
	##clears popup window
	def clearPopup(self):
		self.popupFlag=False
		self.popupText=""
		
	##returns whether character can move
	def canMove(self):
		return self.moveFlag
	
	def setMove(self, flag):
		self.moveFlag = flag
		
		 
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
