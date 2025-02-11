import asyncio
from typing import Optional
from urllib.parse import quote

from domain.additional_property_model import AdditionalPropertyModel
from domain.component_model import ComponentModel
import aiohttp
import bs4

from domain.cosmetic_property_model import CosmeticPropertyModel
from domain.danger_factor_model import DangerFactorModel
from domain.danger_factor_type import DangerFactorType
from domain.decimal_model import DecimalModel
from domain.input_percentage_model import InputPercentageModel
from domain.naturalness_type import NaturalnessType


class CosmobaseComponentService:
    def __init__(self):
        self.__session = None

    async def init(self) -> None:
        self.__session = aiohttp.ClientSession(base_url="https://cosmobase.ru/")

    async def shutdown(self) -> None:
        await self.__session.close()

    async def find_component(self, title: str) -> None:
        links = await self.__find_possible_component_links(title)

        result = []

        async def f(link: str) -> None:
            c = await self.__parse_component(link)
            title_lower = title.lower()
            print(c.latin_title, c.traditional_title, c.inci_title)

            if c.inci_title.lower() == title_lower or c.traditional_title.lower() == title_lower or c.latin_title.lower() == title_lower:
                result.append(c)

        async with asyncio.TaskGroup() as tg:
            for l in links:
                tg.create_task(f(l))

        print(result)

    async def __find_possible_component_links(self, search: str) -> list[str]:
        encoded = quote(search)

        headers = {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9",
            # "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "origin": "https://cosmobase.ru",
            # "priority": "u=1, i",
            # "referer": "https://cosmobase.ru/handbook",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.704 YaBrowser/24.12.1.704 (beta) Yowser/2.5 Safari/537.36",
            #"x-requested-with": "XMLHttpRequest"
        }

        data = f"hbSearch={encoded}&hbGroup=0&hlbFrom=&hlbTo=&factor=&hbEffects=0&hbSkin=0&hbNatural=false&lookDesc=false&start=0&searchType=standart"

        response: aiohttp.ClientResponse = await self.__session.post(url="handbook/search", headers=headers, data=data)

        response_json = await response.json(content_type="text/html; charset=utf-8")

        if response_json["status"] != "success":
            raise Exception("УВА")

        response_html = response_json["data"]

        soup = bs4.BeautifulSoup(response_html, "html.parser")

        links = list(map(lambda i: i.attrs.get("href"),
                    soup.select("a.componentLink")))

        return links

    async def __parse_component(self, uri: str) -> ComponentModel:
        response = await self.__session.get(url=uri)
        return self.parse(await response.text(), uri)

    def parse_titles(self, soup: bs4.BeautifulSoup) -> tuple[str, str, str]:
        # Add exceptions handling
        tags: bs4.ResultSet = soup.select("div.componentName")
        return tags[0].text, tags[1].text, tags[2].text

    def parse_categories(self, soup: bs4.BeautifulSoup) -> list[str]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "категориям" in tag.text
        )
        has_categories: bool = label_tag is not None

        if not has_categories:
            return []

        categories: list[str] = []
        categories_tag: bs4.Tag = label_tag.find_next("div")

        for t in categories_tag.find_all("div"):
            categories.append(t.text)

        return categories


    def parse_cosmetic_properties(self, soup: bs4.BeautifulSoup) -> list[CosmeticPropertyModel]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Косметические" in tag.text
        )
        has_cosmetic_properties: bool = label_tag is not None

        if not has_cosmetic_properties:
            return []

        cosmetic_properties: list[CosmeticPropertyModel] = []
        cosmetic_properties_tag: bs4.Tag = label_tag.find_next("div")

        for t in cosmetic_properties_tag.find_all("div"):
            property_title_tag: bs4.Tag = t.select_one("span.itemLabel")
            property_value_tag: bs4.Tag = t.select_one("span.itemValue")

            cosmetic_properties.append(
                CosmeticPropertyModel(
                    title=property_title_tag.text,
                    value=property_value_tag.text,
                )
            )

        return cosmetic_properties


    def parse_additional_properties(self,
            soup: bs4.BeautifulSoup,
    ) -> list[AdditionalPropertyModel]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Дополнительные" in tag.text
        )
        has_additional_properties: bool = label_tag is not None

        if not has_additional_properties:
            return []

        additional_properties: list[AdditionalPropertyModel] = []
        additional_properties_tag: bs4.Tag = label_tag.find_next("div")

        for t in additional_properties_tag.find_all("div"):
            property_title_tag: bs4.Tag = t.select_one("span.itemLabel")
            property_value_tag: bs4.Tag = t.select_one("span.itemValue")

            additional_properties.append(
                AdditionalPropertyModel(
                    title=property_title_tag.text,
                    value=property_value_tag.text,
                )
            )

        return additional_properties


    def parse_aliases(self, soup: bs4.BeautifulSoup) -> list[str]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Синонимы" in tag.text
        )
        has_aliases: bool = label_tag is not None

        if not has_aliases:
            return []

        aliases: list[str] = []
        aliases_tag: bs4.Tag = label_tag.find_next("div")

        for t in aliases_tag.find_all("div"):
            aliases.append(t.text)

        return aliases


    def parse_skin_types(self, soup: bs4.BeautifulSoup) -> list[str]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Эффективен для типов кожи" in tag.text
        )
        has_skin_types: bool = label_tag is not None

        if not has_skin_types:
            return []

        skin_types: list[str] = []
        skin_types_tag: bs4.Tag = label_tag.find_next("div")

        for t in skin_types_tag.find_all("div"):
            skin_types.append(t.text)

        return skin_types


    def parse_recommended_input_percentage(
            self,
            soup: bs4.BeautifulSoup,
    ) -> Optional[InputPercentageModel]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Рекомендуемый процент ввода" in tag.text
        )
        has_recommended_input_percentage: bool = label_tag is not None

        if not has_recommended_input_percentage:
            return None

        from_tag: bs4.Tag = label_tag.find_previous("div", {"class": "rounded"})
        to_tag: bs4.Tag = label_tag.find_next("div", {"class": "rounded"})

        return InputPercentageModel(
            low=DecimalModel(from_tag.text),
            high=DecimalModel(to_tag.text),
        )


    def parse_hlb_value(self, soup: bs4.BeautifulSoup) -> Optional[float]:
        # Add exceptions handling

        hlb_tag: Optional[bs4.Tag] = soup.select_one("span.hlbCircle")
        return float(hlb_tag.text) if hlb_tag is not None else None


    def parse_danger_factor_type(self, description: str) -> DangerFactorType:
        if description.lower() == "низкий":
            return DangerFactorType.LOW

        if description.lower() == "средний":
            return DangerFactorType.MEDIUM

        return DangerFactorType.HIGH


    def parse_danger_factor(self, soup: bs4.BeautifulSoup) -> Optional[DangerFactorModel]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Фактор опасности" in tag.text
        )
        has_danger_factor: bool = label_tag is not None

        if not has_danger_factor:
            return None

        danger_factor_tag: bs4.Tag = label_tag.find_next("div")
        danger_factor_tag_text: str = danger_factor_tag.text

        danger_factor_value: str = danger_factor_tag.find("span").text
        description_index_start: int = danger_factor_tag_text.find(danger_factor_value) + 1
        danger_factor_description = danger_factor_tag_text[description_index_start:]

        return DangerFactorModel(
            value=danger_factor_value,
            type=self.parse_danger_factor_type(danger_factor_description),
        )


    def parse_naturalness(self, soup: bs4.BeautifulSoup) -> Optional[NaturalnessType]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Натуральность" in tag.text
        )
        has_naturalness: bool = label_tag is not None

        if not has_naturalness:
            return None

        naturalness_tag: bs4.Tag = label_tag.find_next("span")
        naturalness_value: str = naturalness_tag.text

        return (
            NaturalnessType.SYNTHETIC
            if naturalness_value == "Синтетический"
            else NaturalnessType.NATURAL
        )


    def parse_comment(self, soup: bs4.BeautifulSoup) -> Optional[str]:
        # Add exceptions handling

        label_tag: Optional[bs4.Tag] = soup.find(
            lambda tag: tag.name == "label" and "Комментарий безопасности" in tag.text
        )
        has_comment: bool = label_tag is not None

        if not has_comment:
            return None

        return label_tag.find_next("div").text.strip()


    def parse(self, content: str, url: str) -> ComponentModel:
        # Add exceptions handling

        soup = bs4.BeautifulSoup(content, "html.parser")

        with open("out.html", "w") as f:
            f.write(content)

        traditional_title, latin_title, inci_title = self.parse_titles(soup)

        return ComponentModel(
            traditional_title=traditional_title,
            latin_title=latin_title,
            inci_title=inci_title,
            url=url,
            categories=self.parse_categories(soup),
            cosmetic_properties=self.parse_cosmetic_properties(soup),
            additional_properties=self.parse_additional_properties(soup),
            aliases=self.parse_aliases(soup),
            skin_types=self.parse_skin_types(soup),
            recommended_input_percentage=self.parse_recommended_input_percentage(soup),
            danger_factor=self.parse_danger_factor(soup),
            naturalness=self.parse_naturalness(soup),
            hlb_value=self.parse_hlb_value(soup),
            comment=self.parse_comment(soup),
        )

async def main() -> None:
    s = CosmobaseComponentService()
    await s.init()
    await s.find_component("Вода")
    await s.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
