import random
class being():
	name = ""
	sprite = None
	##following values are dice dependent eg: 6=1d6 etc...
	atk = 0
	ac = 0
	gp = 0
	hp = 0
	max_hp = 0
	x,y = 0,0
	
	temp_def_bonus = 0
	temp_atk_bonus = 0

	def __init__(self, name, sprite, atk, ac, gp, hp, x, y):
		self.name=name
		self.sprite=sprite
		self.atk=atk
		self.ac=ac
		self.gp=self.roll(gp)
		self.hp=self.roll(hp)
		self.max_hp=hp
		self.x=x
		self.y=y
	
	def getName(self):
		return self.name
	def getAtk(self):
		return self.roll(self.atk)+self.temp_atk_bonus
	##returns attack damage
	def getDmg(self):
		return self.atk
	def getAc(self):
		return self.ac
	def setAc(self, ac):
		self.ac=ac+self.temp_def_bonus
	def getGp(self):
		return self.gp
	def setGp(self, gp):
		self.gp=gp
	def addGp(self, gp):
		self.gp+=gp
		
	def getHp(self):
		return self.hp
	def setHp(self, hp):
		self.hp=hp
	def getMaxHp(self):
		return self.max_hp
	def setMaxHp(self, hp):
		self.max_hp=hp
		
	def getX(self):
		return self.x
	def getY(self):
		return self.y
		
	def getXY(self):
		return self.x, self.y
		
	def getSprite(self):
		return self.sprite
	def isDead(self):
		return self.hp<=0
	def reduceHp(self, dmg):
		self.setHp(self.getHp()-dmg)
	def addHp(self, hp):
		self.setHp(min(self.getHp()+hp, self.getMaxHp()))
	def roll(self, d):
		return random.randint(1, d)	
		
	def getTempDefBonus(self):
		return self.temp_def_bonus
	def getTempAtkBonus(self):
		return self.temp_atk_bonus
	def setTempDefBonus(self, bonus):
		self.temp_def_bonus=bonus
	def setTempAtkBonus(self, bonus):
		self.temp_atk_bonus=bonus
	def resetTempDefBonus(self):
		self.temp_def_bonus = 0
	def resetTempAtkBonus(self):
		self.temp_atk_bonus = 0
	
	
	def isMonster(self):
		return None
	def main(args):
		return 0
