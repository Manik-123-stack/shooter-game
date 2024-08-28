import tkinter as tk
import random

class BubblePopGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bubble Pop Game")
        
        # Set up the canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg='lightblue')
        self.canvas.pack()
        
        # Create the cannon
        self.cannon = self.canvas.create_rectangle(270, 350, 330, 370, fill='black')
        
        # List to keep track of targets
        self.targets = []
        
        # List to keep track of bullets
        self.bullets = []
        
        # Initialize the score
        self.score = 0
        self.high_score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor='nw', text=f'Score: {self.score}', font=('Arial', 14, 'bold'), fill='black')
        self.high_score_text = self.canvas.create_text(10, 30, anchor='nw', text=f'High Score: {self.high_score}', font=('Arial', 14, 'bold'), fill='black')

        # Initialize the timer
        self.time_left = 60
        self.timer_text = self.canvas.create_text(580, 10, anchor='ne', text=f'Time: {self.time_left}', font=('Arial', 14, 'bold'), fill='black')
        
        # Bind key events
        self.root.bind('<a>', self.move_cannon_left)
        self.root.bind('<d>', self.move_cannon_right)
        
        # Start the game
        self.spawn_target()
        self.update_timer()
        self.start_automatic_shooting()  # Start automatic shooting

    def move_cannon_left(self, event):
        self.canvas.move(self.cannon, -20, 0)
        x1, y1, x2, y2 = self.canvas.coords(self.cannon)
        if x1 < 0:
            self.canvas.move(self.cannon, -x1, 0)
    
    def move_cannon_right(self, event):
        self.canvas.move(self.cannon, 20, 0)
        x1, y1, x2, y2 = self.canvas.coords(self.cannon)
        if x2 > 600:
            self.canvas.move(self.cannon, 600 - x2, 0)
    
    def spawn_target(self):
        if self.time_left > 0:
            x = random.randint(50, 550)
            y = random.randint(50, 200)
            target = self.canvas.create_oval(x, y, x + 30, y + 30, fill='red')
            self.targets.append(target)
            self.root.after(3000, self.spawn_target)  # Spawn a new target every 3 seconds
    
    def move_bullets(self):
        to_remove = []
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, -15)  # Increased bullet speed
            pos = self.canvas.coords(bullet)
            if pos[1] < 0:
                to_remove.append(bullet)
            else:
                for target in self.targets:
                    if self.check_collision(bullet, target):
                        self.canvas.delete(target)
                        self.targets.remove(target)
                        self.canvas.delete(bullet)
                        to_remove.append(bullet)
                        self.update_score()
                        break
        
        for bullet in to_remove:
            self.bullets.remove(bullet)
        
        # Schedule the next bullet movement update
        self.root.after(50, self.move_bullets)
    
    def check_collision(self, bullet, target):
        bullet_coords = self.canvas.coords(bullet)
        target_coords = self.canvas.coords(target)
        return (bullet_coords[0] < target_coords[2] and
                bullet_coords[2] > target_coords[0] and
                bullet_coords[1] < target_coords[3] and
                bullet_coords[3] > target_coords[1])
    
    def shoot(self):
        if self.time_left > 0:
            cannon_coords = self.canvas.coords(self.cannon)
            x = (cannon_coords[0] + cannon_coords[2]) / 2
            y = cannon_coords[1]
            bullet = self.canvas.create_rectangle(x - 5, y - 10, x + 5, y - 30, fill='black')
            self.bullets.append(bullet)
    
    def start_automatic_shooting(self):
        if self.time_left > 0:
            self.shoot()  # Create and shoot a bullet
            self.move_bullets()  # Ensure bullets start moving
            self.root.after(500, self.start_automatic_shooting)  # Schedule next shot in 0.5 seconds (increase rate)
    
    def update_score(self):
        self.score += 10  # Increment score by 10 for each target hit
        self.canvas.itemconfig(self.score_text, text=f'Score: {self.score}')
        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.itemconfig(self.high_score_text, text=f'High Score: {self.high_score}')
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.canvas.itemconfig(self.timer_text, text=f'Time: {self.time_left}')
            self.root.after(1000, self.update_timer)  # Update the timer every second
        else:
            self.end_game()
    
    def end_game(self):
        self.canvas.create_text(300, 200, text=f'Game Over\nFinal Score: {self.score}\nHigh Score: {self.high_score}', fill='black', font=('Arial', 24, 'bold'))
        self.root.unbind('<a>')
        self.root.unbind('<d>')

# Create the Tkinter root window
root = tk.Tk()
game = BubblePopGame(root)

# Run the game
root.mainloop()
