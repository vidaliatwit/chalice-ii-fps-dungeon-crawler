import pc
import spell
import spell_util

class druid(pc.pc):
	spell_list = [] ##list of spells
	spell_points = 0
	
	def __init__(self, name, strength, dexterity, intelligence):
		super(druid, self).__init__(name, strength, dexterity, intelligence)
		self.job="druid"
		self.ac=10
		self.atk=4
		self.hd=4
		self.max_hp=4
		self.hp=4
		self.gp = self.roll(30)
		self.spell_points=self.level
		
		self.generateSpells()
	
	##add spells by level
	def generateSpells(self):
		counter = self.level
		while counter > 0:
			self.spell_list.append(spell_util.getSpellByPCLevel(self.level))
			counter-=1
	def generateSpellTest(self):
		self.spell_list.append(spell_util.getHeal1())
		self.spell_list.append(spell_util.getMissile1())
		self.spell_list.append(spell_util.getBoostDef1())
		self.spell_list.append(spell_util.getReduceAtk1())
	
	def getSpellList(self):
		return self.spell_list
	def addToSpellList(self, newSpell):
		self.spell_list.append(newSpell)
	def getSpellByIndex(self, index):
		return self.spell_list[index]
	def isSpellInList(self, curSpell):
		return curSpell in self.spell_list
		
	def canCast(self):
		return self.spell_points>0
	def isValidSpellIndex(self, index):
		return (index<len(self.spell_list) and index>=0)
	def getNumOfSpells(self):
		return len(self.spell_list)
	def regainSpellPoints(self):
		self.spell_points=self.level
	def reduceSpellPoints(self):
		self.spell_points-=1
def main(args):
	druid1 = druid("Hermetizon", 9, 8, 15)
	print(druid1.getName())
	i = 1
	for spell in druid1.getSpellList():
		print(str(i) + ") " + spell.getName())
		i+=1
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
