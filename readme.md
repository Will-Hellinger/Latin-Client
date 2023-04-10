# LTHS Latin Client

This is a Python script designed to aid &| automate certain tasks in LTHS Latin Schoology. It can help you with vocabulary, morphology, and translations. This program uses Selenium WebDriver to interact with the website.

## Prerequisites

- Python 3
- Chromedriver
- Selenium
- PySimpleGUI

## Setup

1. Clone the repository onto your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Configure the `settings.json` file with your Schoology username, password, and the link to your Latin Schoology course (should be in the data folder).
4. Run the script using `python main.py` or `python3 main.py`.

## Features

- Automatically logs in to your LTHS Latin Schoology account.
- Supports multiple modes such as Vocabulary, Noun Adjective Agreement, Infinitive Morphology, Timed Vocabulary, and Timed Morphology.
- Plugins: the bot can load small javascript plugins.
- Discord Rich Presence: display the current mode and assignment on your Discord profile.

## Usage

After setting up the program, run `python main.py` or `python3 main.py` in your terminal to start the bot. Once the bot starts running, it will automatically login to your LTHS Latin Schoology account and begin listening for mode changes. 

You can switch between modes by clicking on the assignment. For example, opening a synopsis assignment will put the client into synopsis mode. It should display all the relevant information on your discord account.

To use the tool, press the action button, it should be the ` key by default.

## Debugger Tool

If you're developing a plugin or making changes to the code, you can use the debugger tool to reload modules and inject cookies into the browser. To launch the debugger tool, run `python main.py --debugger` or `python3 main.py --debugger`. 

## Contributing

Contributions are welcome! If you have any ideas or suggestions, please feel free to create an issue or submit a pull request. 

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.