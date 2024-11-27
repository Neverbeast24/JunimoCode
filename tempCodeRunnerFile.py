import customtkinter as ctk
from tkinter import ttk
from PIL import Image
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
background_image_path = "stardewbg.jpg"  # Replace this with the path to your Stardew-themed image


class StardewLexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Junimo Code Compiler")

        # Set theme for CustomTkinter
        ctk.set_appearance_mode("light")  # Stardew has a warm feel
        ctk.set_default_color_theme("green")  # Match Junimo greenery

        # Configure window to expand with resizing
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Create main frame with a background image
        self.background_image = ctk.CTkImage(Image.open(background_image_path), size=(1280, 720))  # Adjust size as needed
        self.background_label = ctk.CTkLabel(self.root, image=self.background_image, text="")
        self.background_label.place(relwidth=1, relheight=1)

        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(1, weight=3)  # Adjust weight for dynamic resizing
        self.main_frame.columnconfigure(0, weight=1)

        self.setup_widgets()

    def setup_widgets(self):
        # Heading Label
        title = ctk.CTkLabel(self.main_frame, text="Junimo Lexical Analyzer", 
                             font=("Courier", 24, "bold"), 
                             text_color=TEXT_COLOR)
        title.grid(row=0, column=0, pady=10)

        # Input box for code
        self.code_input = ctk.CTkTextbox(self.main_frame, font=("Courier", 12),
                                         fg_color=TEXT_COLOR, 
                                         text_color=BACKGROUND_COLOR)
        self.code_input.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Analyze and Clear buttons
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=10)

        self.analyze_button = ctk.CTkButton(button_frame, text="Analyze Code", 
                                            command=self.analyze_code_with_sound,
                                            fg_color=BUTTON_COLOR, 
                                            text_color=TEXT_COLOR)
        self.analyze_button.pack(side="left", padx=10)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear Input", 
                                          command=self.clear_input_with_sound,
                                          fg_color=BUTTON_COLOR, 
                                          text_color=TEXT_COLOR)
        self.clear_button.pack(side="left", padx=10)

        # Token Table (Treeview)
        style = ttk.Style()
        style.configure("Treeview", font=("Courier", 14), rowheight=30)  # Adjust font size and row height
        style.configure("Treeview.Heading", font=("Courier", 14, "bold"))  # Adjust heading font

        self.token_tree = ttk.Treeview(self.main_frame, columns=("Lexeme", "Token"), show='headings')
        self.token_tree.heading("Lexeme", text="Lexeme")
        self.token_tree.heading("Token", text="Token")
        self.token_tree.column("Lexeme", width=300, anchor="w")
        self.token_tree.column("Token", width=150, anchor="w")
        self.token_tree.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        # Configure Treeview to resize
        self.main_frame.rowconfigure(3, weight=2)

        # Terminal-like output for errors/success
        self.terminal_output = ctk.CTkTextbox(self.main_frame, font=("Courier", 12), 
                                              fg_color=TERMINAL_COLOR, 
                                              text_color=TEXT_COLOR)
        self.terminal_output.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

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
