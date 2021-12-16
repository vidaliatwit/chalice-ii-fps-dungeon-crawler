import random
import being
class monster(being.being):
	def isMonster(self):
		return True
	def main():
		print("")
		
if __name__ == '__main__':
	import sys
	goblin = monster("goblin", None, 6, 10, 10, 6, 0, 0)
	print(goblin.getName())
	print(goblin.getAtk())
	print(goblin.getAc())
	print(goblin.getGp())
	print(goblin.getHp())
    
