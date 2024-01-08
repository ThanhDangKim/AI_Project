import support_function as spf
import time
from queue import PriorityQueue

'''
//========================//
//         SUKOBAN        //
//        ALGORITHM       //
//     IMPLEMENTATION     //
//========================//
'''

timeRun = 0

#PersonPlay
def PersonPlay(board,next_pos ,list_check_point):

    ''' GET NOW STATE TO SEARCH '''
    now_state = spf.state(board, None, list_check_point)
    ''' GET THE PLAYER'S CURRENT POSITION '''
    cur_pos = spf.find_position_player(now_state.board)
    ''' MAKE NEW BOARD '''
    new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
    ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
    if spf.check_win(board, list_check_point):
        print("Found win")
    # new_board
    return new_board



#BFS
def BFS_Search(board, list_check_point):
    start_time = time.time()
    global timeRun

    ''' BFS SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board,list_check_point):
        print("Found win")
        end_time = time.time()
        timeRun = end_time - start_time
        return [board]
    
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point)

    ''' INITIALIZE 2 LISTS USED FOR BFS SEARCH '''
    list_state = [start_state]
    list_visit = [start_state]

    global num_states_visited 
    num_states_visited = 0

    ''' LOOP THROUGH VISITED LIST '''
    while len(list_visit) != 0:
        ''' GET NOW STATE TO SEARCH '''
        now_state = list_visit.pop(0)
        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)

        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:

            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)

            ''' INCREASE STEP'''
            num_states_visited += 1

            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue

            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point)

            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                end_time = time.time()
                
                timeRun = end_time - start_time
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO VISITED LIST AND TRAVERSED LIST '''
            list_state.append(new_state)
            list_visit.append(new_state)

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
            
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []

#DFS
def DFS_Search(board, list_check_point):
    start_time = time.time()
    global timeRun

    if spf.check_win(board, list_check_point):
        print("Found win")
        end_time = time.time()
        timeRun = end_time - start_time
        return [board]

    start_state = spf.state(board, None, list_check_point)

    # INITIALIZE 2 LISTS USED FOR DFS SEARCH
    stack = [start_state]
    visited_set = set()

    global num_states_visited 
    num_states_visited = 0

    while len(stack) != 0:
        # GET NOW STATE TO SEARCH
        now_state = stack.pop()

        # SKIP IF ALREADY VISITED
        if now_state in visited_set:
            continue

        visited_set.add(now_state)

        # GET THE PLAYER'S CURRENT POSITION
        cur_pos = spf.find_position_player(now_state.board)

        # GET LIST POSITION THAT PLAYER CAN MOVE TO
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        # MAKE NEW STATES FROM LIST CAN MOVE
        for next_pos in list_can_move:
            # MAKE NEW BOARD
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)

            # INCREASE STEP
            num_states_visited += 1
            
            # SKIP IF THIS BOARD HAS BEEN VISITED
            if spf.is_board_exist(new_board, visited_set):
                continue

            # SKIP IF ONE OR MORE BOXES ARE STUCK IN THE CORNER
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            # SKIP IF ALL BOXES ARE STUCK
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            # MAKE NEW STATE
            new_state = spf.state(new_board, now_state, list_check_point)

            # CHECK WHETHER THE NEW STATE IS GOAL OR NOT
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                end_time = time.time()
                timeRun = end_time - start_time
                return (new_state.get_line(), len(visited_set))

            # APPEND NEW STATE TO STACK
            stack.append(new_state)

            # COMPUTE THE TIMEOUT
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []

    # SOLUTION NOT FOUND
    print("Not Found")
    return []

# A Star
def AStar_Search(board, list_check_point):
    start_time = time.time()
    global timeRun
    ''' A* SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board,list_check_point):
        print("Found win")
        end_time = time.time()
        timeRun = end_time - start_time
        return [board]
    
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point, 'A*')
    list_state = [start_state]
    
    ''' INITIALIZE PRIORITY QUEUE '''
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)

    global num_states_visited 
    num_states_visited = 0

    ''' LOOP THROUGH PRIORITY QUEUE '''
    while not heuristic_queue.empty():
        '''GET NOW STATE TO SEARCH'''
        now_state = heuristic_queue.get()

        ''' GET THE PLAYER'S CURRENT POSITION'''
        cur_pos = spf.find_position_player(now_state.board)
        
        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:

            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)

            ''' INCREASE STEP'''
            num_states_visited += 1

            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue

            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point, 'A*')

            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                end_time = time.time()
                timeRun = end_time - start_time
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO PRIORITY QUEUE AND TRAVERSED LIST '''
            list_state.append(new_state)

            ''' USE REAL HEURISTIC FOR PRIORITY QUEUE '''
            heuristic_queue.put(new_state)

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
            
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []


def Greedy_Search(board, list_check_point):
    start_time = time.time()
    global timeRun
    ''' GREEDY SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board, list_check_point):
        print("Found win")
        end_time = time.time()
        timeRun = end_time - start_time
        return [board]
    
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point, 'Greedy')
    list_state = [start_state]
    
    ''' INITIALIZE PRIORITY QUEUE '''
    greedy_queue = PriorityQueue()
    greedy_queue.put(start_state)
    
    global num_states_visited 
    num_states_visited = 0

    ''' LOOP THROUGH PRIORITY QUEUE '''
    while not greedy_queue.empty():
        ''' GET NOW STATE TO SEARCH '''
        now_state = greedy_queue.get()
        
        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)
        
        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            
            ''' INCREASE STEP'''
            num_states_visited += 1

            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue
            
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point, 'Greedy')

            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                end_time = time.time()
                timeRun = end_time - start_time
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO PRIORITY QUEUE AND TRAVERSED LIST '''
            list_state.append(new_state)
            
            ''' USE ONLY HEURISTIC FOR PRIORITY QUEUE '''
            greedy_queue.put(new_state, new_state.compute_heuristic())

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []

def UniformCost_Search(board, list_check_point):
    start_time = time.time()
    global timeRun

    ''' UNIFORM COST SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board, list_check_point):
        print("Found win")
        end_time = time.time()
        timeRun = end_time - start_time
        return [board]
    
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point, 'UCS')
    list_state = [start_state]
    
    ''' INITIALIZE PRIORITY QUEUE '''
    ucs_queue = PriorityQueue()
    ucs_queue.put(start_state)

    global num_states_visited 
    num_states_visited = 0
    
    ''' LOOP THROUGH PRIORITY QUEUE '''
    while not ucs_queue.empty():
        ''' GET NOW STATE TO SEARCH '''
        now_state = ucs_queue.get()
        
        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)
        
        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            
            ''' INCREASE STEP'''
            num_states_visited += 1

            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue
            
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point, 'UCS')

            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                end_time = time.time()
                timeRun = end_time - start_time
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO PRIORITY QUEUE AND TRAVERSED LIST '''
            list_state.append(new_state)
            
            ''' USE ONLY HEURISTIC FOR PRIORITY QUEUE '''
            ucs_queue.put(new_state, new_state.compute_heuristic())

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []


def IDS_Search(board, list_check_point):
    start_time = time.time()
    global timeRun

    if spf.check_win(board, list_check_point):
        print("Found win")
        end_time = time.time()
        timeRun = end_time - start_time
        return [board]

    start_state = spf.state(board, None, list_check_point)

    max_depth = 1

    while True:
        result = depth_limited_DFS(start_state, list_check_point, max_depth, start_time)

        if result is not None:
            return result

        max_depth += 1

    # Solution not found
    print("Not Found")
    return []

def depth_limited_DFS(now_state, list_check_point, max_depth, start_time):
    global timeRun
    stack = [(now_state, 0)]
    visited_set = set()

    global num_states_visited 
    num_states_visited = 0
    
    while len(stack) != 0:
        current_state, depth = stack.pop()

        if current_state in visited_set or depth > max_depth:
            continue

        visited_set.add(current_state)

        cur_pos = spf.find_position_player(current_state.board)
        list_can_move = spf.get_next_pos(current_state.board, cur_pos)

        for next_pos in list_can_move:
            new_board = spf.move(current_state.board, next_pos, cur_pos, list_check_point)

            num_states_visited += 1
            
            if spf.is_board_exist(new_board, visited_set):
                continue

            if spf.is_board_can_not_win(new_board, list_check_point):
                continue

            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, current_state, list_check_point)

            if spf.check_win(new_board, list_check_point):
                print("Found win")
                end_time = time.time()
                timeRun = end_time - start_time
                return (new_state.get_line(), len(visited_set))

            stack.append((new_state, depth + 1))

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return None

    visited_set.clear()  # Clear the visited_set at the end of the depth-limited DFS
    return None