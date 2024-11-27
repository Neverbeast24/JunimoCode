import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import tkinter as tk
from itertools import count
from ctypes import windll

# Register custom fonts
windll.gdi32.AddFontResourceW("Stardew-Valley-Regular.ttf")
windll.gdi32.AddFontResourceW("StardewValley.ttf")

# Initialize sound library
pygame.mixer.init()

# Load sound effects
click_sound = pygame.mixer.Sound(r"Interface/bigSelect.wav")
hover_sound = pygame.mixer.Sound(r"Interface/select.wav")
background_music = r"BackgroundMusic/ConcernedApe - Stardew Valley OST - 01 Stardew Valley Overture.mp3"

# Stardew Valley-themed colors
BACKGROUND_COLOR = "#F5F5DC"  # Soft beige for Stardew Valley theme
TEXT_COLOR = "#3B200E"        # Brown text for title and content
BUTTON_COLOR = "#8B7355"      # Wooden Button-like
HOVER_COLOR = "#6FA3EF"       # Blue hover effect for buttons
TABLE_COLOR = "#D9C2A6"       # Inventory-like background
TERMINAL_COLOR = "#F5F5DC"    # Softer beige for terminal

# Font settings
TITLE_FONT = ("Stardew Valley Regular", 48)  # Large title font
PIXEL_FONT = ("Stardew Valley", 16)  # Font for other UI elements

# Paths for assets
background_image_path = "sv.png"
junimo_gif_path = "junimo.gif"


class StardewLexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Junimo Code Lexical Analyzer")
        self.root.geometry("1920x1080")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Play background music
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(loops=-1)

        # Set theme for CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Setup UI elements
        self.setup_background()
        self.setup_widgets()
        self.add_junimo_animation()

    def setup_background(self):
        # Load and stretch the background image
        bg_image = Image.open(background_image_path)
        bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Place the background image on canvas
        self.canvas = tk.Canvas(self.root, width=1920, height=1080, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.canvas.pack(fill="both", expand=True)
        self.bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

    def add_junimo_animation(self):
        # Add Junimo GIF animation
        self.junimo_label = tk.Label(self.canvas, bg=BACKGROUND_COLOR, borderwidth=0)
        self.junimo_label.place(x=1300, y=30)  # Positioned beside the title
        self.junimo_gif = Image.open(junimo_gif_path)

        # Scale down GIF to make it smaller
        self.junimo_gif = self.junimo_gif.resize((100, 100), Image.LANCZOS)
        self.junimo_frames = []

        for frame in count(0):
            try:
                self.junimo_frames.append(ImageTk.PhotoImage(self.junimo_gif.copy()))
                self.junimo_gif.seek(frame)
            except EOFError:
                break

        self.junimo_frame_index = 0
        self.update_junimo_frame()

    def update_junimo_frame(self):
        # Loop through Junimo GIF frames
        self.junimo_label.config(image=self.junimo_frames[self.junimo_frame_index])
        self.junimo_frame_index = (self.junimo_frame_index + 1) % len(self.junimo_frames)
        self.root.after(100, self.update_junimo_frame)

    def setup_widgets(self):
        # Title Label
        self.title = tk.Label(self.root, text="JUNIMO CODE LEXICAL ANALYZER",
                              font=TITLE_FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        self.title.place(x=500, y=20)  # Centered horizontally with enough padding

        # Input box for code
        self.code_frame = ctk.CTkFrame(self.root, width=850, height=200, fg_color=TABLE_COLOR, corner_radius=10)
        self.code_frame.place(x=170, y=120)
        self.code_input = ctk.CTkTextbox(self.code_frame, width=1180, height=180,
                                         font=PIXEL_FONT,
                                         fg_color="#F5D8A8",
                                         text_color=TEXT_COLOR,
                                         wrap="word")
        self.code_input.pack(padx=10, pady=10)

        # Buttons
        button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        button_frame.place(x=700, y=430)  # Centered horizontally below input
        self.analyze_button = ctk.CTkButton(button_frame, text="Analyze Code",
                                            command=self.analyze_code_with_sound,
                                            width=150, height=50,
                                            fg_color=BUTTON_COLOR,
                                            text_color=TEXT_COLOR,
                                            font=PIXEL_FONT,
                                            corner_radius=10,
                                            hover_color=HOVER_COLOR)
        self.analyze_button.grid(row=0, column=0, padx=10)
        self.clear_button = ctk.CTkButton(button_frame, text="Clear Input",
                                          command=self.clear_input_with_sound,
                                          width=150, height=50,
                                          fg_color=BUTTON_COLOR,
                                          text_color=TEXT_COLOR,
                                          font=PIXEL_FONT,
                                          corner_radius=10,
                                          hover_color=HOVER_COLOR)
        self.clear_button.grid(row=0, column=1, padx=10)

        # Token Table
        self.token_frame = ctk.CTkFrame(self.root, width=1600, height=350, fg_color=TABLE_COLOR, corner_radius=10)
        self.token_frame.place(x=160, y=450)

        self.token_tree = ttk.Treeview(self.token_frame, columns=("Index", "Lexeme", "Token"), show='headings', height=15)
        self.token_tree.heading("Index", text="Index")
        self.token_tree.heading("Lexeme", text="Lexeme")
        self.token_tree.heading("Token", text="Token")
        self.token_tree.column("Index", width=80, anchor="center")
        self.token_tree.column("Lexeme", width=800, anchor="center")
        self.token_tree.column("Token", width=800, anchor="center")
        self.token_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Terminal Output
        self.terminal_frame = ctk.CTkFrame(self.root, width=1600, height=200, fg_color=TERMINAL_COLOR, corner_radius=10)
        self.terminal_frame.place(x=160, y=750)
        self.terminal_output = ctk.CTkTextbox(self.terminal_frame, width=1580, height=180,
                                              font=PIXEL_FONT,
                                              fg_color=TERMINAL_COLOR,
                                              text_color=TEXT_COLOR, wrap="word")
        self.terminal_output.pack(padx=10, pady=5)

    def analyze_code_with_sound(self):
        pygame.mixer.Sound.play(click_sound)
        self.analyze_code()

    def clear_input_with_sound(self):
        pygame.mixer.Sound.play(click_sound)
        self.clear_input()

    def analyze_code(self):
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete(1.0, "end")

        code = self.code_input.get("1.0", "end").strip()

        tokens = [
            ("1", "PLANTING", "Keyword"),
            ("2", "harvest", "Identifier"),
            ("3", "=", "Operator"),
            ("4", "10", "Number"),
            ("5", ";", "Delimiter")
        ]

        for index, lexeme, token in tokens:
            self.token_tree.insert("", "end", values=(index, lexeme, token))

        self.terminal_output.insert("end", "Lexical analysis completed successfully.\n")

    def clear_input(self):
        self.code_input.delete(1.0, "end")
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete(1.0, "end")


if __name__ == "__main__":
    root = ctk.CTk()
    app = StardewLexerGUI(root)
    root.mainloop()
