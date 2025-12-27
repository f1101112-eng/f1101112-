import tkinter as tk
import random

# 視窗設定
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 20

BASE_SPEED = 150      # 初始速度（毫秒）
MIN_SPEED = 60        # 最快限制

UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("貪食蛇 Snake Game")

        # 分數
        self.score = 0
        self.speed = BASE_SPEED
        self.paused = False

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()

        self.canvas = tk.Canvas(
            root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black"
        )
        self.canvas.pack()

        # 按鈕區
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.pause_btn = tk.Button(
            btn_frame, text="暫停", width=10, command=self.toggle_pause
        )
        self.pause_btn.pack(side="left", padx=5)

        self.restart_btn = tk.Button(
            btn_frame, text="重新開始", width=10, command=self.restart_game
        )
        self.restart_btn.pack(side="left", padx=5)

        # 鍵盤控制
        self.root.bind("<Key>", self.change_direction)
        self.root.bind("<space>", lambda e: self.toggle_pause())

        self.init_game()
        self.game_loop()

    def init_game(self):
        self.direction = RIGHT
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = None
        self.running = True
        self.paused = False
        self.score = 0
        self.speed = BASE_SPEED
        self.update_score()
        self.pause_btn.config(text="暫停")
        self.create_food()
        self.canvas.delete("all")

    def update_score(self):
        self.score_label.config(
            text=f"Score: {self.score}   Speed: {BASE_SPEED - self.speed + 1}"
        )

    def create_food(self):
        while True:
            x = random.randrange(0, WINDOW_WIDTH, CELL_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        if self.paused:
            return

        key = event.keysym
        if key == UP and self.direction != DOWN:
            self.direction = UP
        elif key == DOWN and self.direction != UP:
            self.direction = DOWN
        elif key == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif key == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == UP:
            head_y -= CELL_SIZE
        elif self.direction == DOWN:
            head_y += CELL_SIZE
        elif self.direction == LEFT:
            head_x -= CELL_SIZE
        elif self.direction == RIGHT:
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # 撞牆或撞自己
        if (
            head_x < 0 or head_x >= WINDOW_WIDTH or
            head_y < 0 or head_y >= WINDOW_HEIGHT or
            new_head in self.snake
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.update_score()
            self.create_food()

            # ⭐ 每 50 分加速
            if self.score % 50 == 0 and self.speed > MIN_SPEED:
                self.speed -= 10
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green"
            )

        fx, fy = self.food
        self.canvas.create_oval(
            fx, fy, fx + CELL_SIZE, fy + CELL_SIZE, fill="red"
        )

        if self.paused:
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                fill="yellow",
                font=("Arial", 24),
                text="PAUSED"
            )

    def game_loop(self):
        if self.running:
            if not self.paused:
                self.move_snake()
                self.draw()
            self.root.after(self.speed, self.game_loop)

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        self.pause_btn.config(text="繼續" if self.paused else "暫停")

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            fill="white",
            font=("Arial", 24),
            text="Game Over"
        )

    def restart_game(self):
        self.init_game()
        self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
