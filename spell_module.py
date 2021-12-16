import spell

def main(args):
	spell = spell.getSpell("Heal")
	print(spell.getName())

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
