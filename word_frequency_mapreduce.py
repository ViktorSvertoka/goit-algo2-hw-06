import requests
import re
import multiprocessing
import matplotlib.pyplot as plt
from collections import Counter
from colorama import Fore, Style, init

init(autoreset=True)


def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def tokenize(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return words


def mapper(word):
    return (word, 1)


def reducer(counts):
    counter = Counter()
    for word, count in counts:
        counter[word] += count
    return counter


def map_reduce(text, num_workers=4):
    words = tokenize(text)
    with multiprocessing.Pool(num_workers) as pool:
        mapped = pool.map(mapper, words)
    return reducer(mapped)


def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color="skyblue")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Top Words by Frequency")
    plt.xticks(rotation=45)
    plt.show()


def print_top_words(word_counts, top_n=10):
    print(Fore.CYAN + Style.BRIGHT + "Top Words by Frequency:\n")
    for i, (word, count) in enumerate(word_counts.most_common(top_n), 1):
        print(Fore.YELLOW + f"{i}. {word}: " + Fore.GREEN + f"{count}")


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    text = fetch_text(url)
    word_counts = map_reduce(text)
    print_top_words(word_counts)
    visualize_top_words(word_counts)
