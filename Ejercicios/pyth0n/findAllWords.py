import string
import requests
import re
from bs4 import BeautifulSoup
import click
import os
import random


def get_html_of(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)

    return resp.content.decode()


def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count


def get_all_words_from(url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)


def get_top_words_from(all_words, min_lenght):
    occurrences = count_occurrences_in(all_words, min_lenght)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)


def save_word(word, output):
    with open(output, 'a') as my_file:
        my_file.write(word + "\n")


def max_num_words(number_words, top_words):
    number_words = 10

    if int(len(top_words)) < number_words:
        number_words = int(len(top_words)) 

    return number_words 


def mutation(word):
    print(word.capitalize())
    print(word.lower())
    print(word.upper())
    print(word + str(random.randint(1970, 2023)) + str(''.join(random.choices(string.punctuation))))



def output_words(output, number_words, top_words):
    if output != 'none' and os.path.exists(output):
        os.remove(output)
        
    for i in range(number_words):
        if output != 'none':
            save_word(top_words[i][0], output)
        else:
            print(top_words[i][0])

        mutation(top_words[i][0])
        

def find_url(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        print(re.findall(r'*/$', str(link.get('href'))))
        urls.append(link.get('href'))

    return urls

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--output', '-o', default='none', help='Output file to print to instead of the console.')
@click.option('--depth', '-d',  default='1', help='Grab not only words also URLs on the webpage(s), and add them to a list of number of pages to crawl next (default=1).')
def main(url, length, output, depth):

    if depth != 'none':
        urls = find_url(url)

    for all_urls in urls:
        url=all_urls
        print(all_urls)
        the_words = get_all_words_from(url)
        top_words = get_top_words_from(the_words, length)

        number_words=max_num_words(10, top_words)
        output_words(output, number_words, top_words)


if __name__ == '__main__':
    main()
