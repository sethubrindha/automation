from constants import CREDENTIALS, INSTAGRAM_PASSWORD, PAGE_LIST
import os, sys, random
from instascrapper import InstaScrapper


def main():
    page_index = int(sys.argv[1])
    user_name = CREDENTIALS[page_index]['user_name']
    directory = os.path.join(os.path.dirname(__file__), 'downloads')

    scrapper = InstaScrapper(user_name, INSTAGRAM_PASSWORD, directory, random.choice(PAGE_LIST))
    scrapper.Ingester()


if __name__ == "__main__":
    main()
