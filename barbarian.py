import pc

class barbarian(pc.pc):
	
	def __init__(self, name, sprite, atk, ac, gp, hp, x, y, strength, dexterity, intelligence):
		super(barbarian, self).__init__(name, sprite, atk, ac, gp, hp, x, y, strength, dexterity, intelligence) ##SUPERCLASS BABEH
		self.bonus_dmg = 0
		
	def __init__(self, name, strength, dexterity, intelligence):
		super(barbarian, self).__init__(name, strength, dexterity, intelligence)
		self.job = "barbarian"
		self.atk = 8
		self.ac = 8
		self.hd = 8
		self.max_hp = 8
		self.hp = 8
		self.gp = self.roll(7)
	
	##improve later
	def getAc(self):
		return self.ac + self.level
		
def main(args):
	jackie = barbarian("jackie", 10, 15, 10)
	print(jackie.getJob())
	print(jackie.getDmg())
	print(jackie.getLevel())
	print(jackie.getAc())
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
