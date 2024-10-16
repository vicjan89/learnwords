import json
import random
import string
from pathlib import Path
import webbrowser
import os

from translate import Translator
from rich.console import Console
from rich.table import Table

def add_words():
    translator = Translator(to_lang='ru')
    folder = Path(os.path.dirname(__file__))
    path = Path('known_words.json')
    path_input = Path('input.txt')
    try:
        with open(folder / path, 'r', encoding='utf-8') as known_words:
            known_words = json.load(known_words)
    except FileNotFoundError:
        known_words = {}
    with open(folder / path_input, 'r', encoding='utf-8') as file:
        for line in file:
            new_words = line.strip().lower()
            cleared = []
            for chr in new_words:
                if chr in string.ascii_letters:
                    cleared.append(chr)
                else:
                    cleared.append(' ')
            new_words = ''.join(cleared)
            new_words = new_words.split(' ')
            for word in new_words:
                word = word.strip()
                if word not in known_words:
                    if len(word) > 1:
                        translation = translator.translate(word)
                        known_words[word] = (translation, False)
    with open('learnwords' / path, 'w', encoding='utf-8') as known_words_file:
        json.dump(known_words, known_words_file, indent=4, sort_keys=True, ensure_ascii=False)

def check_articles(name):
    folder = Path(os.path.dirname(__file__))
    filename = Path('known_words.json')
    with open(folder / filename, 'r', encoding='utf-8') as file:
        articles = json.load(file)
        return name in articles

def get_words():
    folder = Path(os.path.dirname(__file__))
    filename = Path('known_words.json')
    with open(folder / filename, 'r', encoding='utf-8') as file:
        known_words = json.load(file)
    total_words = len(known_words)
    numbers = set(range(1, total_words + 1))
    num = 1
    for translate, known in known_words.values():
        if known:
            numbers.remove(num)
        num += 1
    return known_words, numbers

def learn_words(quantity: int):
    known_words, numbers = get_words()
    selected_words = random.sample(list(numbers), quantity)
    table = Table(title="Learn Words")

    table.add_column("Num", justify="right", style="cyan", no_wrap=True)
    table.add_column("Words", justify="left", style="magenta")
    table.add_column("Translate", style="green")
    num = 1
    for word, translate in known_words.items():
        if num in selected_words:
            table.add_row(str(num), word, translate[0])
        num += 1
    console = Console()
    console.print(table)

def learn():
    known_words, numbers = get_words()
    known_words_list = list(known_words.items())
    known_words_list = [word for word in known_words_list if not word[1][1]]
    folder = Path(os.path.dirname(__file__))
    filename = Path('known_words.json')
    while True:
        command = input('>')
        if command == 'e':
            with open(folder / filename, 'w', encoding='utf-8') as known_words_file:
                json.dump(known_words, known_words_file, indent=4, sort_keys=True, ensure_ascii=False)
            break
        elif command == 'd':
            known_words[rand_word][1] = True
            known_words_list.remove(word)
        elif command == 's':
            statistic(known_words)
            continue
        elif command == 't':
            new_translate = input('New translate: ')
            if new_translate:
                known_words[rand_word][0] = new_translate
            continue
        elif command == 'b':
            webbrowser.open_new('https://wooordhunt.ru/word/' + rand_word)
            continue
        word = random.choice(known_words_list)
        rand_word, (translate, known) = word
        print(f'{rand_word}                 {translate}\n')


def mark_known(numbers: int | list):
    if isinstance(numbers, int):
        numbers = [numbers]
    folder = Path(os.path.dirname(__file__))
    filename = Path('known_words.json')
    with open(folder / filename, 'r', encoding='utf-8') as file:
        known_words = json.load(file)
    num = 1
    for word, translate in known_words.items():
        if num in numbers:
            known_words[word][1] = True
        num += 1
    with open(folder / filename, 'w', encoding='utf-8') as known_words_file:
        json.dump(known_words, known_words_file, indent=4, sort_keys=True, ensure_ascii=False)

def known_words():
    folder = Path(os.path.dirname(__file__))
    filename = Path('known_words.json')
    with open(folder / filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def statistic(known_words):
    known_count = 0
    total = 0
    for word, (translate, known) in known_words.items():
        if known:
            known_count += 1
        total += 1
    print(f'Known words = {known_count} ({known_count / total * 100:.0f}%), Unknown words={total - known_count}, Total words = {total}\n')

