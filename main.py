import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
import tkinter as tk
from itertools import count
from PIL import Image, ImageTk  # Import Pillow
from pathlib import Path
from tkinter import filedialog
import parser_syntax
import lexer
import sys
import semantic
from nodes import convert_text_file_to_python_and_execute
from pathlib import Path
from ctypes import windll

# Register custom fonts
windll.gdi32.AddFontResourceW("Stardew-Valley-Regular.ttf")
windll.gdi32.AddFontResourceW("StardewValley.ttf")

# Initialize sound library
mixer.init()

# Load sound effects
click_sound = mixer.Sound("Interface/bigSelect.wav")
hover_sound = mixer.Sound("Interface/select.wav")
delete_sound = mixer.Sound("Interface/bigDeSelect.wav")
background_music = r"BackgroundMusic/ConcernedApe - Stardew Valley OST - 01 Stardew Valley Overture.mp3"

# Stardew Valley-themed colors
BACKGROUND_COLOR = "#F5F5DC"  # Soft beige for Stardew Valley theme
TEXT_COLOR = "#3B200E"  # Brown text for title and content
BUTTON_COLOR = "#8B7355"  # Wooden Button-like
HOVER_COLOR = "#6FA3EF"  # Blue hover effect for buttons
TABLE_COLOR = "#D9C2A6"  # Inventory-like background
TERMINAL_COLOR = "#F5F5DC"  # Softer beige for terminal

# Font settings
TITLE_FONT = ("Stardew Valley Regular", 48)  # Large title font
PIXEL_FONT = ("Verdana", 12, "bold" )  # Font for other UI elements

# Paths for assets
background_image_path = "background.jpg"

#Cursor
junimo_cursor = "Stardew_Cursor.xpm" #Not Yet Working ; Maganda sana na-additional kaechosan.


class StardewLexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Junimo Code Lexical Analyzer")
        self.root.geometry("1920x1200")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.code = None

        # Play background music
        mixer.music.load(background_music)
        mixer.music.play(loops=-1)

        # Set theme for CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Setup UI elements
        self.setup_background()
        self.setup_widgets()


    def setup_background(self):
        # Load and stretch the background image
        bg_image = Image.open(background_image_path)
        bg_image = bg_image.resize((1920, 1200), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Place the background image on canvas
        self.canvas = tk.Canvas(self.root, width=1920, height=1200, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.canvas.pack(fill="both", expand=True)
        self.bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        
    def update_line_numbers(self):
        """Synchronize line numbers with text lines in the code_input box."""
        # Enable editing for the line number widget
        self.line_numbers.configure(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)

        # Get the number of lines in the code_input
        code = self.code_input.get("1.0", tk.END)
        self.code = code
        lines = code.split("\n")  # Count lines

        # Add line numbers for each line
        for i in range(1, len(lines) + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

        # Ensure the line numbers are aligned with the text
        self.line_numbers.configure(state=tk.DISABLED)

        # Align the font size with the code_input
        self.line_numbers.configure(font=("Verdana", 15))  # Set font and size

        # Adjust spacing to add margin or padding
        self.line_numbers.configure(spacing1=1)  # Default spacing for all lines
        self.line_numbers.tag_configure("first_line", spacing1=25)  # Adjust first-line spacing

        # Apply custom alignment for the first line
        self.line_numbers.tag_add("first_line", "1.0", "1.end")
        self.line_numbers.tag_configure("center", justify="center")  # Center-align numbers
        self.line_numbers.tag_add("center", "1.0", "end")

        # Update the scroll synchronization
        self.line_numbers.yview_moveto(self.code_input.yview()[0])
        self.code_input.configure(font=("Verdana", 16))  # Match font size
 # Match font size
    # Match font size
           
    def sync_scrollbars(self, *args):
        try:
            # Synchronize the scroll position of the line numbers with the code input
            self.line_numbers.yview_moveto(self.code_input.yview()[0])
            self.code_input.yview(*args)
        except Exception as e:
            print(f"Error syncing scrollbars: {e}")


    def setup_widgets(self):
        # Input box for code
        self.code_frame = ctk.CTkFrame(self.root, width=200, height=600, fg_color="#8f3901", corner_radius=10) #width and height of the outline box
        self.code_frame.place(x=100, y=140) #x and y for input box
        self.code_input = ctk.CTkTextbox(self.code_frame, width=650, height=500, #width and height of the box
                                         font=("Verdana", 10),
                                         fg_color="#ffe9db",
                                         text_color=TEXT_COLOR,
                                         wrap="word")
        self.code_input.configure(spacing1=2)
        # Insert placeholder text
        self.placeholder_text = "Code will be placed here...\n"
        self.code_input.insert(tk.END, self.placeholder_text)
                        # Bind to update line numbers dynamically
        self.code_input.bind("<KeyRelease>", lambda event: self.update_line_numbers())
        self.code_input.bind("<MouseWheel>", lambda event: self.update_line_numbers())

                # Error at line numbers
        self.line_numbers = tk.Text(self.code_frame, width=4, padx=3, takefocus=0, fg="#ffe9db",
                                     bg="#8f3901", highlightthickness=0, state=tk.DISABLED)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_input.pack(padx=10, pady=10)
        # self.code_input.configure(yscrollcommand=self.sync_scrollbars)
        # self.line_numbers.configure(yscrollcommand=self.sync_scrollbars)

        #image for Lexical Analyzer Button/Button
        self.analyze_button = Image.open("Images/Lexical.png")
        self.resize_analyze_button = self.analyze_button.resize((200,50))
        self.analyze_button_picture = ImageTk.PhotoImage(self.resize_analyze_button)
        self.image_analyze_button = tk.Button(image=self.analyze_button_picture, borderwidth=0, command=self.analyze_code_with_sound)
        self.image_analyze_button.place(x=190, y=920)  #x and y for lexical
        
        #image for Semantic Analyzer Button/Button
        self.semantic_button = Image.open("Images/Semantic.png")
        self.resize_semantic_button = self.semantic_button.resize((200,50))
        self.semantic_button_picture = ImageTk.PhotoImage(self.resize_semantic_button)
        self.image_semantic_button = tk.Button(image=self.semantic_button_picture, borderwidth=0, command=self.semantic_input_with_sound)
        self.image_semantic_button.place(x=450, y=920) #x and y for semantic

        #image for Syntax Button
        self.syntax_button = Image.open("Images/Syntax.png") #placeholder for syntax button
        self.resize_syntax_button = self.syntax_button.resize((200,50))
        self.syntax_button_picture = ImageTk.PhotoImage(self.resize_syntax_button)
        self.image_syntax_button = tk.Button(image=self.syntax_button_picture, borderwidth=0, command=self.syntax_analyzer_with_sound)
        self.image_syntax_button.place(x=710, y=920) #x and y for syntax button

        #image for Clear Button
        self.clear_button = Image.open("Images/Clear.png")
        self.resize_clear_button = self.clear_button.resize((40,40))
        self.clear_button_picture = ImageTk.PhotoImage(self.resize_clear_button)
        self.image_clear_button = tk.Button(image=self.clear_button_picture, borderwidth=0, command=self.clear_input_with_sound)
        self.image_clear_button.place(x=700, y=90) #may differ in 1920x1200 resolution, x and y for clear buttons

        #image for Undo Button
        self.undo_button = Image.open("Images/Undo.png")
        self.resize_undo_button = self.undo_button.resize((40,40))
        self.undo_button_picture = ImageTk.PhotoImage(self.resize_undo_button)
        self.image_undo_button = tk.Button(image=self.undo_button_picture, borderwidth=0, command=self.undo_input_with_sound)
        self.image_undo_button.place(x=760, y=90) #may differ in 1920x1200 resolution, x and y for clear buttons


        #Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Verdana", 14), fieldbackground="#ffe9db", rowheight=25)  # Change font for Treeview
        style.configure("Treeview.Heading", font=("Verdana", 16), background="#d88e41", foreground="#ffe9db")  # Change font for headings

        # Token Table
        self.token_frame = ctk.CTkFrame(self.root, fg_color="#8f3901", corner_radius=10)
        self.token_frame.place(x=830, y=50) #x and y for the table

        self.token_tree = ttk.Treeview(self.token_frame, columns=("Index", "Lexeme", "Token"), show='headings',
                                       height=40)
        self.token_tree.heading("Index", text="Index")
        self.token_tree.heading("Lexeme", text="Lexeme")
        self.token_tree.heading("Token", text="Token")
        self.token_tree.column("Index", width=120, anchor="center")
        self.token_tree.column("Lexeme", width=440, anchor="center")
        self.token_tree.column("Token", width=230, anchor="center")
        self.token_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Terminal Output
        self.terminal_frame = ctk.CTkFrame(self.root, width=200, height=100, fg_color="#8f3901", corner_radius=10)
        self.terminal_frame.place(x=100, y=800) #x and y for terminal
        self.terminal_output = ctk.CTkTextbox(self.terminal_frame, width=700, height=85,
                                              font=PIXEL_FONT,
                                              fg_color="#ffe9db",
                                              text_color="red",
                                              wrap="word")
        self.terminal_output.insert(tk.END, "Errors will be displayed here...\n")
        self.terminal_output.pack(padx=10, pady=2)

    def place_widgets(self):
        # Dynamically position widgets
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        self.canvas.config(width=width, height=height)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((width, height), Image.LANCZOS))
        self.canvas.itemconfig(self.bg, image=self.bg_photo)

        # Input code frame
        self.code_frame.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.5)

        # Buttons
        self.image_analyze_button.place(relx=0.05, rely=0.7, relwidth=0.1, relheight=0.05)
        self.image_clear_button.place(relx=0.17, rely=0.7, relwidth=0.1, relheight=0.05)
        self.image_undo_button.place(relx=0.29, rely=0.7, relwidth=0.1, relheight=0.05)

        # Token table
        self.token_frame.place(relx=0.5, rely=0.1, relwidth=0.45, relheight=0.5)

        # Terminal output
        self.terminal_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.15)

    def on_resize(self, event):
        self.place_widgets()

 # Sound Effects

    def analyze_code_with_sound(self):
        mixer.Sound.play(click_sound)
        self.analyze_code()

    def semantic_input_with_sound(self):
        mixer.Sound.play(click_sound)
        self.semantic_input()

    def syntax_analyzer_with_sound(self):
        mixer.Sound.play(click_sound)
        self.syntax_analyzer()

    def clear_input_with_sound(self):
        mixer.Sound.play(delete_sound)
        self.clear_input()

    def undo_input_with_sound(self):
        mixer.Sound.play(delete_sound)
        self.undo_input()


    def analyze_code(self): #lexer button

        # Clear previous tokens and errors
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete("1.0", tk.END)

        # Get code from input box and handle any extra newline at the end
        code = self.code_input.get("1.0", tk.END).rstrip("\n")  # Remove the trailing newline
        lines = code.splitlines()  # Split code into lines for easier indexing
        
        # Do not strip the code; keep all spaces intact
        lexer = Lexer("<input>", code)
        tokens, errors = lexer.make_tokens()

        # Configure Treeview tags row background
        self.token_tree.tag_configure("all_rows", background="#ffe9db")  # Light blue background

        # Display tokens in the treeview with row numbers
        row_number = 1
        for token in tokens:
            if isinstance(token, Token):  # Ensure it's a valid token object
                lexeme = token.value if token.value is not None else token.token
                # Check for spaces as errors
                if token.token == "SPACE":
                    self.terminal_output.insert(tk.END, f"Error: Unexpected whitespace at line {row_number}\n")
                # Check for newlines as tokens
                elif token.token == "NEWLINE":
                    lexeme = "\\n"  # Display as "\n" in the table for clarity
                row_tag = "odd_row" if row_number % 2 == 1 else "even_row"
                self.token_tree.insert("", tk.END, values=(row_number, lexeme, token.token), tags=("all_rows",))
                row_number += 1

        if errors:
            self.terminal_output.insert(tk.END, "\n".join(errors) + "\n")
        else:
            self.terminal_output.insert(tk.END, "No errors found.\n")
            
    def clear_input(self):
        """Clear the code input box"""
        self.code_input.delete("1.0", tk.END)
        
    def undo_input(self): #added for the undo button feature
        """Undo the last action in the code input box"""
        current_text = self.code_input.get("1.0", tk.END)
        if len(current_text) > 1:  # Check if there's any text to undo
            self.code_input.delete("1.0", tk.END)
            self.code_input.insert("1.0", current_text[:-2])  # Remove the last character (including newline)


    def syntax_analyzer(self): # syntax button
        
        # Clear previous tokens and errors
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete("1.0", tk.END)

        # Get code from input box and handle any extra newline at the end
        code = self.code_input.get("1.0", tk.END).rstrip("\n")  # Remove the trailing newline
        lines = code.splitlines()  # Split code into lines for easier indexing
        
        # Do not strip the code; keep all spaces intact
        lexer = Lexer("<input>", code)
        tokens, errors = lexer.make_tokens()

        # Configure Treeview tags row background
        self.token_tree.tag_configure("all_rows", background="#ffe9db")  # Light blue background

        # Display tokens in the treeview with row numbers
        row_number = 1
        for token in tokens:
            if isinstance(token, Token):  # Ensure it's a valid token object
                lexeme = token.value if token.value is not None else token.token
                # Check for spaces as errors
                if token.token == "SPACE":
                    self.terminal_output.insert(tk.END, f"Error: Unexpected whitespace at line {row_number}\n")
                # Check for newlines as tokens
                elif token.token == "NEWLINE":
                    lexeme = "\\n"  # Display as "\n" in the table for clarity
                row_tag = "odd_row" if row_number % 2 == 1 else "even_row"
                self.token_tree.insert("", tk.END, values=(row_number, lexeme, token.token), tags=("all_rows",))
                row_number += 1

        if errors:
            self.terminal_output.insert(tk.END, "\n".join(errors) + "\n")
        else:
            # self.terminal_output.insert(tk.END, "No errors found.\n")
            # If lexer is successful, run syntax parser
            syntax_result, syntax_error = run("<junimo code>", code)
            if syntax_error:
                # self.terminal_output.insert(tk.END, syntax_error.details)
                for err in syntax_error:
                    self.terminal_output.insert(tk.END, err.as_string())
                # for err in syntax_error:
                #     if isinstance(err, list):
                #         for e in err:
                #             errorResult, fileDetail, arrowDetail, arrows = e.as_string()
                #             self.terminal_output.insert(tk.END, errorResult)
                #             self.terminal_output.insert(tk.END, fileDetail)
                #             self.terminal_output.insert(tk.END, arrowDetail)
                #             # errors_text.insert(tk.END, arrows)
                #     else:
                #         errorResult, fileDetail, arrowDetail, arrows = err.as_string()
                #         self.terminal_output.insert(tk.END, errorResult)
                #         self.terminal_output.insert(tk.END, fileDetail)
                #         self.terminal_output.insert(tk.END, arrowDetail)
                #         # errors_text.insert(tk.END, arrows)
            else:
                
                # for res in syntax_result:
                self.terminal_output.insert(tk.END, "SUCCESS from syntax")
                # errors_text.insert(tk.END, "SUCCESS")


if __name__ == "__main__":
    root = ctk.CTk()
    app = StardewLexerGUI(root)
    root.mainloop()
