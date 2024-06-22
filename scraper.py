from typing import DefaultDict, List, Tuple
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
import logging
from animal import Animal
from logger import get_logger
from collections import defaultdict


logger = get_logger("scraper", logging.WARNING)


async def parse_animal_page(page_content: str, animal: Animal):
    try:
        soup = BeautifulSoup(page_content, "html.parser")
        source = soup.find("a", class_="mw-file-description")        
        await animal.save_picture(source.find("img")["src"])
    except Exception as e:
        logger.error(f"Exception raise on {e}", exc_info=True)


def parse_main_page(page_content: str, arrange_by: str) -> DefaultDict[str, List[Animal]]:
    data_list = defaultdict(list)
    try:
        soup = BeautifulSoup(page_content, "html.parser")

        table = soup.find("table", class_="wikitable sortable sticky-header")

        if not table:
            raise ValueError("Table not found on the page.")
        
        ths = table.find_all("th")
        arrange_by_index = __extract_arrange_by_index(arrange_by, ths)
        trs = table.find_all("tr")
        first_animal_index = __find_index_of_first_animal(trs)
        for i in range(first_animal_index, len(trs)-1):
            tds = trs[i].find_all('td')
            if not tds:
                continue
            link, name, arrange_by_name = __get_properties(tds, arrange_by_index)
            data_list[arrange_by_name].append(Animal(name, link))

        return data_list
            
    except Exception as e:
        logger.error(f"Error occurred while parsing page: {e}.", exc_info=True)
        raise


def __extract_arrange_by_index(arrange_by, ths: ResultSet) -> int:
    for i, th in enumerate(ths):
        if arrange_by in th.string.lower():
            return i            
    raise ValueError(f"{arrange_by=} not found in table")
    

def __get_properties(tds: Tag, arrange_by_id) -> Tuple[str, str, str]:
    a = tds[0].find("a")
    link = a["href"]
    name = a["title"]
    arrange_by = tds[arrange_by_id].get_text(strip=True)
    return link, name, arrange_by


def __find_index_of_first_animal(trs: ResultSet) -> int:
    for i, tr in enumerate(trs):
        if tr.find("td"):
            return i
    raise ValueError("Cannot find first animal.")




    