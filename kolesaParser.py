from typing import List, Tuple, Any
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from pip._internal.network.utils import HEADERS
from tqdm import trange
from models import Car


def get_html(url: str) -> str:
    """Принимает URL-адрес в качестве аргумента запроса,
    возвращает html-страницу из запроса.
    Uses `get()` method from `requests` package
    Args:
        url ([str]): link to the website
    Returns:
        [str]: HTML page from the request
    """
    response = requests.get(url, headers=HEADERS)
    html = response.text
    return html


def pages_count(html: str) -> int:
        """Определение количества страниц в каталоге объявления
        Args:
            html (str): The page to search in which
            the value of the last page is being searched
        Returns:
            int: Last page value
        """
        soup = BeautifulSoup(html, "lxml")
        paginator = soup.find("div", {"class": "pager"}).find_all("li")
        if paginator:
            last_page = int(paginator[-1].text.strip())
        else:
            last_page = 1
        return last_page

class MyParser:
    BASE_URL = "https://kolesa.kz/cars/"
    LINK = ""
    HEADERS = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/97.0.4692.99 Safari/537.36",
    }
    allPrice = []

    def __init__(self, LINK):
        self.LINK = self.BASE_URL + LINK



    def gather_valuable_data(self, advert: Tag) -> Car:
        # все виды топлива указываемые в объявлении
        fuels = ("бензин", "дизель", "газ-бензин", "газ", "гибрид", "электричество")
        # название техники, берем всегда только первые три слова из названия
        vehicle_mark = " ".join(
            advert.find("span", {"class": "a-el-info-title"}).text.split()[:3]
        )
        price = int("".join(advert.find("span", {"class": "price"}).text.split()[:-1]))
        link = self.BASE_URL[:-6]
        link += advert.find("a", {"class": "list-link ddl_product_link"}).get('href')
        self.allPrice.append(price)
        description = (
            advert.find("div", {"class": "a-search-description"})
                .text.strip()
                .split(",")[:6]
        )
        year = description[0].strip()
        fuel_type = ""
        for target in description[1:]:
            if target.strip() in fuels:
                fuel_type = target.strip()

        car = Car(
            vehicle_mark,
            year,
            price,
            link,
            fuel_type,
        )
        return car

    def collect_data(self, adverts: ResultSet) -> List:
        """Сбор всех блоков с объявлениями со страницы
        Args:
            adverts (ResultSet): результат поиска блока с объявлениями
        Returns:
            List: список из объявлении
        """
        collection = []
        for ad in adverts:
            try:
                data = self.gather_valuable_data(ad)
                collection.append(data)
            except AttributeError:
                continue
            except IndexError:
                continue
        return collection

    def getCars(self):
        last_page = pages_count(get_html(self.LINK))
        data_collection = []
        for i in trange(1, last_page + 1, desc="Progress"):
            html = get_html(f"{self.LINK}?page={i}")
            soup = BeautifulSoup(html, "lxml")
            ads_list = soup.find_all("div", {"class": "a-elem"})
            data = self.collect_data(ads_list)
            data_collection.extend(data)
        sum = 0
        for price in self.allPrice:
            sum += price
        return data_collection

    def getSortCars(self):
        data_collection = []
        html = get_html(f"{self.LINK}?page={1}")
        soup = BeautifulSoup(html, "lxml")
        ads_list = soup.find_all("div", {"class": "a-elem"})
        data = self.collect_data(ads_list)
        data_collection.extend(data)
        sum = 0
        return data_collection


    def Top10(self, cars):
        self.LINK = self.LINK + "?auto-custom=2&sort_by=price-asc&year[from]=2000&year[to]=2000"
        cars = self.getSortCars()
        cars = cars[:10]
        return cars





