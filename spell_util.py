##spell_util
import spell
import random

##return spell values		
def generateHealSpell(name, target, value):
	return spell.spell(name, target, "HEAL", False, value)

def generateMissileSpell(name, target, value):
	return spell.spell(name, target, "MISSILE", True, value)
	
def generateBoostStatSpell(name, target, value, stat):
	return spell.support_spell(name, target, "BOOST", False, value, stat)
	
def generateReduceStatSpell(name, target, value, stat):
	return spell.support_spell(name, target, "REDUCE", True, value, stat)
		
##SPELL GETTERS
def getHeal1():
	return heal_1
def getMissile1():
	return missile_1
def getBoostDef1():
	return boost_def_1
def getReduceAtk1():
	return reduce_atk_1
	
def getLevel1Spells():
	return spell_list_1
	

##return spell by pc level
def getSpellByPCLevel(level):
	if level==1:
		return getL1Spell()

##returns a spell from L1 spells
def getL1Spell():
	return spell_list_1[random.randint(0, 3)]

##get spell by name from spellList
def getSpellByName(name, spellList):
	for mySpell in spellList:
		if name == mySpell.getName():
			return mySpell
			
###SPELL NAME STATIC VARIABLES
heal_1_name = "Cure Light Wounds"
missile_1_name = "Magic Missile"
boost_def_1_name = "Barkskin"
reduce_atk_1_name = "Rust"

###SPELL INITIALIZATIONS
heal_1 = generateHealSpell(heal_1_name, "ONE", 6) ##static spell for level 1 heal
missile_1 = generateMissileSpell(missile_1_name, "ONE", 6)
boost_def_1 = generateBoostStatSpell(boost_def_1_name, "ONE", 2, "DEF")
reduce_atk_1 = generateReduceStatSpell(reduce_atk_1_name, "ONE", 2, "ATK")

spell_list_1 = [heal_1, missile_1, boost_def_1, reduce_atk_1]
	
