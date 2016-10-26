# -*- coding:utf-8 -*-
import webbrowser
from colorama import init, Fore, Style
from quiz import app
from quiz.generator import Generator


init()
print(Fore.LIGHTYELLOW_EX + 'Generating HBR quiz out of your notes...' + Fore.LIGHTRED_EX)
generator = Generator()
generator.generate_quiz()
print(Fore.LIGHTGREEN_EX + 'Generated HBR quiz successfully' + Style.RESET_ALL)
print(Fore.LIGHTCYAN_EX + 'Launching HBR quiz on your default browser' + Style.RESET_ALL)
webbrowser.open_new_tab('http://localhost:5000')
app.run(threaded=True)
