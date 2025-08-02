import tkinter as tk
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("430x680")
        self.resizable(False, False)

        # Themes
        self.dark_mode = True
        self.themes = {
            "dark": {
                "bg": "#ffffff", "fg": "#ffffff",
                "btn": "#3c3f41", "btn_hover": "#4b5052",
                "entry": "#2b2b2b", "history": "#1e1e1e"
            },
            "light": {
                "bg": "#f0f0f0", "fg": "#00FFFF",
                "btn": "#dcdcdc", "btn_hover": "#c0c0c0",
                "entry": "#ffffff", "history": "#eaeaea"
            }
        }

        self.expression = ""
        self.history = []
        self.last_answer = "0"

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        # Display
        self.display = tk.Entry(self, font=("Consolas", 20), bd=0, justify='right')
        self.display.pack(expand=False, fill='both', ipady=20)
        self.display.bind("<Button-3>", self.right_click_menu)

        # History
        self.history_box = tk.Text(self, height=6, font=("Consolas", 12), bd=0, state='disabled')
        self.history_box.pack(fill='both', padx=4, pady=2)

        # Button layout
        buttons = [
            ["C", "⌫", "(", ")", "Theme"],
            ["sin", "cos", "tan", "√", "^"],
            ["log", "ln", "π", "e", "/"],
            ["7", "8", "9", "*", "Hist"],
            ["4", "5", "6", "-", "mod"],
            ["1", "2", "3", "+", "Ans"],
            ["0", ".", "=", "abs", "!"],
            ["deg", "rad", "", "", ""]
        ]

        for row in buttons:
            frame = tk.Frame(self)
            frame.pack(expand=True, fill='both')
            for btn in row:
                if btn == "":
                    tk.Label(frame, text="").pack(side="left", expand=True, fill="both", padx=1, pady=1)
                    continue
                b = tk.Button(frame, text=btn, font=("Consolas", 14),
                              command=lambda x=btn: self.on_button_click(x))
                b.pack(side="left", expand=True, fill="both", padx=1, pady=1)

        # Keyboard support
        self.bind("<Key>", self.on_key)

    def apply_theme(self):
        theme = self.themes["dark" if self.dark_mode else "light"]

        self.configure(bg=theme["bg"])
        self.display.configure(bg=theme["entry"], fg=theme["fg"], insertbackground=theme["fg"])
        self.history_box.configure(bg=theme["history"], fg=theme["fg"])

        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.configure(
                            bg=theme["btn"], fg=theme["fg"],
                            activebackground=theme["btn_hover"],
                            activeforeground=theme["fg"],
                            bd=0
                        )

    def right_click_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Copy", command=lambda: self.clipboard_append(self.display.get()))
        menu.add_command(label="Paste", command=lambda: self.insert_from_clipboard())
        menu.tk_popup(event.x_root, event.y_root)

    def insert_from_clipboard(self):
        try:
            pasted = self.clipboard_get()
            self.expression += pasted
            self.update_display()
        except:
            pass

    def on_key(self, event):
        key = event.char
        if key in "0123456789.+-*/()":
            self.expression += key
        elif key == "\r":
            self.calculate()
        elif key == "\x08":
            self.expression = self.expression[:-1]
        self.update_display()

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "⌫":
            self.expression = self.expression[:-1]
        elif char == "=":
            self.calculate()
        elif char == "Theme":
            self.dark_mode = not self.dark_mode
            self.apply_theme()
        elif char == "Hist":
            self.show_history()
        elif char == "Ans":
            self.expression += self.last_answer
        elif char == "π":
            self.expression += str(math.pi)
        elif char == "e":
            self.expression += str(math.e)
        elif char == "√":
            self.expression += "sqrt("
        elif char == "^":
            self.expression += "**"
        elif char == "abs":
            self.expression += "abs("
        elif char == "!":
            self.expression += "factorial("
        elif char == "mod":
            self.expression += "%"
        elif char == "deg":
            self.expression += "degrees("
        elif char == "rad":
            self.expression += "radians("
        elif char in ["sin", "cos", "tan", "log", "ln"]:
            func_map = {
                "sin": "sin(", "cos": "cos(", "tan": "tan(",
                "log": "log10(", "ln": "log("
            }
            self.expression += func_map[char]
        else:
            self.expression += char
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        # Truncate long expressions in display
        shown = self.expression if len(self.expression) < 100 else self.expression[-100:] + "..."
        self.display.insert(tk.END, shown)

    def calculate(self):
        try:
            expr = self.expression.replace("Ans", self.last_answer)
            parsed = self.parse_expression(expr)
            result = eval(parsed)
            self.last_answer = str(result)
            self.history.append(f"{self.expression} = {result}")
            self.expression = str(result)
        except Exception:
            self.expression = "Error"
        self.update_display()

    def parse_expression(self, expr):
        replacements = {
            "sin": "math.sin", "cos": "math.cos", "tan": "math.tan",
            "log10": "math.log10", "log": "math.log", "sqrt": "math.sqrt",
            "abs": "abs", "factorial": "math.factorial", "degrees": "math.degrees",
            "radians": "math.radians"
        }
        for key in replacements:
            expr = expr.replace(key, replacements[key])
        return expr

    def show_history(self):
        self.history_box.configure(state='normal')
        self.history_box.delete(1.0, tk.END)
        for item in reversed(self.history[-12:]):
            self.history_box.insert(tk.END, item + "\n")
        self.history_box.configure(state='disabled')

if __name__ == "__main__":
    Calculator().mainloop()
# calculator.py
# This code implements a scientific calculator with a GUI using Tkinter.