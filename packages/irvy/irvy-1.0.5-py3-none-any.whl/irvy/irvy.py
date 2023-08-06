#!/usr/bin/env python3


from irvy.generators.PlaywrightGenerator import PlaywrightGenerator
from irvy.generators.SeleniumGenerator import SeleniumGenerator

import os
from rich.panel import Panel
from rich.text import Text
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class Irvy:
    def __init__(self, language, tool):
        self.language = language
        self.tool = tool

    def generate(self):
        if self.tool == "selenium":
            selenium_generator = SeleniumGenerator(self.language)
            selenium_generator.generate()
        elif self.tool == "playwright":
            playwright_generator = PlaywrightGenerator(self.language)
            playwright_generator.generate()

def main():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Initialize the console
    console = Console()

    # Create a panel
    welcome_message = Text("Welcome to ", style="bold blue")
    welcome_message.append("Irvy", style="bold red")
    welcome_message.append(", Quick setup for your test automation project!", style="bold blue")
    

    # Print ASCII art
    welcome_message.append(r"""
     /$$                               
    |__/                               
     /$$  /$$$$$$  /$$    /$$ /$$   /$$
    | $$ /$$__  $$|  $$  /$$/| $$  | $$
    | $$| $$  \__/ \  $$/$$/ | $$  | $$
    | $$| $$        \  $$$/  | $$  | $$
    | $$| $$         \  $/   |  $$$$$$$
    |__/|__/          \_/     \____  $$
                              /$$  | $$
                             |  $$$$$$/
                              \______/ 
    https://www.irvy.org
    naveen@irvy.org
    """)
    panel = Panel(welcome_message, border_style="green")
    console.print(panel)
    
    languages = ['csharp', 'python', 'javascript']
    tools = ['selenium', 'playwright']

    questions = [
        {
            'type': 'select',
            'name': 'language',
            'message': "What language do you want to use?",
            'choices': languages,
        },
        {
            'type': 'select',
            'name': 'tool',
            'message': "What tool do you want to use?",
            'choices': tools,
        }
    ]

    answers = questionary.prompt(questions)

    language = answers['language']
    tool = answers['tool']
    irvy = Irvy(answers['language'], answers['tool'])
    irvy.generate()

    success_message = Text("Project setup completed successfully!", style="bold green")
    success_panel = Panel(success_message, border_style="green")

    console.print(success_panel)

if __name__ == "__main__":
    main()
