import textwrap

from os import system
from time import sleep
from .utilities.menu import Menu
from .utilities.community_console import CommunityConsole
from .utilities.profile_console import ProfileConsole
from .utilities.chat_console import ChatConsole
from colorama import Fore, Style

class Console:
    def __init__(self, bot):
        """
        The Console class is responsible for the overall operation of the terminal application.

        :param bot: An instance of the bot which will interact with the Amino API.
        :type bot: Bot
        """
        self.bot = bot
        self.menu = Menu(self)
        self.community_console = CommunityConsole(self)
        self.profile_console = ProfileConsole(self)
        self.chat_console = ChatConsole(self)

    def print(self, text="", amount=0):
        """
        Prints a string with a specified indentation.

        :param text: The string to be printed.
        :type text: str
        :param amount: The number of spaces to indent.
        :type amount: int
        """
        print(textwrap.indent(text, ' ' * amount))

    def sleep(self, seconds):
        """
        Sleeps for a specified number of seconds.

        :param seconds: The number of seconds to sleep.
        :type seconds: int
        """
        sleep(seconds)

    def clear(self):
        """
        Clears the console screen irrespective of the platform (Windows/Linux).
        """
        clear_command = "cls || clear"
        system(clear_command)

    def input(self, text):
        """
        Accepts user input prefixed with a fixed number of spaces for consistent look and feel.

        :param text: The prompt to be displayed to the user.
        :type text: str
        :return: User input as a string.
        """
        return input(" " * 0 + text)

    def fetch_menu(self):
        """
        Displays the main menu of the application to the user and processes their input.
        """
        self.menu.display()
