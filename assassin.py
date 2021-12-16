import pc

class assassin(pc.pc):
	
	def __init__(self, name, sprite, atk, ac, gp, hp, x, y, strength, dexterity, intelligence):
		super(assassin, self).__init__(name, sprite, atk, ac, gp, hp, x, y, strength, dexterity, intelligence) ##SUPERCLASS BABEH
		self.bonus_dmg = 0
		
	def __init__(self, name, strength, dexterity, intelligence):
		super(assassin, self).__init__(name, strength, dexterity, intelligence)
		self.job = "assassin"
		self.atk = 6
		self.ac = 12
		self.hd = 6
		self.max_hp = 6
		self.hp = 6
		self.gp = self.roll(13)
	
	def getBonusDmgMult(self):
		if self.level<3:
			return 1.25
		elif self.level>=3 and self.level<5:
			return 1.50
		elif self.level>=5:
			return 1.75
		
def main(args):
	jackie = assassin("jackie", 10, 15, 10)
	print(jackie.getJob())
	print(jackie.getDmg())
	print(jackie.getLevel())
	print((jackie.getAtk())*jackie.getBonusDmgMult())
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
