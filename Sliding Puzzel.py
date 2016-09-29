import sys
import random
import pygame

IMAGE_FILE="dduck800_600.jpg"
IMAGE_SIZE = (800,600)
TILE_WIDTH = int(800/3)
TILE_HEIGHT = int(600/3)
COLUMNS = 3
ROWS = 3

frontier=[]
explored=[]
index=[]

EMPTY_TILE = (COLUMNS-1,ROWS-1)
BLACK=(0,0,0)

hor_border = pygame.Surface((TILE_WIDTH,1))
hor_border.fill(BLACK)
ver_border = pygame.Surface((1,TILE_HEIGHT))
ver_border.fill(BLACK)

image = pygame.image.load(IMAGE_FILE)
tiles={}
for c in range(COLUMNS):
	for r in range(ROWS):
		tile = image.subsurface(c*TILE_WIDTH,r*TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT)
		tiles[(c,r)] =(tile)
		if (c,r) !=EMPTY_TILE:
			tile.blit(hor_border, (0, 0))
			tile.blit(hor_border, (0, TILE_HEIGHT-1))
			tile.blit(ver_border, (0, 0))
			tile.blit(ver_border, (TILE_WIDTH-1, 0))		
			tile.set_at((1, 1), BLACK)
			tile.set_at((1, TILE_HEIGHT-2), BLACK)
			tile.set_at((TILE_WIDTH-2, 1), BLACK)
			tile.set_at((TILE_WIDTH-2, TILE_HEIGHT-2), BLACK)
tiles[EMPTY_TILE].fill(BLACK)
state = {(col, row): (col, row) 
			for col in range(COLUMNS) for row in range(ROWS)}
GOALSTATE = tiles.copy()

# keep track of which tile is in which position


# keep track of the position of the empty tyle
(emptyc, emptyr) = EMPTY_TILE

# start game and display the completed puzzle
pygame.init()
display = pygame.display.set_mode(IMAGE_SIZE)
pygame.display.set_caption("shift-puzzle")
display.blit (image, (0, 0))
pygame.display.flip()


def shift (c, r) :
	global emptyc, emptyr 
	display.blit(
		tiles[state[(c, r)]],
		(emptyc*TILE_WIDTH, emptyr*TILE_HEIGHT))
	display.blit(
		tiles[EMPTY_TILE],
		(c*TILE_WIDTH, r*TILE_HEIGHT))
	tempE = state[(emptyc,emptyr)]
	state[(emptyc, emptyr)] = state[(c, r)]
	state[(c, r)] = tempE
	(emptyc, emptyr) = (c, r)
	pygame.display.flip()

def newshift (c, r,emptyc,emptyr) :
	emptyc, emptyr 
	display.blit(
		tiles[state[(c, r)]],
		(emptyc*TILE_WIDTH, emptyr*TILE_HEIGHT))
	display.blit(
		tiles[EMPTY_TILE],
		(c*TILE_WIDTH, r*TILE_HEIGHT))
	tempE = state[(emptyc,emptyr)]
	state[(emptyc, emptyr)] = state[(c, r)]
	state[(c, r)] = tempE
	(emptyc, emptyr) = (c, r)
	pygame.display.flip()

def AIshift():
	initBlank = index[0]
	index.remove(initBlank)
	initBlankCol = int(initBlank%3)
	initBlankRow = int(initBlank/3)
	# print("Initial blank "+str(initBlank))
	while index:
		# event = pygame.event.wait()
		# if event.type == pygame.MOUSEBUTTONDOWN:
		nextBlank = index[0]
		index.remove(nextBlank)
		# print("next position blank"+str(nextBlank))
		nextBlankrow = int(nextBlank/3)
		nextBlankcol = int(nextBlank%3)
		pygame.time.delay(100)
		newshift(nextBlankrow,nextBlankcol,initBlankRow,initBlankCol)
		initBlankCol = nextBlankcol
		initBlankRow = nextBlankrow
			#pygame.time.delay(100)


# shuffle the puzzle by making some random shift moves
def shuffle() :
	global emptyc, emptyr
	# keep track of last shuffling direction to avoid "undo" shuffle moves
	last_r = 0 
	#shift(emptyc - 1, emptyr)
	#shift(emptyc - 1, emptyr)
	for i in range(75):
		# slow down shuffling for visual effect
		pygame.time.delay(50)
		while True:
			# pick a random direction and make a shuffling move
			# if that is possible in that direction
			r = random.randint(1, 4)
			if (last_r + r == 5):
				# don't undo the last shuffling move
				continue
			if r == 1 and (emptyc > 0):
				shift(emptyc - 1, emptyr) # shift left
			elif r == 4 and (emptyc < COLUMNS - 1):
				shift(emptyc + 1, emptyr) # shift right
			elif r == 2 and (emptyr > 0):
				shift(emptyc, emptyr - 1) # shift up
			elif r == 3 and (emptyr < ROWS - 1):
				shift(emptyc, emptyr + 1) # shift down
			else:
				# the random shuffle move didn't fit in that direction  
				continue
			last_r=r
			break # a shuffling move was made

def convertToArray():
	global state
	array = []
	for c in range(COLUMNS):
		for r in range(ROWS):
			#print("goalState = "+str(state[c,r][0])+str(state[c,r][1]))

			value = state[(c,r)][0]*3+state[(c,r)][1]+1	
			array.append(value)
	return array




def mHueristics(state):
	counter=0
	for i in range(len(state)):
		value = state[i]
		if value != 0:
			row = int(i/3)
			col = int(i%3)
			expRow = int((value-1)/3)
			expCol = int((value-1)%3)
			diff = abs(row-expRow)+abs(col-expCol)
			#print(diff)
			counter+=diff
	return counter


# def Actions(state):
# 	zeroIndex = state.index(9)
# 	row = int(zeroIndex/3)
# 	col = int(zeroIndex%3)
# 	actions = []
# 	if row <2:
# 		actions.append("D")
# 	if row>0:
# 		actions.append("U")
# 	if col<2:
# 		actions.append("R")
# 	if col>0:
# 		actions.append("L")

# 	return actions

# def Move(state,actions):
# 	ms=[]
# 	while actions:
# 		nstate = state[:]
# 		action = actions.pop()
# 		#print("Actions "+action)
# 		#print("Orignal State "+str(state))
# 		zeroIndex = state.index(9)
# 		row = int(zeroIndex/3)
# 		col = int(zeroIndex%3)
# 		if action=="D":
# 			row+=1
# 		elif action=="U":
# 			row-=1
# 		elif action=="R":
# 			col+=1
# 		elif action=="L":
# 			col-=1
# 		newIndex = row*3+col
# 		#print("Old index "+str(zeroIndex))
# 		#print("New index "+str(newIndex))
# 		temp = nstate[zeroIndex]
# 		nstate[zeroIndex] = nstate[newIndex]
# 		nstate[newIndex] = temp
# 		#print("New state "+str(nstate))	
# 		ms.append(nstate)
		
# 	return ms


# def calculate(ms):
# 	for l in ms:
# 		#print("State "+str(l))
# 		if l not in explored:
# 			frontier.append([mHueristics(l),l])
# 	frontier.sort(key=lambda x:x[0])

def goalState(state):
	return True if mHueristics(state)==0 else False

def determineChild(frontierTuple):
	print("Deteminig Child")
	global frontier
	ms=[]
	currentState = frontierTuple[0][:]
	currentHueristics = frontierTuple[1]
	path = frontierTuple[2][:]
	# print("currentState "+str(currentState))
	# print("currentHueristics "+str(currentHueristics))
	# print("path "+str(path))
	#Actions
	zeroIndex = currentState.index(9)
	row = int(zeroIndex/3)
	col = int(zeroIndex%3)
	actions = []
	if row <2:
		actions.append("D")
	if row>0:
		actions.append("U")
	if col<2:
		actions.append("R")
	if col>0:
		actions.append("L")
	#Actions child
	print("Actions List "+str(actions))
	while actions:
		nrow,ncol = row,col
		# print("Inside Actions Loop")
		npath=path[:]
		# print("npath "+str(npath))
		# print("Inside Actions Loop"+str(path))
		nstate=currentState[:]
		action = actions.pop()
		
		# print("currentState "+str(currentState))
		if action=="D":
			nrow=row+1
		elif action=="U":
			nrow=row-1
		elif action=="R":
			ncol=col+1
		elif action=="L":
			ncol=col-1
		newIndex = nrow*3+ncol
		# print("Old index "+str(zeroIndex))
		# print("New index "+str(newIndex))
		temp = nstate[zeroIndex]
		nstate[zeroIndex] = nstate[newIndex]
		nstate[newIndex] = temp
		# print("nstate "+str(nstate))
		npath.append(newIndex)
		if nstate not in explored:
			nextHueristics = mHueristics(nstate)
			frontier.append((nstate,nextHueristics,npath))
			ms.append((nstate,nextHueristics,npath))

	# for a in ms:
	# 	print("MS "+str(ms))



def Astar(state):
	global index
	frontier.append((state,mHueristics(state),[state.index(9)]))
	while frontier:
		frontier.sort(key=lambda x:x[1])
		s = frontier[0]
		# print("Top of the frontier"+str(s))
		frontier.remove(s)
		if goalState(s[0]):
			# print("Goal state "+str(s))
			index=s[2][:]
			break
		explored.append(s[0])
		determineChild(s)



##########A*##############
at_start = True
while True:
	event = pygame.event.wait()
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
	elif event.type == pygame.MOUSEBUTTONDOWN:
		if at_start:
			shuffle()
			at_start = False
		else:
			Astar(convertToArray())
			AIshift()