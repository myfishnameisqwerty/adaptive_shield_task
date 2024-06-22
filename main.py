import argparse
import asyncio
import logging
import os
import shutil
import sys
from typing import DefaultDict, List
from to_html import create_html
from animal import Animal
from requester import fetch
from logger import get_logger
import scraper


logger = get_logger("main", logging.WARNING)


ARRANGE_BY = "collateral adjective"
WIKI = "https://en.wikipedia.org"
MAIN_PAGE = "/wiki/List_of_animal_names"
BATCH = 30


async def add_image(animal: Animal):
    animal_page = await fetch(WIKI+animal.link)
    await scraper.parse_animal_page(animal_page, animal)


async def save_animal_imgs(results: DefaultDict[str, List[Animal]]):
    tasks = []
    for arranged_animals in results.values():
        for animal in arranged_animals:
            tasks.append(add_image(animal))
            if len(tasks) > BATCH:
                await asyncio.gather(*tasks)
                tasks = []
    if tasks:    
        await asyncio.gather(*tasks)


def print_animals(results: DefaultDict[str, List[Animal]]):
    for key, animals in results.items():
            print(key+":")
            for animal in animals:
                print(f"{animal.name} - {animal.picture_local_link}")


async def run(args: argparse.Namespace) -> None:
    page = await fetch(WIKI+MAIN_PAGE)
    if not page:
        logger.error(f"Error on fetching {WIKI+MAIN_PAGE}")
        sys.exit(1)
    results = scraper.parse_main_page(page, args.arrange_by)
    await save_animal_imgs(results)
    print_animals(results)
    create_html(results, "output.html")
    sys.exit(0)

    
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrange-by", type=str, default=ARRANGE_BY)
    args = parser.parse_args()
    init_tmp()
    asyncio.run(run(args))
    

def init_tmp() -> None:
    try:
        tmp_dir = "tmp"
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)
        
    except Exception as e:
        logger.error(f"Exception {e} raised during tmp directory initialization.")
        sys.exit(1)
        

if __name__ == "__main__":
    main()

