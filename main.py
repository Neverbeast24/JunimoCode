import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pygame  # For sound effects

# Initialize sound library
pygame.mixer.init()

# Load sound effects
click_sound = pygame.mixer.Sound(r"Interface\bigSelect.wav")

# Stardew Valley themed colors
BACKGROUND_COLOR = "#7A5230"  # Brownish
TEXT_COLOR = "#F4EBD0"        # Light Tan
BUTTON_COLOR = "#8B7355"      # Wooden Button-like
TERMINAL_COLOR = "#000000"    # Black terminal output
FONT = ("Courier", 14, "bold")  # Retro typewriter style font

# Background image path
background_image_path = "sv.jpg"  # Replace this with the path to your Stardew-themed image

class StardewLexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stardew Valley Themed Lexer")
        
        # Set theme for CustomTkinter
        ctk.set_appearance_mode("light")  # Stardew has a warm feel
        ctk.set_default_color_theme("green")  # Match Junimo greenery

        # Configure window size
        self.root.geometry("800x600")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Set background image
        self.set_background_image()

        self.setup_widgets()

    def set_background_image(self):
        bg_image = Image.open(background_image_path)
        bg_image = bg_image.resize((800, 600), Image.LANCZOS) # Adjust size
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Place background image in a canvas to avoid overlapping with other widgets
        self.canvas = ctk.CTkCanvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=bg_photo)
        self.canvas.image = bg_photo  # Keep a reference to avoid garbage collection

    def setup_widgets(self):
        # Heading Label
        title = ctk.CTkLabel(self.root, text="Junimo Lexical Analyzer", 
                             font=("Courier", 24, "bold"), 
                             text_color=TEXT_COLOR, bg_color=BACKGROUND_COLOR)
        title.place(x=240, y=20)
        
        # Input box for code
        self.code_input = ctk.CTkTextbox(self.root, width=700, height=150, 
                                         font=("Courier", 12), 
                                         fg_color=TEXT_COLOR, 
                                         text_color=BACKGROUND_COLOR)
        self.code_input.place(x=50, y=80)

        # Analyze Button with sound effect
        self.analyze_button = ctk.CTkButton(self.root, text="Analyze Code", 
                                            command=self.analyze_code_with_sound, 
                                            width=150, 
                                            fg_color=BUTTON_COLOR, 
                                            text_color=TEXT_COLOR)
        self.analyze_button.place(x=200, y=350)

        # Clear Button with sound effect
        self.clear_button = ctk.CTkButton(self.root, text="Clear Input", 
                                          command=self.clear_input_with_sound, 
                                          width=150, 
                                          fg_color=BUTTON_COLOR, 
                                          text_color=TEXT_COLOR)
        self.clear_button.place(x=450, y=350)

        # Token Table (Treeview)
        self.token_frame = ctk.CTkFrame(self.root, width=700, height=150, fg_color=BACKGROUND_COLOR)
        self.token_frame.place(x=50, y=400)

        self.token_tree = ttk.Treeview(self.token_frame, columns=("Lexeme", "Token"), show='headings', height=6)
        self.token_tree.heading("Lexeme", text="Lexeme")
        self.token_tree.heading("Token", text="Token")
        self.token_tree.column("Lexeme", width=300)
        self.token_tree.column("Token", width=150)
        self.token_tree.pack(fill="both", expand=True)

        # Terminal-like output for errors/success
        self.terminal_output = ctk.CTkTextbox(self.root, width=700, height=100, 
                                              font=("Courier", 12), 
                                              fg_color=TERMINAL_COLOR, 
                                              text_color=TEXT_COLOR)
        self.terminal_output.place(x=50, y=520)

    def analyze_code_with_sound(self):
        pygame.mixer.Sound.play(click_sound)
        self.analyze_code()

    def clear_input_with_sound(self):
        pygame.mixer.Sound.play(click_sound)
        self.clear_input()

    def analyze_code(self):
        # Clear previous tokens and messages
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete(1.0, "end")

        # Get code from input box
        code = self.code_input.get("1.0", "end").strip()

        # Simulate lexical analysis (replace with real lexer output)
        tokens = [
            ("PLANTING", "Keyword"), ("harvest", "Identifier"), 
            ("=", "Operator"), ("10", "Number"), (";", "Delimiter")
        ]  # Example output

        errors = []  # Simulated, use lexer for real errors

        # Display tokens in Treeview
        for lexeme, token in tokens:
            self.token_tree.insert("", "end", values=(lexeme, token))

        # Terminal output for success or errors
        if not errors:
            self.terminal_output.insert("end", "Lexical analysis completed successfully.\n")
        else:
            for error in errors:
                self.terminal_output.insert("end", f"Error: {error}\n")

    def clear_input(self):
        self.code_input.delete(1.0, "end")
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete(1.0, "end")


if __name__ == "__main__":
    root = ctk.CTk()
    app = StardewLexerGUI(root)
    root.mainloop()
