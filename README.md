# Text Editor

## Description

This is a simple text editor built using Python and Tkinter. It offers basic functionalities like opening, saving, and running Python files. Additionally, it provides syntax highlighting and theme customization.

## Features

- Open, Save, and Save As functionalities for Python files
- Syntax highlighting for Python code
- Theme customization with support for Monokai and Default Light themes
- Run Python code directly from the editor
- Comment and uncomment code blocks
- Cut, Copy, Paste functionalities
- Scrollable interface

## Dependencies

- Python 3.x
- Tkinter
- Pygments

## How to Run

1. Clone the repository
2. Run `texteditor.pyw`

## Usage

### File Operations

- **New File**: `Ctrl + N`
- **Open File**: `Ctrl + O`
- **Save File**: `Ctrl + S`

### Code Operations

- **Comment/Uncomment**: `Ctrl + /`
- **Run Code**: Accessible from the `Run` menu
- **Test Code**: Accessible from the `Run` menu

### Theme and Syntax

- Change the theme from the `Format` menu
- Enable/Disable syntax highlighting from the `Format` menu

### Available Themes

- **Monokai (Default)**: Dark background with colorful syntax highlighting
- **Default Light**: Light background with standard syntax highlighting

## Code Structure

- `graphics.py`: Handles the themes and syntax highlighting
- `texteditor.pyw`: Main file that contains the Tkinter GUI and functionalities
- `themes.json`: JSON file containing theme configurations

## Contributing

Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
