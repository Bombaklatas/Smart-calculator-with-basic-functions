## Simple Calculator Application
## Introduction
## What is your application?
The Simple Calculator is a Python-based graphical application that performs basic arithmetic operations. It has a user-friendly interface with buttons for digits, operators, and functions like clear (C), clear entry (CE), and quit (q). The application keeps track of the calculation history and the last result.

## How to run the program?
To run the program, you need to have Python and Tkinter installed on your system. Save the code in a file named calculator.py and execute it:
```python
calculator.py
```
## How to use the program?
Launch the application.
Use the on-screen buttons or your keyboard to input numbers and operations.
Click '=' or press Enter to see the result of your calculation.
Use 'C' to clear the last character, 'CE' to clear the entire entry, "r" to clear history of your calculations and times calculator was opened and 'q' to quit the application.
The result of the calculation and the history of operations will be displayed on the screen.
## Body/Analysis
Functional Requirements Implementation
Load and Save State
The application saves the state, including the number of times the application was opened and the last result, in a file named calculator_state.txt. It loads this state when the application starts.
```python
def load_state(self):
    # Load state from file
    ...

def save_state(self):
    # Save state to file
    ...
```
## User Interface
The UI is created using Tkinter, with buttons for digits, operations, and special functions. The history and display are implemented using Text and Entry widgets.

```python
# Create history text widget
self.history_text = tk.Text(...)

# Create display entry widget
self.display = tk.Entry(...)

# Define buttons
buttons = [
    ...
]

# Create buttons and assign commands
for (text, row, column) in buttons:
    button = tk.Button(self, ...)
    button.grid(row=row, column=column)
    ...
```
## Operations and Input Handling
Button clicks and keyboard inputs are handled to perform calculations. The application supports basic arithmetic operations, displaying results, and handling errors.
```python
def on_button_click(self, text):
    # Handle button clicks
    ...

def on_keyboard_input(self, event):
    # Handle keyboard inputs
    ...
```
## Code Snippets
Load State Function:
```python
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
                        self.display.insert(tk.END, str(self.result))
    except FileNotFoundError:
        pass

    if not hasattr(self, 'open_count'):
        self.open_count = 0
```
## Error handling 
error handling was done using try and exept and finally methods that were discussed during theory lessons which i found very usefull , you can find it in on_button_click method.
on_button_click method:
```python
def on_button_click(self, text):
    try:
        self.display.config(state='normal')
        if self.error_occurred:
            self.display.delete(0, tk.END)
            self.error_occurred = False

        if text in "+-*/":
            current_text = self.display.get()
            if current_text and current_text[-1] in "+-*/":
                self.display.delete(len(current_text) - 1, tk.END)
            self.display.insert(tk.END, text)
            return

        if text == "=":
            expression = self.display.get()
            self.result = eval(expression)
            if len(str(self.result)) > 11:
                self.result = round(self.result, 5)
            if len(str(self.result)) > 11:
                display_text = "Max_Value"
            else:
                display_text = str(self.result)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, display_text)
            self.operations += 1
            if display_text != "Max_Value":
                self.history_text.config(state='normal')
                self.history_text.insert(tk.END, f"{expression} = {self.result}\n")
                self.history_text.config(state='disabled')
        elif text == "CE":
            self.display.delete(0, tk.END)
        elif text == "C":
            current_text = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current_text[:-1])
        elif text == "q":
            self.destroy()
        elif text == "r":
            self.reset_history()
        else:
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
        self.display.config(state='disabled')
```
## Used OOP pillars
## 1. Encapsulation
Encapsulation involves bundling the data (attributes) and methods (functions) that operate on the data into a single unit, or class, and restricting access to some of the object's components.
In my code, encapsulation is demonstrated through the use of instance variables and methods within the CalculatorApp class. For example:
```python
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
        ...
```
## 2. Abstraction
Abstraction means hiding the complex implementation details and showing only the necessary features of the object.
In your code, abstraction is achieved by defining methods that hide the implementation details of specific functionalities, such as load_state, save_state, on_button_click, on_keyboard_input, and reset_history.
For example:

```python
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
                        self.display.insert(tk.END, str(self.result))
    except FileNotFoundError:
        pass

    if not hasattr(self, 'open_count'):
        self.open_count = 0
```
## 3. Inheritance
Inheritance allows a class to inherit the properties and methods of another class.

In your code, inheritance is shown by inheriting from the tk.Tk class, which provides all the necessary methods and properties for creating a Tkinter application:

```python
class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        ...
```
## 4. Polymorphism
Polymorphism allows methods to do different things based on the object it is acting upon, even though they share the same name.

In your code, polymorphism is less explicitly visible since we don't see method overriding or method overloading directly. However, the use of the eval function to evaluate expressions dynamically can be considered a form of polymorphism:

```python
if text == "=":
    expression = self.display.get()
    self.result = eval(expression)
    ...
```
Additionally, the on_button_click method can handle different types of button inputs in various ways based on the input text:

```python
def on_button_click(self, text):
    ...
    if text in "+-*/":
        ...
    elif text == "=":
        ...
    elif text == "CE":
        ...
    elif text == "C":
        ...
    elif text == "q":
        ...
    elif text == "r":
        ...
    else:
        ...
```
## Results and Summary
- Results
- Successfully implemented a functional calculator with basic arithmetic operations.
- Implemented state saving and loading, allowing persistence between sessions.
- Created a user-friendly interface using Tkinter.
- Added errors for missusing the calculator.
## Challenges
- Handling various edge cases in user input and ensuring the program does not crash.
- Managing the state of the display and history text widgets to ensure proper updates and user interactions.
- Adding and evaluating errors , also limiting input options from not open textbox to only button inputs that are shown on the screen ( means you can enter only buttons that are displayed if a is not displayed , the calculator will not register it)
## Conclusions
- This coursework achieved the development of a simple yet functional calculator application in Python. The application saves its state, provides a user-friendly interface, and handles various user inputs effectively. Future improvements could include more advanced mathematical functions, a better error handling mechanism, and an enhanced UI.

## Future Prospects
- Adding scientific calculator functions.
- Improving the error handling system.
- Enhancing the user interface with themes and animations.
