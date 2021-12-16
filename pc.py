import being
class pc(being.being):
	level = 1
	strength= 3
	dexterity = 3
	intelligence = 3
	hd = 0 ##hit dice
	job = ""
	
	parrying = False##combat usage
	
	def __init__(self, name, sprite, atk, ac, gp, hp, x, y, strength, dexterity, intelligence):
		self.name=name
		self.sprite=sprite
		self.atk=atk
		self.ac=ac
		self.gp=self.roll(gp)
		self.hp=self.roll(hp)
		self.max_hp=hp
		self.x=x
		self.y=y
		self.strength=strength
		self.dexterity=dexterity
		self.intelligence=intelligence
	
	def __init__(self, name, strength, dexterity, intelligence):
		self.name=name
		self.strength=strength
		self.dexterity=dexterity
		self.intelligence=intelligence
		self.level=1
	
	def getLevel(self):
		return self.level
	def getStr(self):
		return self.strength
	def getDex(self):
		return self.dexterity
	def getInt(self):
		return self.intelligence
	def canCast(self):
		return False
	def canAttack(self):
		return True
	def isArmed(self):
		return True
	def isMonster(self):
		return False
	def getJob(self):
		return self.job
	def isParrying(self):
		return self.parrying
	def setParrying(self, flag):
		self.parrying=True
	
	def getAc(self):
		if (self.isParrying()):
			self.setParrying(False)
			return self.ac+3
		else:
			return self.ac
	
	def rest(self):
		self.hp = self.max_hp
		self.resetTempAtkBonus()
		self.resetTempDefBonus()
	
	##resets any temp bonuses received during combat
	def resetStatus(self):
		self.resetTempAtkBonus()
		self.resetTempDefBonus()

	def rollStr(self):
		return self.roll(20)>self.getStr()
	def rollDex(self):
		return self.roll(20)>self.getDex()
	def rollInt(self):
		return self.roll(20)>self.getInt()

		
