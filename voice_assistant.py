
import speech_recognition as sr
import pyttsx3 as ptt
import pywhatkit as pwtk
import datetime as dt
import wikipedia
import webbrowser
import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from random import randint
from unidecode import unidecode

class Voice_assistant():
    def __init__(self, apostrophe, end=False):
        # apostrofa - słowo klucz, od którego powinna zaczynać się każda komenda
        self.apostrophe = apostrophe.lower()
        self.listener = sr.Recognizer()
        self.speaker = ptt.init()
        self.mode = None
        # lista słów kluczy, które będą skutkować uruchomieniem odtwarzania piosenki na YouTube
        self.playing_list_commands = ['zagraj', 'graj', 'puść']
        # lista słów kluczy, dzięki którym asystent poda aktualną godzinę
        self.time_list_commands = ['która jest godzina', 'podaj godzinę', 'jaka jest godzina', 'podaj czas']
        # lista słów kluczy, dzięki którym asystent poda dane z Wikipedii
        self.wiki_list_commands = ['co to jest', 'co to są', 'kto to jest', 'kto to są', 'kto to był', 'kim jest', 'kim był', 'czym są', 'kim są']
        # lista słów kluczy, dzięki którym asystent poszuka odpowiedzi z Google
        self.answer_question_list_commands = ['co', 'czym', 'czy', 'kto', 'kim', 'czemu', 'dlaczego', 'skąd', 'gdzie', 'jakich', 'jak', 'ile', 'ilu', 'po co', 'który', 'którą']
        # lista słów kluczy, dzięki którym asystent wyszuka hasło w wyszukiwarce Google
        self.google_search_list_commands = ['znajdź w google', 'wyszukaj w google', 'szukaj w google', 'znajdź', 'wyszukaj', 'szukaj', 'google']
        # lista słów kluczy, dzięki którym asystent pokaże obrazek znaleziony w internecie
        self.show_image_list_commands = ['pokaż na ekranie', 'wyświetl na ekranie', 'pokaż', 'wyświetl']
        self.file_list_to_load = []
        # lista słów kluczy podziękowań
        self.thanks_list_commands = ['dziękuję', 'dzięki']
        # lista słów kluczy, które kończą działanie programu
        self.thanks_list_response = ['Proszę. Nie ma za co', 'Proszę. Jestem do usług', 'Proszę bardzo']
        self.exit_list_commands = ['zakończ program', 'stop', 'wyjdź']
        self.end = end # Jeśli end=True wtedy działanie programu zostanie zakończone
        # lista zwrotów pożegnalnych
        self.bye_list = ['Do widzenia', 'Miej dobry dzień. Cześć', 'Żegnaj', 'Ja lecę. Miłego dnia', 'Do zobaczenia wkrótce']

    def talk(self, speech):
        self.speaker.say(speech)
        self.speaker.runAndWait()

    def listen(self):
        command = ''
        try:
            with sr.Microphone() as source:
                # print('I am listening you...')
                audio = self.listener.listen(source)
                command = self.listener.recognize_google(audio, language='pl-PL')
                command = command.lower()
        except:
            pass
        return command

    def execute_command(self, command):
        self.file_list_to_load = []
        if self.apostrophe in command:
            command = command.replace(self.apostrophe, '')
            for item in self.playing_list_commands:
                if item in command:
                    self.mode = 'music_playing'
                    key = item
                    command = command.replace(key, '')
                    try:
                        pwtk.playonyt(command)
                    except:
                        self.talk('Niestety, nie mogę zagrać tej piosenki.')
                    return None
            for item in self.time_list_commands:
                if item in command:
                    self.mode = 'current_time'
                    try:
                        current_time = dt.datetime.now().strftime("%H:%M")
                        self.talk(f'Teraz jest godzina {current_time}')
                    except:
                        self.talk('Niestety, nie wiem, która jest godzina.')
                    return None
            for item in self.wiki_list_commands:
                if item in command:
                    self.mode = 'wiki_answer'
                    key = item
                    command = command.replace(key, '')
                    try:
                        wikipedia.set_lang('pl')
                        answer = wikipedia.summary(command, sentences=4)
                        self.talk(answer)
                    except:
                        self.talk(f'Niestety, nie wiem {key} {command}')
                    return None
            for item in self.answer_question_list_commands:
                if item in command:
                    self.mode = 'question_answer'
                    try:
                        command = unidecode(command)
                        command = command.replace(' ', '+')
                        url = 'https://www.google.pl/search?q='+command
                        self.talk('Szukam odpowiedzi w internecie')
                        webbrowser.open(url)
                    except:
                        self.talk(f'Niestety, nie wiem {command}')
                    return None
            for item in self.google_search_list_commands:
                if item in command:
                    self.mode = 'Google_search'
                    key = item
                    command = command.replace(key, '')
                    url = f'https://www.google.com.tr/search?q={command}'
                    try:
                        webbrowser.open(url)
                    except:
                        self.talk(f'Nie udało mi się wyszukać {command}')
                    return None
            for item in self.show_image_list_commands:
                if item in command:
                    self.mode = 'show_image'
                    key = item
                    command = command.replace(key, '')
                    param_dict = {'q':command, 'tbm':'isch'}
                    html = requests.get('https://www.google.pl/search', params=param_dict, timeout=50)
                    soup = BeautifulSoup(html.content, "html.parser")
                    image = soup.select('div img')
                    location = os.getcwd()
                    try:
                        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            image_url = image[i]['src']
                            relative_path = f'\\temporary\\file{i}.jpg'
                            urllib.request.urlretrieve(image_url, location + relative_path)
                            self.file_list_to_load.append(relative_path)
                    except:
                        pass
                    return None
            for item in self.thanks_list_commands:
                if item in command:
                    self.mode = 'thank'
                    range = len(self.thanks_list_response) - 1
                    self.talk(self.thanks_list_response[randint(0, range)])
                    return None
            for item in self.exit_list_commands:
                if item in command:
                    self.mode = 'bye'
                    self.end = True
                    range = len(self.bye_list) - 1
                    self.talk(self.bye_list[randint(0, range)])
                    return None
            if len(command) > 0:
                self.mode = 'not_understood'
                self.talk('Nie zrozumiałam Cię. Proszę powtórz.')


if __name__ == '__main__':
    app_version = 2.2
    # apostrophe = 'Dominika'
    apostrophe = ''
    va = Voice_assistant(apostrophe)
    if len(apostrophe) > 0:
        va.talk(f'Z tej strony {va.apostrophe}.')
    va.talk('Co mogę dla Ciebie zrobić?')
    while not va.end:
        command = va.listen()
        va.execute_command(command)