import tkinter as tk
class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")

        # Load state
        self.load_state()

        # Initialize variables
        self.result = 0
        self.operations = 0
        self.error_occurred = False

        # Create history text widgets
        self.history_text = tk.Text(self, width=40, height=5, font=("Segoe", 12), state='disabled')
        self.history_text.grid(row=1, column=0, columnspan=4)
        self.history_text.config(state='normal')  # Enable to allow insertion
        self.history_text.insert(tk.END, "")
        self.history_text.config(state='disabled')  # Disable to prevent further editing

        self.display = tk.Entry(self, width=20, font=("Segoe", 20), state='disabled')
        self.display.grid(row=2, column=0, columnspan=5)
        self.display.insert(tk.END, str(self.result))  # Display last result
        self.display.focus_set()  # Set focus on the entry field

        # Define allowed characters
        self.allowed_chars = set("0123456789+-*/.rq")

        buttons = [
            ('q', 3, 0), ('CE', 3, 1), ('C', 3, 2), ('/', 3, 3),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('*', 4, 3),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('+', 6, 3),
            ('.', 7, 0), ('0', 7, 1), ('r', 7, 2), ('=', 7, 3),
        ]

        for (text, row, column) in buttons:
            button = tk.Button(self, text=text, width=7, height=3, font=("Segoe", 16),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column)
            if text == '=':  # Change color of the '=' button
                button.config(bg='#4F6F52', fg='white')
            if text == 'q':  # Modify command for 'q' button
                button.config(command=self.destroy)

        # Bind Enter key to '=' action
        self.bind('<Return>', lambda event: self.on_button_click('='))
        # Bind Backspace key to 'C' action
        self.bind('<BackSpace>', lambda event: self.on_button_click('C'))

        # Bind keyboard inputs
        self.bind('<Key>', self.on_keyboard_input)

    def load_state(self):
        if hasattr(self, 'display'):
            self.display.delete(0, tk.END)
        try:
            with open("calculator_state.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "times calculator was opened" in line:
                        self.open_count = int(line.split(":")[-1].strip())
                    elif "last result" in line:
                        self.result = float(line.split(":")[-1].strip())
                        if hasattr(self, 'display'):
                            self.display.delete(0, tk.END)
                            self.display.insert(tk.END, str(self.result))  # Display last result
        except FileNotFoundError:
            pass

        if not hasattr(self, 'open_count'):  # If open_count is not already defined
            self.open_count = 0

    def save_state(self):
        with open("calculator_state.txt", "w") as file:
            file.write("times calculator was opened : {}\n".format(self.open_count))
            file.write("last result : {}\n".format(self.result))

    def on_button_click(self, text):
        try:
            self.display.config(state='normal')  # Enable the display for input
            if self.error_occurred:
                self.display.delete(0, tk.END)  # Clear the display
                self.error_occurred = False  # Reset error flag

            # If input is an operator, replace the previous operator in the display
            if text in "+-*/":
                current_text = self.display.get()
                if current_text and current_text[-1] in "+-*/":
                    self.display.delete(len(current_text) - 1, tk.END)
                self.display.insert(tk.END, text)
                return  # Exit early to avoid appending operator to history

            if text == "=":
                expression = self.display.get()
                self.result = eval(expression)
                if len(str(self.result)) > 11:
                    self.result = round(self.result, 5)
                if len(str(self.result)) > 11: # Check if result length exceeds 11 symbol
                    display_text = "Max_Value"
                else:
                    display_text = str(self.result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, display_text)
                self.operations += 1  # Increment operations count on new operation
                if display_text != "Max_Value":  # Only add to history if not "Max_Value"
                    self.history_text.config(state='normal')  # Enable history text for editing
                    self.history_text.insert(tk.END, f"{expression} = {self.result}\n")
                    self.history_text.config(state='disabled')  # Disable history text after editing
            elif text == "CE":
                self.display.delete(0, tk.END)
            elif text == "C":
                current_text = self.display.get()
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, current_text[:-1])  # Remove the last character
            elif text == "q":
                self.destroy()
            elif text == "r":
                self.reset_history()
                self.open_count = 0  # Reset the open count when 'r' is pressed
            else:
                # Clear error and append new input
                if self.display.get() == "Max_Value":
                    self.display.delete(0, tk.END)
                self.display.insert(tk.END, text)
        except SyntaxError:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Invalid syntax")
            self.error_occurred = True
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(e))
            self.error_occurred = True
        finally:
            self.display.config(state='disabled')  # Disable the display after input

    def on_keyboard_input(self, event):
        if event.char in self.allowed_chars:
            if event.char == 'q':
                self.destroy()
            else:
                self.on_button_click(event.char)

    def reset_history(self):
        self.history_text.config(state='normal')
        self.history_text.delete('1.0', tk.END)  # Clear all text
        self.history_text.config(state='disabled')

    def destroy(self):
        self.open_count += 1  # Increment the open count
        self.save_state()
        super().destroy()

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
