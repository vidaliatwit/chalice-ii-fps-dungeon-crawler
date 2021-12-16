import pygame
class explore_gfx():
	screen_width=320*4
	screen_height=200*4

	def drawScreen(self, screen, sprites):
		for sprite in sprites:
			screen.blit(sprite, (0,0))
		
		pygame.display.flip()


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
