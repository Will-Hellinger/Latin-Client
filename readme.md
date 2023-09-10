# LTHS Latin Client

This is a Python script designed to aid and or automate certain tasks in LTHS Latin Schoology. It can help you with vocabulary, morphology, translations and more.

## <u>Setup</u>

1. Clone the repository onto your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Configure the `settings.json` file with your Schoology username, password, and the link to your Latin Schoology course (should be in the data folder).
4. Run the script using `python main.py` or `python3 main.py`.

## <u>Features</u>

- Automatically logs in to your LTHS Latin Schoology account.
- Supports multiple assignment types such as, Synopsis, Compositions, Noun Adjective Agreement, Infinitive Morphology, Timed Vocabulary, Timed Morphology, and Catullus.
- Plugins: the bot can load small javascript plugins.
- Discord Rich Presence: display the current mode and assignment on your Discord profile.

## <u>Usage</u>

After setting up the program, run `python main.py` or `python3 main.py` in your terminal to start the bot. Once the bot starts running, it will automatically login to your LTHS Latin Schoology account and begin listening for mode changes. 

You can switch between modes by clicking on the assignment. For example, opening a synopsis assignment will put the client into synopsis mode. It should display all the relevant information on your discord account.

To use the tool, press the action button, it should be the ` key by default.

## <u>Debugger Tool</u>

The debugging tool can be found as a function within the main script. It's a simple GUI that allows you to reload modules, inject tokens, spoof activity, and connect multiple clients together. It's run on a separate thread, so it won't interfere with the main program.W

If you're developing a plugin or making changes to the code, you can use the debugger tool to reload modules, and inject tokens, spoof activity, and connect multiple clients together. To launch the debugger tool, run `python main.py --debugger` or `python3 main.py --debugger`.

When adding a module to the program, (for example a new assignment type), you can reload the module by selecting it from a dropdown in the debugger. In order to do this however you must add the imported module to the module list found within the debugger function.

## <u>Contributing</u>

Contributions are welcome! However, I cannot maintain this project anymore as I no longer have access to the LTHS Latin Server. (I graduated lol) If you would like to contribute, please feel free to open a pull request.

### Adding a new assignment type
    To add a new assignment type, create a new python file in the main folder. The python file should be called the same thing as the assignment itself (or a shortened version). To add this into the program, you must add text from the assignment page title into the "modes" list which can be found in the info.py file <line 25>.

    This list is used in the main.py when scanning for assignments and switching modes. If the assignment title contains any of the strings in the modes list, it will switch to that mode. For example, if the assignment title is "Synopsis 1-10", it will switch to synopsis mode. To add the new python file for that mode, you must first import the file into the main.py then go to the main.py file again <line 307> and add the function call to the switch statement.

    There are 2 main switch statements inside main.py. The first for "doAction" is for when you hit the action key. The second "enterKey" is for when you hit the enter key. If you want your function to run once, have it reset the key back to False, otherwise it will keep running unless the user hits the key again.

### Formatting
    This project is ment to follow the following formatting rules:

    - tab size: 4
    - snake_case for variables and functions
    - docstrings for functions
    - comments for code that is hard to understand (although I did not follow this rule very well)
    - Reduce redundant code, chances are it's the information you're looking for can be found in the info.py file
    - Use the debugger tool to test your code (The debugger lets you keep running the program while you make changes to the code, just reload the module and it should update (How to reload can be found in the debugger section of this readme))

Cache files can be shared btw.

## <u>License</u>

This project is licensed under the MIT License - see the `LICENSE` file for details.