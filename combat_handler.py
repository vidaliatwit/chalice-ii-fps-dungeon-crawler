import monster
import pc
import druid
import being
import random
import math
import pygame
class combat_handler:
	turn = None
	party = []
	monsters = []
	monster_size = 0
	gold_reward = 0
	state = None
	action_queue = []
	outcome_queue = []
	
	combat_running = False
	game_over = False
	
	outcome_counter = 0
	
	##player data
	run_flag = False ##whether a player succesfully ran away
	temp_action = None
	temp_target = None
	temp_spell = None ##might not get used....
	
	def __init__(self, party, monsters):
		self.turn = 0
		self.state = 1
		self.gold_reward = 0
		self.outcome_counter = 0
		self.action_queue.clear()
		self.outcome_queue.clear()
		self.combat_running = True
		self.party = party
		self.monsters = monsters
		self.monster_size = len(monsters)
		self.temp_action = None
		self.temp_target = None
		self.temp_spell = None
		self.run_flag = False
		
	def checkState(self):
		if self.state==1:
			if (self.isActionSelected()):				
				if self.isTargetAction(self.temp_action):
					if self.temp_action=='c':
						self.state=7
					else:
						self.state=2
				else: ##IF NOT A TARGET ACTION
					action = [self.getActivePlayer(), self.temp_action, -1] ##assign action to not have target
					self.action_queue.append(action)
					if self.isRoundOver(): ##if player round over
						self.handleActionQueue()
						self.state=3
					else:
						self.nextTurn()
			return True
		elif self.state==2:
			if (self.isTargetSelected()):
				action = [self.getActivePlayer(), self.temp_action, self.temp_target]
				self.action_queue.append(action)
				if (self.isRoundOver()):
					self.handleActionQueue()
					self.state=3
				else:
					self.nextTurn()
			return True
		elif self.state==3:
			if (self.hasOutcomeDisplayEnded()):
				if self.hasRunAway():
					self.state=4
				elif self.areBothGroupsAlive():
					self.state=1
					self.resetFlags()
				else:
					self.state=4
			return True
		elif self.state==4:
			print("STATE 4")
			
		elif self.state==5:
			self.endCombat()
			return False
		elif self.state==7: ##magic
			if (self.isSpellSelected()):
				print("Spell is selected!")
				self.state=2
	
	def render(self):
		print(self.getPartyStr())
		print(self.getMonsterStr())
		if self.state==1:
			print(self.getOptionString())
		elif self.state==2:
			print(self.getTargetGroupString())
		elif self.state==3:
			##print("Outcome counter!!!" + str(self.outcome_counter))
			print(self.outcome_queue[self.outcome_counter])
		elif self.state==4 and self.combat_running:
			print("end of the road")
		
	def handleInput(self, i):
		if (self.state==1): ##Choosing actions
			pc = self.getActivePlayer()
			if i in self.getValidActions(pc):
				self.setTempAction(i)
				return True
		elif (self.state==2 and self.isActionSelected()): ##Choosing target
			pc = self.getActivePlayer()
			if (self.isValidTarget(i)): ##maybe check for errors?
				self.temp_target = int(i)-1
				return True
		elif (self.state==3): ##Viewing outcome
			if (i=="ENTER"):
				self.outcome_counter+=1
				return True
		elif (self.state==4): ##Handling end of combat
			if (i=="ENTER"):
				self.state=5 ##Ending combat
				return True
		elif (self.state==7): ##Magic
			pc = self.getActivePlayer()
			if (i.isnumeric()):
				print("isnumeric!")
				i = int(i)-1
				if (pc.isValidSpellIndex(i)):
					print("ISVALIDSPELLINDEX!")
					self.temp_spell = pc.getSpellByIndex(i)
					return True
		else:
			return False
				
	##Helpers
	def endCombat(self):
		print("STATE 5")
		self.resetFlags()
		print("COMBAT OVER")
		if (len(self.party)<=0):
			print("Party has died!")
			self.game_over=True
		else:
			self.party[0].addGp(self.gold_reward)
			for pc in self.party:
				pc.resetStatus()
		
		self.combat_running=False
			

	def nextTurn(self):
		self.state=1
		self.temp_action=None
		self.temp_target=None
		self.turn = (self.turn + 1) % len(self.party)
	def pushMonsterActions(self):
		for mon in self.monsters:
			target = self.getTargetForMonsterAttack() ## assign target
			self.action_queue.append([mon, 'f', target])
			
	def sortQueue(self):
		new_queue = []
		after_queue = []
		before_queue = []
		##print(self.action_queue) ##theres three
		for action in self.action_queue:
			if action[0].isMonster():
				new_queue.append(action)
			elif (self.dexCheck(action[0])):
				before_queue.append(action)
			else:
				after_queue.append(action)
		new_queue = before_queue + new_queue + after_queue
		return new_queue
		
	def handleActionQueue(self):
		self.pushMonsterActions()
		sortedQueue = self.sortQueue()
		##print(sortedQueue)
		while (len(sortedQueue)>0):
			action = sortedQueue.pop(0)
			if action[0].isMonster():
				outStr = self.monsterAction(action)
			else:
				outStr = self.playerAction(action)
			self.outcome_queue.append(outStr)	
		self.janitor() ##CLEAN UP THE MESS	
		##print(self.outcome_queue)	
				
	def dexCheck(self, player):
		return player.roll(20)<player.getDex()	
		
	def strCheck(self, player):
		return player.roll(20)<player.getStr()
	
	def playerAction(self, action):
		if action[1]=='f':
			return self.playerAttack(action[0], action[2])
		elif action[1]=='r':
			return self.playerRun(action[0])
		elif action[1]=='p':
			return self.playerParry(action[0])		
		elif action[1]=='c':
			return self.playerCast(action[0], action[2])
			##return self.temp_spell.getName() + " " + str(action[2])
			
	def playerAttack(self, player, index):
		dmg = player.roll(player.getAtk())
		monster = self.monsters[int(index)]
		if self.strCheck(player):
			if (player.getJob()=="assassin" and player.rollDex()):
				dmg = int(math.ceil(dmg*player.getBonusDmgMult()))
			monster.reduceHp(dmg)
			return player.getName() + " hit " + monster.getName() + " for " + str(dmg) + " points of damage!"
		else:
			return player.getName() + " missed!"
	
	def playerRun(self, player):
		if self.dexCheck(player) and self.dexCheck(player):
			self.run_flag = True
			return player.getName() + " ran away!"
		else:
			return player.getName() + " couldn't run away!"
	
	def playerParry(self, player):
		player.setParrying(True)
		return player.getName() + " is parrying blows!"
	
	def playerCast(self, player, index):
		target = self.getTargetGroup('c')[index]
		player.reduceSpellPoints()
		return (player.getName() + " cast " + self.handleSpellEffect(target, player))
	
	def handleSpellEffect(self, target, player):
		curSpell = self.temp_spell
		spell_type = curSpell.getEffectType()
		print(spell_type)
		target_type = curSpell.getTargetType()
		value = curSpell.getValue()
		outStr = curSpell.getName()
		if (spell_type == "HEAL"):
			print("heal")
			hp_plus = player.roll(value)
			target.addHp(hp_plus)
		elif (spell_type == "MISSILE"):
			print("missile")
			dmg = player.roll(value)
			target.reduceHp(dmg)
		elif (spell_type == "BOOST"):
			if (curSpell.getStat()=="DEF"):
				target.setTempDefBonus(value)
			elif (curSpell.getStat()=="ATK"):
				target.setTempAtkBonus(value)
		outStr+= " on " + target.getName()
		return outStr
		
	def monsterAction(self, action):
		if action[1]=='f':
			return self.monsterAttack(action[0], action[2])
		else:
			return "NO!" ##they can only ever attack
		
	def monsterAttack(self, monster, index):
		dmg = monster.roll(monster.getAtk())
		pc = self.party[int(index)]
		if self.dexCheck(pc):
			return monster.getName() + " missed!"
		else:
			pc.reduceHp(dmg)
			return monster.getName() + " hit " + pc.getName() + " for " + str(dmg) + " points of damage!"
			
	def getTargetForMonsterAttack(self):
		return random.randint(0, min(len(self.party)-1, 3))
	
	##Cleans up dead people
	def janitor(self):
		monsterSack = []
		pcSack = []
		for pc in self.party:
			if (pc.isDead()):
				self.outcome_queue.append(pc.getName() + " died!")
				pcSack.append(pc)
		for monster in self.monsters:
			if (monster.isDead()):
				self.outcome_queue.append(monster.getName() + " died!")
				self.gold_reward+=monster.getGp()
				monsterSack.append(monster)
		if len(pcSack)>0:
			for deadPc in pcSack:
				self.party.remove(deadPc)
		if len(monsterSack)>0:
			for deadMon in monsterSack:
				self.monsters.remove(deadMon)
	
	def resetFlags(self):
		self.action_queue.clear()
		self.outcome_queue.clear()
		self.outcome_counter = 0
		self.turn = 0
		self.temp_action = None
		self.temp_target = None
		self.temp_spell = None
	##GETTERS
	
	##gets current state
	def getState(self):
		return self.state
	
	##returns player at index[turn] or the length of the party-1 if the former is invalid
	def getActivePlayer(self):
		return self.party[min(len(self.party)-1, self.turn)]
		
	def getValidActions(self, pc):
		valid_actions = ['r', 'p']
		if self.canAttack(pc):
			valid_actions.append('f')
		if self.canCast(pc):
			valid_actions.append('c')
		return valid_actions
	
	def getTargetGroup(self, action):
		if self.isHostileAction(action):
			return self.monsters
		else:
			return self.party
			
	##Flags
	
	##checks if action is hostile
	def isHostileAction(self, action):
		return(action=='f' or (action=='c' and self.temp_spell.isHostile()))

	##checks if action requires target
	def isTargetAction(self, action):
		return(action=='f' or action=='c')
	
	##checks if tempAction is null
	def isActionSelected(self):
		return self.temp_action!=None
	def isTargetSelected(self):
		return self.temp_target!=None
	def isSpellSelected(self):
		return self.temp_spell!=None
	
	##returns if pc can attack
	def canAttack(self, pc):
		return self.turn<4
	
	##returns if pc can cast
	def canCast(self, pc):
		return pc.canCast()
		
	##returns whether combat is running
	def isCombatRunning(self):
		return self.combat_running
	
	def setCombatRunning(self, flag):
		self.combat_running=flag
		
	##returns whether player has succesfully ran away
	def hasRunAway(self):
		return self.run_flag
		
	##returns whether the combat round is over
	def isRoundOver(self):
		return self.turn==len(self.party)-1
		
	##returns whether all set of outcomes have been displayed to player
	def hasOutcomeDisplayEnded(self):
		return self.outcome_counter==len(self.outcome_queue)
	
	##returns whether both monster and player groups are alive	
	def areBothGroupsAlive(self):
		return (len(self.monsters) > 0 and len(self.party) > 0)
	
	def isValidTarget(self, i):
		return (i.isdigit() and int(i) <= len(self.getTargetGroup(self.temp_action)))
		
	def isGameOver(self):
		return self.game_over
		
	##SETTERS
	def setTempAction(self, action):
		self.temp_action = action	
		
	##String getters
	
	##gets String of player party
	def getPartyStr(self):
		outStr=""
		i = 1
		for pc in self.party:
			outStr+= str(i) + ") " + pc.getName() + ": " + str(pc.getHp())
			if i<len(self.party):
				outStr+="\n" 
			i+=1
		return outStr
	
	##for external render calls
	def getPartyStrList(self):
		outList = []
		i = 1
		for pc in self.party:
			outList.append(str(i) + ") " + pc.getName() + ": " + str(pc.getHp()))
			i+=1
		return outList
		
	##gets String of monster group
	def getMonsterStr(self):
		outStr=""
		i = 1
		for mon in self.monsters:
			outStr+= str(i) + ") " + mon.getName() + ": " + str(mon.getHp())
			if i<len(self.monsters):
				outStr+="\n" 
			i+=1
		return outStr
		
	def getMonsterStrList(self):
		outList = []
		i = 1
		for mon in self.monsters:
			outList.append(str(i) + ") " + mon.getName() + ": " + str(mon.getHp()))
			i+=1
		return outList
	##gets Option strings
	def getOptionString(self):
		if len(self.party)>0:
			player = self.getActivePlayer()
			valid_actions = self.getValidActions(player)
			option_string = player.getName() + " will...\n"
			for action in valid_actions:
				if action=='f':
					option_string+="F)ight\n"
				if action=='c':
					option_string+="C)ast\n"
			option_string+= "P)arry\nR)un"
			return option_string
		else:
			return ["Accept your lot in life and die..."]
		
	##gets Option strings as list
	def getOptionStringList(self):
		if len(self.party)>0:
			player = self.getActivePlayer()
			valid_actions = self.getValidActions(player)
			out_list = []
			if self.state==3 or self.state==4: ##CHECK'd
				return ["Press Enter to continue..."]
			##if self.state==7:
				##i = 1
				##while i < player.getNumOfSpells():
					##out_list.append(str(i) + ")      ")
					##i+=1
				##return out_list
			out_list.append(player.getName() + " will...")  
			option_string = ""
			for action in valid_actions:
				if action=='f':
					option_string+="F)ight     " ##adequate space
				if action=='c':
					option_string+="C)ast      "
			option_string+= "P)arry     R)un     "
			out_list.append(option_string)
			return out_list
		else:
			return ["Accept your lot in life and die..."]
		
	##gets Target group string
	def getTargetGroupString(self):
		i = 1
		outStr = ""
		group = self.getTargetGroup(self.temp_action)
		for ch in group:
			outStr+=str(i) + ") " + ch.getName()
			if (i<len(group)):
				outStr+="\n"
			i+=1
		return outStr
	
	def getTargetGroupStringList(self):
		i = 1
		outStrList = []
		group = self.getTargetGroup(self.temp_action)
		for ch in group:
			outStrList.append(str(i) + ") " + ch.getName())
			i+=1
		return outStrList
	
	def getVictoryString(self):
		outStrList = []
		if self.hasRunAway():
			outStrList.append("You ran away...")
		else:
			if self.monster_size>1:
				outStrList.append("You defeated the creatures!")
			else:
				outStrList.append("You defeated the creature!")
			outStrList.append("You find " + str(self.gold_reward) + "gp among the gristle...") 
		return outStrList
	
	##returns spell list in string form for current player
	def getSpellList(self, pc):
		outStrList = []
		i = 1
		for curSpell in pc.getSpellList():
			outStrList.append(str(i) + ") " + curSpell.getName())
			i+=1
		return outStrList
		
	##get text list for contextMenu
	def getContextStringList(self):
		if self.state==2:
			return self.getTargetGroupStringList()
		elif self.state==3:
			print(self.outcome_queue)
			return [self.outcome_queue[self.outcome_counter]]
		elif self.state==4:
			if len(self.party)>0:
				return self.getVictoryString()
			else:
				return ["You have died!"]
		elif self.state==7:
			if self.getActivePlayer().canCast(): ##IF DRUID
				return self.getSpellList(self.getActivePlayer())
			else:
				return ["You can't cast spells yet you got to state 7... Why???"]
		else:
			return ["Somehow you managed to die and you can see this secret screen..."]
