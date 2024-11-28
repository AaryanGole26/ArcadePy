import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class ArcadePyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ArcadePy - Game Launcher")
        self.root.configure(bg='#2C3E50')  # Dark background
        
        # Base directory setup
        self.base_dir = r"C:\Users\aaryu\Downloads\Games"
        
        # Game configurations
        self.games = [
            {
                'name': 'Slither',
                'script': os.path.join(self.base_dir, 'Slither', 'Slither.py'),
                'installer': os.path.join(self.base_dir, 'setup', 'Slither_installer.msi'),
                'image': os.path.join(self.base_dir, 'Slither', 'Slither.png')
            },
            {
                'name': 'Pong',
                'script': os.path.join(self.base_dir, 'Pong', 'Pong.py'),
                'installer': os.path.join(self.base_dir, 'setup', 'Pong_installer.msi'),
                'image': os.path.join(self.base_dir, 'Pong', 'Pong.png')
            },
            {
                'name': 'HoveringUFO',
                'script': os.path.join(self.base_dir, 'HoveringUFO', 'HoveringUFO.py'),
                'installer': os.path.join(self.base_dir, 'setup', 'HoveringUFO_installer.msi'),
                'image': os.path.join(self.base_dir, 'HoveringUFO', 'HoveringUFO.png')
            },
            {
                'name': 'Hangman',
                'script': os.path.join(self.base_dir, 'Hangman', 'Hangman.py'),
                'installer': os.path.join(self.base_dir, 'setup', 'Hangman_installer.msi'),
                'image': os.path.join(self.base_dir, 'Hangman', 'Hangman.png')
            }
        ]
        
        self.create_ui()
    
    def create_ui(self):
        # Main container frame
        main_frame = tk.Frame(self.root, bg='#2C3E50', padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Games frame
        games_frame = tk.Frame(main_frame, bg='#2C3E50')
        games_frame.pack(expand=True, fill=tk.BOTH)
        
        # Configure grid
        games_frame.columnconfigure(0, weight=1)
        games_frame.columnconfigure(1, weight=1)
        
        # Create game buttons with installers
        for i, game in enumerate(self.games):
            # Game button frame
            game_frame = tk.Frame(games_frame, bg='#34495E', bd=5, relief=tk.RAISED)
            game_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            # Load and resize game image
            try:
                original_image = Image.open(game['image'])
                # Resize image while maintaining aspect ratio
                original_image.thumbnail((200, 200))  # Adjust size as needed
                game_photo = ImageTk.PhotoImage(original_image)
                
                # Game launch button with image
                game_button = tk.Button(
                    game_frame, 
                    image=game_photo, 
                    command=lambda g=game: self.launch_game(g),
                    bd=0,
                    highlightthickness=0
                )
                game_button.image = game_photo  # Keep a reference
                game_button.pack(side=tk.TOP, padx=5, pady=5)
                
                # Installer button
                installer_button = tk.Button(
                    game_frame, 
                    text=f'Install {game["name"]}', 
                    command=lambda g=game: self.launch_installer(g),
                    bg='#3498DB',
                    fg='white',
                    font=('Arial', 10, 'bold')
                )
                installer_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
                
            except Exception as e:
                messagebox.showerror("Image Error", 
                                     f"Could not load image for {game['name']}:\n{str(e)}")
        
        # Quit button
        quit_button = tk.Button(
            main_frame, 
            text='Exit ArcadePy', 
            command=self.root.quit, 
            bg='#E74C3C',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=30
        )
        quit_button.pack(side=tk.BOTTOM, pady=20)
    
    def launch_game(self, game):
        try:
            # Verify script exists
            if not os.path.exists(game['script']):
                messagebox.showerror("Error", f"{game['name']} game script not found!")
                return
            
            # Run Python script in a new window
            subprocess.Popen(['python', game['script']], 
                             cwd=os.path.dirname(game['script']),
                             shell=True)
        except Exception as e:
            messagebox.showerror("Launch Error", 
                                 f"Could not launch {game['name']} game:\n{str(e)}")
    
    def launch_installer(self, game):
        try:
            # Verify installer exists
            if not os.path.exists(game['installer']):
                messagebox.showerror("Error", f"{game['name']} installer not found!")
                return
            
            # Launch MSI installer using msiexec
            subprocess.Popen(['msiexec', '/i', game['installer'], '/quiet'], 
                             cwd=os.path.dirname(game['installer']))
        except Exception as e:
            messagebox.showerror("Install Error", 
                                 f"Could not launch {game['name']} installer:\n{str(e)}")

def main():
    root = tk.Tk()
    app = ArcadePyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()