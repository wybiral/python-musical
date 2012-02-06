import pygame, urllib
from musical.audio import source, playback, effect

print 'Loading sound from internet...'

pygame.mixer.init()
rate, format, channels = pygame.mixer.get_init()
web = urllib.urlopen('http://www.moviesounds.com/matrix/dodge.wav')
sound = pygame.mixer.Sound(web)
data = source.pygamesound(sound)
pygame.mixer.quit()

print 'Applying flanger...'

data = effect.flanger(data, 1.0, dry=0.25, wet=0.75) * 0.75

print "Playing audio..."

playback.play(data, rate=rate)

print "Done!"
