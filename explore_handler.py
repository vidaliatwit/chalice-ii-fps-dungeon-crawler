import pygame

class explore_handler():
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
	game_map+="x.xx.....xxxx.......xx..x...x..x"#1
	game_map+="x.xx..xxxxxxx.xxxxxxxx..x...x..x"#2
	game_map+="x......xxxxxx..................x"#3
	game_map+="xxxxx.xx.xxxxx.xxxxxx...x...x..x"#4
	game_map+="x........xxxxx.xxxxxxxxxxxxxxxxx"#5
	game_map+="xxxxxxxx.xxxxx.x...............x"#6
	game_map+="x......x.xxxxx.x.xxxx.xxxx.x.x.x"#7
	game_map+="x.x....x.........x..x.x.xx.x.x.x"
	game_map+="x..x.x.xxxxxxxxx....x.x.xx.x.x.x"
	game_map+="x....x..............x.x........x"
	game_map+="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	
	map_width = 32
	map_height = 12
	
	
	mFarWall = pygame.image.load("bgrenders/MidFarWall_hq.png")
	lFarWall = pygame.image.load("bgrenders/LefFarWall_hq.png")
	rFarWall = pygame.image.load("bgrenders/RigFarWall_hq.png")
	
	mNearWall = pygame.image.load("bgrenders/MidNearWall_hq.png")
	lNearWall = pygame.image.load("bgrenders/LefNearWall_hq.png")
	rNearWall = pygame.image.load("bgrenders/RigNearWall_hq.png")
	
	lCloseWall = pygame.image.load("bgrenders/LefCloseWall_hq.png")
	rCloseWall = pygame.image.load("bgrenders/RigCloseWall_hq.png")
	
	frame = pygame.image.load("bgrenders/frame_hq.png")
	
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
		
		if (self.getTile(farL[0], farL[1])=='x'):
			outSprites.append(self.lFarWall)
		if (self.getTile(farR[0], farR[1])=='x'):
			outSprites.append(self.rFarWall)
		if (self.getTile(farM[0], farM[1])=='x'):
			outSprites.append(self.mFarWall)
			
		if (self.getTile(nearL[0], nearL[1])=='x'):
			outSprites.append(self.lNearWall)
		if (self.getTile(nearR[0], nearR[1])=='x'):
			outSprites.append(self.rNearWall)
		if (self.getTile(nearM[0], nearM[1])=='x'):
			outSprites.append(self.mNearWall)
		
		if (self.getTile(closeL[0], closeL[1])=='x'):
			outSprites.append(self.lCloseWall)
		if (self.getTile(closeR[0], closeR[1])=='x'):
			outSprites.append(self.rCloseWall)
			
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
		for sprite in sprites:
			screen.blit(sprite, (0,0))
		
		pygame.display.flip()
	
	##handles input
	def handleInput(self, i):
		mod = [0,0]
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
		nextX = self.camPosX+mod[0]
		nextY = self.camPosY+mod[1]
		nextTile = self.getTile(nextX, nextY)
	
		if nextTile=='x':
			collide=True
		if (collide==False):
		self.camPosX = (self.camPosX + mod[0]) 
		self.camPosY = (self.camPosY + mod[1]) 
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
