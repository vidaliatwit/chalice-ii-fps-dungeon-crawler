import spell_test

heal_1 = "Heal"
attack_1 = "Missile"
boost_def_1 = "BoostDef"
reduce_atk_1 = "ReduceAtk"

validSpellNames = []


def getSpell(name):
	if name==heal_1:
		return getHeal(heal_1, "ONE", 6)
	elif name==attack_1:
		return getMissile(attack_1, "ONE", 6)
	elif name==boost_def_1:
		return getBoostStat(boost_def_1, "ONE", 2, "DEF") 
	elif name==reduce_atk_1:
		return getReduceStat(reduce_atk_1, "ONE", 2, "ATK")
	else:
		return None
		
##return spell values		
def getHeal(name, target, value):
	return spell(name, target, "HEAL", False, value)

def getMissile(name, target, value):
	return spell(name, target, "ATTACK", True, value)
	
def getBoostStat(name, target, value, stat):
	return support_spell(name, target, "BOOST", False, value, stat)
def getReduceStat(name, target, value, stat):
	return support_spell(name, target, "REDUCE", True, value, stat)


