import random

class spell: ##general case spell
	##vars for all spells
	name = "def_spell"
	target_type = "NONE" ##how many targets spell can affect [ONE/ALL]
	effect_type = "NONE" ##the spell's effect [HEAL/ATTACK/BOOST/REDUCE]
	hostile = False ##hostile or friendly
	value = 0 ##value of effect
	
	target_type_values = ["ONE", "ALL"]
	effect_type_values = ["HEAL", "ATTACK", "BOOST", "REDUCE"]
	
	def __init__(self, name, target, effect, hostile, value):
		self.name=name
		self.target_type=target
		self.effect_type=effect
		self.hostile=hostile
		self.value=value
	
	def setName(self, name):
		self.name=name
	def setTarget(self, target_type):
		if (self.isValidTargetType(target_type)):
			self.target_type=target_type
	def setEffect(self, effect_type):
		if (self.isValidEffectType(effect_type)):
			self.effect_type=effect_type
	def setHostile(self, flag):
		self.hostile=flag
	def setValue(self, value):
		self.value=value
	
	def getName(self):
		return self.name
	def getTargetType(self):
		return self.target_type
	def getEffectType(self):
		return self.effect_type
	def isHostile(self):
		return self.hostile
	def getValue(self):
		return self.value
	def getValidTargetType(self):
		return self.target_type_values
	def getValidEffectType(self):
		return self.effect_type_values
		
	def isValidTargetType(self, target_type):
		return target_type in self.target_type_values
	def isValidEffectType(self, effect_type):
		return effect_type in self.effect_type_values

class support_spell(spell): ##spell that affects statistics
	stat = "NONE" ##statistic to boost or reduce [STR,DEX,INT,HP,DEF,ATK]
	stat_values = ["STR", "DEX", "INT", "HP", "DEF", "ATK"]
	
	def __init__(self, name, target, effect, hostile, value, stat):
		spell.__init__(self, name, target, effect, hostile, value)
		if (self.isValidStat(stat)):
			self.stat=stat
		else:
			self.stat=None
	
	def setStat(self, stat):
		if (self.isValidStat(stat)):
			self.stat=stat
	def getStat(self):
		return self.stat
	
	def isValidStat(self, stat):
		return stat in self.stat_values
		
