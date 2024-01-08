import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import Algorithm as Algo
import time
import support_function as spf


''' TRAVERSE TESTCASE FILES AND RETURN A SET OF BOARD '''
def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = os.path.join(path_board, file)
            board = get_board(file_path)
            list_boards.append(board)
    return list_boards

''' TRAVERSE CHECKPOINT FILES AND RETURN A SET OF CHECKPOINT '''
def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = os.path.join(path_checkpoint, file)
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point

''' FORMAT THE INPUT TESTCASE TXT FILE '''
def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'

''' FORMAT THE INPUT CHECKPOINT TXT FILE '''
def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result

''' READ A SINGLE TESTCASE TXT FILE '''
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

''' READ A SINGLE CHECKPOINT TXT FILE '''
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

def CreateSokobanGui():
	''' TIME OUT FOR ALL ALGORITHM : 30 MIN ~ 1800 SECONDS '''
	global TIME_OUT
	TIME_OUT = 1800

	''' GET THE TESTCASES AND CHECKPOINTS PATH FOLDERS '''
	global path_board
	global path_checkpoint
	current_folder = os.path.dirname(os.path.abspath(__file__))
	path_board = os.path.join(current_folder, '..', 'Testcases')
	path_checkpoint = os.path.join(current_folder, '..', 'Checkpoints')

	'''
	//========================//
	//      DECLARE AND       //
	//  INITIALIZE MAPS AND   //
	//      CHECK POINTS      //
	//========================//
	'''
	global maps
	global check_points
	maps = get_boards()
	check_points = get_check_points()


	'''
	//========================//
	//         PYGAME         //
	//     INITIALIZATIONS    //
	//                        //
	//========================//
	'''
	global pygame
	global screen
	global clock
	global BACKGROUND
	global WHITE
	pygame.init()
	pygame.font.init()
	screen = pygame.display.set_mode((640, 740))
	pygame.display.set_caption('Sokoban')
	clock = pygame.time.Clock()
	BACKGROUND = (0, 0, 0)
	WHITE = (255, 255, 255)

	'''
	GET SOME ASSETS
	'''
	assets_path = os.getcwd() + "\\..\\Assets"
	os.chdir(assets_path)
	pygame.mixer.music.load(os.getcwd() + '\\music.mp3')
	# Phát âm thanh
	pygame.mixer.music.play(-1)  # -1 để lặp lại âm thanh liên tục
	# Đặt âm lượng (ví dụ: đặt âm lượng là 0.7)
	pygame.mixer.music.set_volume(0.1)

	global player
	global player1
	global wall
	global box
	global point
	global space
	global arrow_left
	global arrow_right
	global init_background
	global loading_background
	global notfound_background
	global found_background
	global found_background2
	player = pygame.image.load(os.getcwd() + '\\player3.png')
	player1 = pygame.image.load(os.getcwd() + '\\player1.png')
	wall = pygame.image.load(os.getcwd() + '\\wall.png')
	box = pygame.image.load(os.getcwd() + '\\box.png')
	point = pygame.image.load(os.getcwd() + '\\point.png')
	space = pygame.image.load(os.getcwd() + '\\space.png')
	arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
	arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
	init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
	loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
	notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
	found_background = pygame.image.load(os.getcwd() + '\\found_background.png')
	found_background2 = pygame.image.load(os.getcwd() + '\\found_background2.png')


'''
RENDER THE MAP FOR GAMEPLAY
'''
def renderMap(board, style=None):
	width = len(board[0])
	height = len(board)
	indent = (640 - width * 32) / 2.0

	if style == 'init' or style == 'run':
		screen.fill((0, 0, 0))
		scaled_found_background = pygame.transform.scale(init_background, (640, 740))
		screen.blit(scaled_found_background, (0, 0))
	elif style == 'found':
		screen.fill((0, 0, 0))
		scaled_found_background = pygame.transform.scale(found_background, (640, 740))
		screen.blit(scaled_found_background, (0, 0))
	elif style == 'play':
		screen.fill((0, 0, 0))
		scaled_found_background = pygame.transform.scale(found_background2, (640, 740))
		screen.blit(scaled_found_background, (0, 0))
	elif style == 'person':
		screen.fill((0, 0, 0))
		scaled_found_background = pygame.transform.scale(found_background2, (640, 740))
		screen.blit(scaled_found_background, (0, 0))

	for i in range(height):
		for j in range(width):
			screen.blit(space, (j * 32 + indent, i * 32 + 240))
			if board[i][j] == '#':
				screen.blit(wall, (j * 32 + indent, i * 32 + 240))
			if board[i][j] == '$':
				screen.blit(box, (j * 32 + indent, i * 32 + 240))
			if board[i][j] == '%':
				screen.blit(point, (j * 32 + indent, i * 32 + 240))
			if board[i][j] == '@':
				screen.blit(player, (j * 32 + indent, i * 32 + 240))
				if style == 'init':
					screen.blit(player1, (j * 32 + indent + 50, i * 32 + 300))
				elif style == 'run':
					screen.blit(player1, (j * 32 + indent - 70, i * 32 + 270))


''' SOKOBAN FUNCTION '''
def sokoban():
	running = True
	global sceneState
	global loading
	global algorithm
	global list_board
	global mapNumber
	global num_states_visited
	global stateLenght
	global personScore
	global timeAlgo
	
	'''
	VARIABLES INITIALIZATIONS
	'''
	#Map level
	mapNumber = 0
	#Algorithm to solve the game
	algorithm = "Breadth First Search"
	#Your scene states, including: 
	#init for choosing your map and algorithm
	#loading for displaying "loading scene"
	#executing for solving problem
	#playing for displaying the game
	sceneState = "init"
	loading = False
	num_states_visited = 0
	#Thêm vào biến để tính thời gian timeout
	timeAlgo = 0
	personScore = 150
	stateLenght = 0
	currentState = 0
	found = True
	isPersonPlay = False
	currentMap = None
	
	while running:
		screen.blit(init_background, (0, 0))
		if sceneState == "init":
			#Choose map and display
			initGame(maps[mapNumber])
			currentMap = None
			
		if sceneState == "executing":
			#Choose map
			list_check_point = check_points[mapNumber]
			#Choose between BFS or Greedy or A*
			if algorithm == "Breadth First Search":
				print("BFS")
				isPersonPlay = False
				list_board = Algo.BFS_Search(maps[mapNumber], list_check_point)
				num_states_visited = Algo.num_states_visited
				timeAlgo = round(Algo.timeRun, 2)

			elif algorithm == "DFS":
				print("DFS")
				isPersonPlay = False
				list_board = Algo.DFS_Search(maps[mapNumber], list_check_point)
				num_states_visited = Algo.num_states_visited
				timeAlgo = round(Algo.timeRun, 2)

			elif algorithm == "Greedy":
				print("Greedy")
				isPersonPlay = False
				list_board = Algo.Greedy_Search(maps[mapNumber], list_check_point)
				num_states_visited = Algo.num_states_visited
				timeAlgo = round(Algo.timeRun, 2)

			elif algorithm == "Iterative Deepening Search":
				print("Iterative Deepening Search")
				isPersonPlay = False
				list_board = Algo.IDS_Search(maps[mapNumber], list_check_point)
				num_states_visited = Algo.num_states_visited
				timeAlgo = round(Algo.timeRun, 2)

			elif algorithm == "UCS":
				print("UCS")
				isPersonPlay = False
				list_board = Algo.UniformCost_Search(maps[mapNumber], list_check_point)
				num_states_visited = Algo.num_states_visited
				timeAlgo = round(Algo.timeRun, 2)

			elif algorithm == "A Star":
				print("A Star")
				isPersonPlay = False
				list_board = Algo.AStar_Search(maps[mapNumber], list_check_point)
				num_states_visited = Algo.num_states_visited
				timeAlgo = round(Algo.timeRun, 2)

			elif algorithm == "Person Play" and isPersonPlay == False:
				# print("Person Play")
				personScore = 150
				start_time = time.time()
				isPersonPlay = True
				list_board = maps[mapNumber]
				currentMap =  maps[mapNumber]
				num_states_visited = 0

			if len(list_board) > 0 and isPersonPlay == False:
				sceneState = "playing"
				stateLenght = len(list_board[0])
				currentState = 0
			else:
				if isPersonPlay == False:
					sceneState = "end"
					found = False
		
		if sceneState == "loading" and isPersonPlay == False:
			loadingGame()
			sceneState = "executing"
		
		if isPersonPlay == True:
			playGame(currentMap)
			cur_pos = spf.find_position_player(currentMap)
			# print("cur_pos = ",cur_pos)
			list_can_move = spf.get_next_pos(currentMap, cur_pos)
			# print("list_can_move = ",list_can_move)
			if spf.is_board_can_not_win(currentMap, list_check_point) or spf.is_all_boxes_stuck(currentMap, list_check_point):
				isPersonPlay = False
				sceneState = 'end'
				found = False
				continue

			if spf.check_win(currentMap, list_check_point):
				isPersonPlay = False
				sceneState = 'end'
				found = True
				stateLenght = len(list_board[0])
				end_time = time.time()
				timeAlgo = round((end_time - start_time), 2)
				continue

			# 275 - 323
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					new_pos = None
					if event.key == pygame.K_e:
						isPersonPlay = False
						sceneState = 'end'
						found = False
						print("H is pressed")
							
					# Xử lý logic khi phím mũi tên lên được nhấn
					if event.key == pygame.K_UP:
						new_pos = (cur_pos[0] - 1,cur_pos[1])
						if new_pos in list_can_move :
							currentMap = Algo.PersonPlay(currentMap, new_pos, list_check_point)
							num_states_visited += 1
							personScore -= 1

					# Xử lý logic khi phím mũi tên xuống được nhấn	
					elif event.key == pygame.K_DOWN:
						new_pos = (cur_pos[0] + 1,cur_pos[1])
						if new_pos in list_can_move :
							currentMap = Algo.PersonPlay(currentMap, new_pos, list_check_point)
							num_states_visited += 1
							personScore -= 1

					# Xử lý logic khi phím mũi tên trái được nhấn
					elif event.key == pygame.K_LEFT:
						new_pos = (cur_pos[0],cur_pos[1] - 1)
						if new_pos in list_can_move :
							currentMap = Algo.PersonPlay(currentMap, new_pos, list_check_point)
							num_states_visited += 1
							personScore -= 1

					# Xử lý logic khi phím mũi tên phải được nhấn
					elif event.key == pygame.K_RIGHT:
						new_pos = (cur_pos[0],cur_pos[1] + 1)
						if new_pos in list_can_move :
							currentMap = Algo.PersonPlay(currentMap, new_pos, list_check_point)
							num_states_visited += 1
							personScore -= 1
						
					elif event.key == pygame.K_r:
						currentMap = maps[mapNumber]
						num_states_visited = 0
						personScore = 150

		# 323 - 334
		if sceneState == "end" and isPersonPlay == False:
			if found and currentMap == None:
				foundGame(list_board[0][stateLenght - 1])
			elif found and currentMap != None:
				foundGamePerson(currentMap)
			else:
				notfoundGame()

		if sceneState == "playing" and isPersonPlay == False:
			clock.tick(5)
			renderMap(list_board[0][currentState], 'run')
			currentState = currentState + 1
			if currentState == stateLenght:
				sceneState = "end"
				found = True

		#Check event when you press key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				#Press arrow key board to change level map
				if event.key == pygame.K_RIGHT and sceneState == "init":
					if mapNumber < len(maps) - 1:
						mapNumber = mapNumber + 1
				if event.key == pygame.K_LEFT and sceneState == "init":
					if mapNumber > 0:
						mapNumber = mapNumber - 1
				#Press ENTER key board to select level map and algorithm
				if event.key == pygame.K_RETURN:
					if sceneState == "init":
						sceneState = "loading"
					if sceneState == "end":
						sceneState = "init"
				#Press SPACE key board to switch algorithm
				if event.key == pygame.K_SPACE and sceneState == "init":
					if algorithm == "Breadth First Search":
						algorithm = "DFS"

					elif algorithm == "DFS":
						algorithm = "Greedy"

					elif algorithm == "Greedy":
						algorithm = "Iterative Deepening Search"

					elif algorithm == "Iterative Deepening Search":
						algorithm = "UCS"

					elif algorithm == "UCS":
						algorithm = "A Star"

					elif algorithm == "A Star":
						algorithm = "Person Play"

					else:
						algorithm = "Breadth First Search"

		pygame.display.flip()
	pygame.quit()

''' DISPLAY MAIN SCENE '''	
#DISPLAY INITIAL SCENE
def initGame(map):
	renderMap(map, 'init')

	titleSize = pygame.font.Font('gameFont.ttf', 60)
	titleText = titleSize.render('Boo-koban', True, WHITE)
	titleRect = titleText.get_rect(center=(320, 50))
	screen.blit(titleText, titleRect)

	desSize = pygame.font.Font('gameFont.ttf', 20)
	desText = desSize.render('Now, select your map!!!', True, WHITE)
	desRect = desText.get_rect(center=(320, 110))
	screen.blit(desText, desRect)

	mapSize = pygame.font.Font('gameFont.ttf', 30)
	mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
	mapRect = mapText.get_rect(center=(320, 160))
	screen.blit(mapText, mapRect)

	screen.blit(arrow_left, (246, 148))
	screen.blit(arrow_right, (370, 148))

	font1Size = pygame.font.Font('gameFont.ttf', 30)
	font1Text = font1Size.render(f"Press ENTER to start", True, WHITE)
	font1Rect = font1Text.get_rect(center=(320, 210))
	screen.blit(font1Text, font1Rect)

	algorithmSize = pygame.font.Font('gameFont.ttf', 30)
	algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
	algorithmRect = algorithmText.get_rect(center=(320, 570))
	screen.blit(algorithmText, algorithmRect)

	font2Size = pygame.font.Font('gameFont.ttf', 20)
	font2Text = font2Size.render(f"(Press SPACE to change)", True, WHITE)
	font2Rect = font2Text.get_rect(center=(320, 610))
	screen.blit(font2Text, font2Rect)


''' LOADING SCENE '''
#DISPLAY LOADING SCENE
def loadingGame():
	scaled_loading_background = pygame.transform.scale(loading_background, (640, 740))
	screen.blit(scaled_loading_background, (0, 0))

	fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = fontLoading_1.render('SHHHHHHH!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 60))
	screen.blit(text_1, text_rect_1)

	fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = fontLoading_2.render('The problem is being solved, stay right there!', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 100))
	screen.blit(text_2, text_rect_2)

	# Adjust the coordinates and scale for player1
	player1_size = (240, 240)  # Adjust the size as needed
	player1_rect = player1.get_rect(center=(240, 900))
	player1_scaled = pygame.transform.scale(player1, player1_size)
	screen.blit(player1_scaled, player1_rect)

def foundGame(map):
	renderMap(map, 'found')

	font_1 = pygame.font.Font('gameFont.ttf', 30)
	text_1 = font_1.render('Yeah! The problem is solved!!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 25)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 150))
	screen.blit(text_2, text_rect_2)

	font_3 = pygame.font.Font('gameFont.ttf', 30)
	text_3 = font_3.render("Stage algorithm: " + str(num_states_visited), True, WHITE)	
	text_rect_3 = text_3.get_rect(center=(320, 560))
	screen.blit(text_3, text_rect_3)

	font_4 = pygame.font.Font('gameFont.ttf', 30)
	text_4 = font_4.render("Num step: " + str(stateLenght), True, WHITE)	
	text_rect_4 = text_4.get_rect(center=(320, 610))
	screen.blit(text_4, text_rect_4)

	font_5 = pygame.font.Font('gameFont.ttf', 30)
	text_5 = font_5.render("Time algorithm: " + str(timeAlgo) + "s", True, WHITE)	
	text_rect_5 = text_5.get_rect(center=(320, 660))
	screen.blit(text_5, text_rect_5)

# 470 - 493
def foundGamePerson(map):
	renderMap(map, 'person')

	font_1 = pygame.font.Font('gameFont.ttf', 30)
	text_1 = font_1.render('Yeah! The problem is solved!!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 25)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 150))
	screen.blit(text_2, text_rect_2)

	font_3 = pygame.font.Font('gameFont.ttf', 30)
	text_3 = font_3.render("Moved step: " + str(num_states_visited), True, WHITE)	
	text_rect_3 = text_3.get_rect(center=(320, 560))
	screen.blit(text_3, text_rect_3)

	font_4 = pygame.font.Font('gameFont.ttf', 30)
	text_4 = font_4.render("Time step: " + str(timeAlgo) + "s", True, WHITE)	
	text_rect_4 = text_4.get_rect(center=(320, 610))
	screen.blit(text_4, text_rect_4)

	font_5 = pygame.font.Font('gameFont.ttf', 25)
	text_5 = font_5.render("Point: " + str(personScore), True, WHITE)	
	text_rect_5 = text_5.get_rect(center=(320, 660))
	screen.blit(text_5, text_rect_5)

# 493 - 520
def playGame(map):
	renderMap(map, 'play')

	font_1 = pygame.font.Font('gameFont.ttf', 30)
	text_1 = font_1.render('Playing Sokoban !!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 25)
	text_2 = font_2.render('Press < ^ v > to move.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 660))
	screen.blit(text_2, text_rect_2)
	
	font_3 = pygame.font.Font('gameFont.ttf', 25)
	text_3 = font_3.render('Press R to restart.', True, WHITE)
	text_rect_3 = text_3.get_rect(center=(320, 550))
	screen.blit(text_3, text_rect_3)

	font_4 = pygame.font.Font('gameFont.ttf', 25)
	text_4 = font_4.render("Good luck !!!", True, WHITE)	
	text_rect_4 = text_4.get_rect(center=(320, 150))
	screen.blit(text_4, text_rect_4)

	font_5 = pygame.font.Font('gameFont.ttf', 25)
	text_5 = font_5.render('Press E to end game', True, WHITE)
	text_rect_5 = text_5.get_rect(center=(320, 600))
	screen.blit(text_5, text_rect_5)

	
def notfoundGame():
	scaled_notfound_background = pygame.transform.scale(notfound_background, (640, 740))
	screen.blit(scaled_notfound_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 45)
	text_1 = font_1.render('Oh no !!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 80))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 35)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)


def main():
	CreateSokobanGui()
	sokoban()

if __name__ == "__main__":
	main()

