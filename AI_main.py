from functools import partial
import os.path
import random
import sys
import time
from tkinter import *
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import pygame
#Nạp thư viện cho các ứng dụng khác
from pygame.locals import *
# Nạp folder chứa 8puzzleGui
import EightPuzzleGame as EPG

root = Tk()
def play_music_bg():
    pygame.mixer.init()
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Join the script's directory with the music folder
    music_path = os.path.join(script_directory)
    os.chdir(music_path)
    # Load and play the background music
    pygame.mixer.music.load('bg.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

def CreateMainPage():
    root.title('Đồ án: Trí tuệ nhân tạo') 

    # Giao diện âm thanh
    pygame.init()
    
    # Bắt đầu bật âm thanh mặc định
    play_music_bg()

    def pause_music():
        # Stop the background music
        pygame.mixer.music.pause()

    def unpause_music():
        pygame.mixer.music.unpause()

    def toggle_sound():
        # Bật hoặc tắt âm thanh
        if pygame.mixer.music.get_busy():
            pause_music()
        else:
            unpause_music()

    # Đường dẫn đến biểu tượng (icon) mới
    icon_path = os.path.join(os.path.dirname(__file__), "player.ico")

    # Kiểm tra sự tồn tại của tập tin biểu tượng
    if os.path.isfile(icon_path):
        # Thay đổi biểu tượng của cửa sổ
        root.iconbitmap(default=icon_path)
    else:
        print("Không tìm thấy tập tin biểu tượng")

    # Load and scale the background image
    try:
        # Get the absolute path to the image file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "bg.png")
        
        # Load the image file
        original_image = Image.open(image_path)
        
        # Specify the maximum size
        max_size = (600, 600)
        
        # Resize the image to have a maximum size of 800x600
        original_image.thumbnail(max_size)
        
        # Convert the resized image to Tkinter-compatible format
        background_image = ImageTk.PhotoImage(original_image)

        # Create a Label widget and set the image as its background
        background_label = Label(root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    except IOError as e:
        print("Error loading image:", str(e))

    lb_Intro = Label(root, text="Artificial Intelligence Project",
                    font='arial 20', bg="#1A5F7A", fg="#FFFF00", borderwidth='3', relief='sunken', anchor='center')
    lb_Intro.grid(column=0, row=0)
    lb_Intro.place(x=135, y=30)

    lb_Member = Label(root, text="21110298 - Đặng Kim Thành\n21110279 - Lê Minh Quang\n21110742 - Võ Thị Minh Thục\n21119170 - Ngô Nguyên Bảo",
                    font='arial 14', bg="#1A5F7A", fg="#FEA1A1", borderwidth='3', relief='sunken', anchor='center')
    lb_Member.grid(column=0, row=0)
    lb_Member.place(x=180, y=100)

    btn_EDA = Button(root, text="GAME BOO-KOBAN", width=20, font="arial 12", background='#917FB3', fg="white", borderwidth='3', relief='sunken', activebackground='gray', border=5, command=sokoban)
    btn_EDA.place(x=215, y=300)

    btn_EDA = Button(root, text="GAME 8-PUZZLE", width=20, font="arial 12", background='#917FB3', fg="white", borderwidth='3', relief='sunken', activebackground='gray', border=5, command=eightpuzzle)
    btn_EDA.place(x=215, y=360)

    btn_toggle_sound = Button(root, text="Bật/Tắt Âm Thanh", width=20, font="arial 12", background='#917FB3', fg="white", borderwidth='3', relief='sunken', activebackground='gray', border=5, command=toggle_sound)
    btn_toggle_sound.pack()
    btn_toggle_sound.place(x=215, y=420)

    btn_Exit=Button(root,text="ĐÓNG GIAO DIỆN", width=20, font="arial 12", background='#917FB3', fg="white", borderwidth='3', relief='sunken', activebackground='gray', border=5, command=Thoat)
    btn_Exit.place(x=215,y=480)
            
    # Set the window size
    root.geometry('600x600')
    # Disable resizing of the window
    root.resizable(False, False)

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = ((screen_width - root.winfo_reqwidth() - 600) // 2) 
    y = ((screen_height - root.winfo_reqheight() - 600) // 2) 

    # Set the window to be centered
    root.geometry("+{}+{}".format(x, y))
    root.mainloop()

'''GAME 8 - PUZZLE'''
state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
puzzle = EPG.EightPuzzle(tuple(state))
# Số bước di chuyển
moves = 0
board = []

def eightpuzzle():
    winform = Toplevel(root)
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    #
    bgbtn = "#000"
    ctxt = "#f6993f"

    # Lấy kích thước của màn hình
    screen_width = winform.winfo_screenwidth() 
    screen_height = winform.winfo_screenheight()
    winform.geometry("{0}x{1}+0+0".format(screen_width,screen_height))
    # Tạo hình ảnh gradient
    def create_gradient_image(width, height, color1, color2):
        img = Image.new('RGB', (width, height), color1)
        img_data = np.array(img)
        for i in range(height):
            img_data[i, :, 0] = np.linspace(color1[0], color2[0], width)
            img_data[i, :, 1] = np.linspace(color1[1], color2[1], width)
            img_data[i, :, 2] = np.linspace(color1[2], color2[2], width)
        gradient_img = Image.fromarray(np.uint8(img_data))
        return gradient_img

    # Màu gradient
    color_start =  (63,68,214)
    color_end =  (160,230,222)

    ffm = 'Courier New'

    # Tạo hình ảnh gradient
    gradient_image = create_gradient_image(winform.winfo_screenwidth() , winform.winfo_screenheight(), color_start, color_end)
    tk_gradient_image = ImageTk.PhotoImage(gradient_image)

    # Chèn hình ảnh gradient vào cửa sổ
    background_label = Label(winform, image=tk_gradient_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Chọn màu nền cho cửa sổ
    background_color = "#fff"  # Thay đổi mã màu theo ý muốn của bạn

    # Đặt màu nền cho cửa sổ
    winform.configure(bg=background_color)

    winform.title("8 puzzle game Algorithms")

    solution = None

    b = [None] * 9
    size = 200
    distanceBtn = 1

    # Thêm danh sách các thuật toán
    algorithms = ['A*', 'BFS', 'Greedy', 'HillClimbing', 'IDS', 'DFS', 'UCS']  # Thêm các thuật toán mà bạn muốn hỗ trợ

    # Biến để theo dõi thuật toán được chọn
    selected_algorithm = 'A*'  # Thiết lập một giá trị mặc định

    # TODO: refactor into OOP, remove global variables

    # Create a label to display the step count
    step_label = Label(winform, text="Steps: 0", font=(ffm, 15, 'bold'), fg="#E4E6EB", bg="#000")
    # step_label.grid(row=0, column=7, pady=10)
    step_label.place(x=170, y=710)

    # Tạo nút hoặc tùy chọn để chọn thuật toán
    algorithm_label = Label(winform, text="Select Algorithm:", font=(ffm, 15, 'bold'), padx=10, pady=10)
    # algorithm_label.grid(row=2, column=5, pady=10)
    algorithm_label.place(x=295, y=640)

    # Create a variable to store the selected algorithm
    selected_algorithm_var = StringVar(winform)
    selected_algorithm_var.set(selected_algorithm)  # Set the default algorithm

    algorithm_option = OptionMenu(winform, selected_algorithm_var, *algorithms)
    algorithm_option.config(font=(ffm, 15, 'bold'), padx=10, pady=10)
    # algorithm_option.grid(row=2, column=7, pady=10)
    algorithm_option.place(x=540, y=640)
    # Tạo một biến toàn cục để theo dõi thời gian
    elapsed_time_var = StringVar()
    elapsed_time_var.set("Time: 0.00s")

    # Tạo một label để hiển thị thời gian
    time_label = Label(winform, textvariable=elapsed_time_var, font=(ffm, 15, 'bold'), padx=10, pady=10)
    # time_label.grid(row=1, column=7, pady=10)
    time_label.place(x=0, y=700)

    elapsed_time_algorithm_var = StringVar()
    elapsed_time_algorithm_var.set("Time algorithm: 0.00s")
    # Tạo một label để hiển thị thời gian thuật toán
    time_label_algorithm = Label(winform, textvariable=elapsed_time_algorithm_var, font=(ffm, 15, 'bold'), padx=10, pady=10)
    # time_label.grid(row=1, column=7, pady=10)
    time_label_algorithm.place(x=0, y=640)

    def update_selected_algorithm(*args):
        global selected_algorithm
        selected_algorithm = selected_algorithm_var.get()

    # Attach the function to update the selected algorithm when the user makes a selection
    selected_algorithm_var.trace("w", update_selected_algorithm)

    # Gắn hàm xử lý sự kiện chọn thuật toán cho nút tùy chọn
    algorithm_option.bind("<Configure>", lambda event: select_algorithm(selected_algorithm_var.get()))

    def update_step_label():
        step_label.config(text=f"Steps: {moves}")

    # Hàm xử lý sự kiện khi người dùng chọn thuật toán
    def select_algorithm(algorithm):
        global selected_algorithm
        selected_algorithm = algorithm

    #Giao diện nhạc
    # Initialize pygame
    pygame.init()
    # Get the current script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the relative path to the music folder
    music_folder = 'musicEightPuzzle'
    # Join the script's directory with the music folder
    music_path = os.path.join(script_directory, music_folder)
    os.chdir(music_path)
    pygame.mixer.music.load('puzzle.mp3')
    # Set the initial volume (between 0.0 and 1.0)
    initial_volume = 0.12
    pygame.mixer.music.set_volume(initial_volume)
    # Function to update the volume
    def update_volume(value):
        volume = float(value) / 100.0  # Convert scale value to volume (between 0.0 and 1.0)
        pygame.mixer.music.set_volume(volume)
    # Function to play background music
    def play_music():
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    def stop_music():
        pygame.mixer.music.stop()
    # Add the volume scale and label
    volume_label = Label(winform, text="Volume", font=(ffm, 15, 'bold'), bg="#000", fg="#E4E6EB")
    volume_label.place(x=660, y=470)
    # Create a Scale widget for volume control
    volume_scale = Scale(winform, from_=0, to=100, orient='horizontal', label='Volume music', command=update_volume)
    volume_scale.set(initial_volume * 100)  # Set initial volume on the scale
    volume_scale.place(x=660, y=500)  # Adjust the coordinates based on your layout

    #Giao diện kết thúc game
    def close_game():
        """Closes the eightpuzzle game"""
        stop_music()
        play_music_bg()
        winform.destroy()
        

    # Thêm nút để đóng game
    close_btn = Button(winform, text='Đóng Game', font=(ffm, 20, 'bold'), width=12,bg="#fff",
        relief="solid",    
        background="#fff",
        foreground="#135887", 
        activebackground="#5faee4",
        activeforeground="#0e4163",
        highlightbackground="GREEN",
        highlightcolor='BLACK',
        border=0,
        cursor='hand1', command=close_game)
    close_btn.grid(row = 0, column = 5, ipady = 30, padx = 30, pady =30)
    close_btn.place(x=420, y=700)
        
    # Xử lí hình ảnh chèn vào
    image_paths = [
        "empty.png",
        "01.jpg",
        "02.jpg",
        "03.jpg",
        "04.jpg",
        "05.jpg",
        "06.jpg",
        "07.jpg",
        "08.jpg",
        # ... Thêm đường dẫn cho các hình ảnh còn lại
    ]

    # Tạo danh sách để lưu trữ các đối tượng PhotoImage
    tk_images = []
    script_directory = os.path.dirname(os.path.abspath(__file__))
    image_directory = os.path.join(script_directory, 'imageEightPuzzle')

    # Tạo và chèn ảnh vào nút trong vòng lặp
    for i, image_filename in enumerate(image_paths):
        image_path = os.path.join(image_directory, image_filename)
        # Đọc ảnh từ đường dẫn
        image = Image.open(image_path)
        resized_image = image.resize((size, size))  # Chỉnh kích thước ảnh
        tk_image = ImageTk.PhotoImage(resized_image)
        # Chuyển đổi ảnh thành đối tượng PhotoImage
        # Thêm tk_image vào danh sách
        tk_images.append(tk_image)

    def scramble():
        """Scrambles the puzzle starting from the goal state"""

        global state
        global puzzle
        global moves  # Declare moves as a global variable

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        scramble = []
        for _ in range(60):
            scramble.append(random.choice(possible_actions))

        for move in scramble:
            if move in puzzle.actions(state):
                state = list(puzzle.result(state, move))
                puzzle = EPG.EightPuzzle(tuple(state))
                create_buttons()
                moves = 0
                update_step_label() 
                # Đặt lại thời gian sau mỗi bước
                start_time = time.time()

    def solve():
        """Solves the puzzle using the selected algorithm"""
        if selected_algorithm == 'A*':
            # Sử dụng thuật toán A*
            return EPG.astar_search(puzzle).solution()
        elif selected_algorithm == 'BFS':
            # Sử dụng thuật toán BFS
            return EPG.breadth_first_graph_search(puzzle).solution()
        elif selected_algorithm == 'Greedy':
            # Sử dụng thuật toán Greedy
            return EPG.greedy_best_first_graph_search(puzzle).solution()
        elif selected_algorithm == 'HillClimbing':
            # Sử dụng thuật toán Hill Climbing
            return EPG.hill_climbing(puzzle).solution()
        elif selected_algorithm == 'IDS':
            return EPG.iterative_deepening_search(puzzle).solution()
        elif selected_algorithm == 'DFS':
            return EPG.depth_first_graph_search(puzzle).solution()
        elif selected_algorithm == 'UCS':
            return EPG.uniform_cost_search(puzzle).solution()

    def solve_steps():
        """Solves the puzzle step by step"""
        # Bắt đầu đo thời gian
        start_time = time.time()
        global puzzle
        global solution
        global state
        global moves

        solution = solve()
        print(solution)
        elapsed_time_algorithm_var.set(f"Time algorithm: {(time.time() -start_time):.2f}s")
        for move in solution:
            state = puzzle.result(state, move)
            create_buttons()
            moves += 1
            update_step_label()
            winform.update()
            # Lấy thời gian hiện tại
            current_time = time.time()
            # Tính thời gian đã trôi qua từ khi bắt đầu đo thời gian
            elapsed_time = current_time - start_time
            # Cập nhật giá trị thời gian cho label
            elapsed_time_var.set(f"Time: {elapsed_time:.2f}s")
            winform.after(1, time.sleep(1))
        
        # Hiển thị hộp thoại thông báo trên cửa sổ con
        messagebox.showinfo("Hoàn thành", "Xếp hình thành công!", parent = winform)

    def exchange(index):
        """Interchanges the position of the selected tile with the zero tile under certain conditions"""

        global state
        global solution
        global puzzle
        global moves

        zero_ix = list(state).index(0)
        actions = puzzle.actions(state)
        current_action = ''
        i_diff = index // 3 - zero_ix // 3
        j_diff = index % 3 - zero_ix % 3
        if i_diff == 1:
            current_action += 'DOWN'
        elif i_diff == -1:
            current_action += 'UP'

        if j_diff == 1:
            current_action += 'RIGHT'
        elif j_diff == -1:
            current_action += 'LEFT'

        if abs(i_diff) + abs(j_diff) != 1:
            current_action = ''

        if current_action in actions:
            b[zero_ix].grid_forget()
            b[zero_ix] = Button(winform, width=size,height=size,command=partial(exchange, zero_ix),bg=bgbtn,fg=ctxt,image=tk_images[state[index]])
            b[zero_ix].grid(row=zero_ix // 3, column=zero_ix % 3,pady=distanceBtn,padx=distanceBtn)
            b[index].grid_forget()
            b[index] = Button(winform,width=size,height=size,command=partial(exchange, index),bg=bgbtn,fg=ctxt,image=tk_images[0])
            b[index].grid(row=index // 3, column=index % 3, pady=distanceBtn,padx=distanceBtn)
            state[zero_ix], state[index] = state[index], state[zero_ix]
            puzzle = EPG.EightPuzzle(tuple(state))

    def create_buttons():
        """Creates dynamic buttons"""
        # TODO: Find a way to use grid_forget() with a for loop for initialization
        b[0] = Button(winform,width=size,height=size,command=partial(exchange, 0),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[0]]}' if state[0] != 0 else tk_images[0])
        b[1] = Button(winform,width=size,height=size,command=partial(exchange, 1),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[1]]}' if state[1] != 0 else tk_images[0])
        b[2] = Button(winform,width=size,height=size,command=partial(exchange, 2),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[2]]}' if state[2] != 0 else tk_images[0])
        b[3] = Button(winform,width=size,height=size,command=partial(exchange, 3),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[3]]}' if state[3] != 0 else tk_images[0])
        b[4] = Button(winform,width=size,height=size,command=partial(exchange, 4),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[4]]}' if state[4] != 0 else tk_images[0])
        b[5] = Button(winform,width=size,height=size,command=partial(exchange, 5),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[5]]}' if state[5] != 0 else tk_images[0])
        b[6] = Button(winform,width=size,height=size,command=partial(exchange, 6),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[6]]}' if state[6] != 0 else tk_images[0])
        b[7] = Button(winform,width=size,height=size, command=partial(exchange, 7),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[7]]}' if state[7] != 0 else tk_images[0])
        b[8] = Button(winform,width=size,height=size, command=partial(exchange, 8),bg=bgbtn,fg=ctxt,image=f'{tk_images[state[8]]}' if state[8] != 0 else tk_images[0])
        
        b[0].grid(row=0, column=0,pady=distanceBtn,padx=distanceBtn)
        b[1].grid(row=0, column=1,pady=distanceBtn,padx=distanceBtn)
        b[2].grid(row=0, column=2,pady=distanceBtn,padx=distanceBtn)
        b[3].grid(row=1, column=0,pady=distanceBtn,padx=distanceBtn)
        b[4].grid(row=1, column=1,pady=distanceBtn,padx=distanceBtn)
        b[5].grid(row=1, column=2,pady=distanceBtn,padx=distanceBtn)
        b[6].grid(row=2, column=0,pady=distanceBtn,padx=distanceBtn)
        b[7].grid(row=2, column=1,pady=distanceBtn,padx=distanceBtn)
        b[8].grid(row=2, column=2,pady=distanceBtn,padx=distanceBtn)


    def create_static_buttons():
        """Creates scramble and solve buttons"""
        btnbg = "#1877f2"
        btnbg1 = "#36a420"
        scramble_btn = Button(winform, text='Scramble', font=(ffm, 20, 'bold'), width=8, command=partial(init),bg="#fff",relief="solid",    
        background="#fff",
        foreground="#135887", 
        activebackground="#5faee4",
        activeforeground="#0e4163",
        highlightbackground="GREEN",
        highlightcolor='BLACK',
        border=0,
        cursor='hand1')
        scramble_btn.grid(row=0, column=5, ipady=20,padx=30, pady=10)
        solve_btn = Button(winform, text='Solve', font=(ffm, 20, 'bold'), width=8, command=partial(solve_steps),
        borderwidth=2,bg="#fff",relief="solid",    
        background="#fff",
        foreground="#135887", 
        activebackground="#5faee4",
        activeforeground="#0e4163",
        highlightbackground="GREEN",
        highlightcolor='BLACK',
        border=1,
        cursor='hand1',
        )
        solve_btn.grid(row=1, column=5, ipady=20,padx=30, pady=10)


    def init():
        """Calls necessary functions"""
        global state
        global solution
        state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        scramble()
        create_buttons()
        create_static_buttons()

    winform.protocol("WM_DELETE_WINDOW", close_game)
    play_music()
    init()
    winform.mainloop()
    
'''GAME SOKOBAN'''
sources_path = os.path.join(os.path.dirname(__file__), 'SokobanGame', 'Sources')
sys.path.append(sources_path)
def sokoban():
    from SokobanGame.Sources import mainGui
    mainGui.main()
    play_music_bg()

'''THOÁT GIAO DIỆN'''
def Thoat():
    chose = messagebox.askyesno(title="Exit", message="Bạn có chắc muốn thoát")
    if chose == 1:
        root.destroy() 

if __name__ == "__main__":
    CreateMainPage()