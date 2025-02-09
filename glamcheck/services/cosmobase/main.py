from typing import Optional
from urllib.parse import quote

import bs4
import requests

from glamcheck.models.composition.domain.additional_property import (
    AdditionalPropertyModel,
)
from glamcheck.models.composition.domain.component import ComponentModel
from glamcheck.models.composition.domain.cosmetic_property import CosmeticPropertyModel
from glamcheck.models.composition.domain.danger_factor import DangerFactorModel
from glamcheck.models.composition.domain.danger_factor_type import DangerFactorType
from glamcheck.models.composition.domain.input_percentage import InputPercentageModel
from glamcheck.models.composition.domain.naturalness import NaturalnessType


def parse_titles(soup: bs4.BeautifulSoup) -> tuple[str, str, str]:
    # Add exceptions handling
    tags: bs4.ResultSet = soup.select("div.componentName")
    return tags[0].text, tags[1].text, tags[2].text


def parse_categories(soup: bs4.BeautifulSoup) -> list[str]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "категориям" in tag.text
    )
    has_categories: bool = label_tag is not None

    if not has_categories:
        return []

    categories: list[str] = []
    categories_tag: bs4.Tag = label_tag.findNext("div")

    for t in categories_tag.findAll("div"):
        categories.append(t.text)

    return categories


def parse_cosmetic_properties(soup: bs4.BeautifulSoup) -> list[CosmeticPropertyModel]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Косметические" in tag.text
    )
    has_cosmetic_properties: bool = label_tag is not None

    if not has_cosmetic_properties:
        return []

    cosmetic_properties: list[CosmeticPropertyModel] = []
    cosmetic_properties_tag: bs4.Tag = label_tag.findNext("div")

    for t in cosmetic_properties_tag.findAll("div"):
        property_title_tag: bs4.Tag = t.select_one("span.itemLabel")
        property_value_tag: bs4.Tag = t.select_one("span.itemValue")

        cosmetic_properties.append(
            CosmeticPropertyModel(
                title=property_title_tag.text,
                value=property_value_tag.text,
            )
        )

    return cosmetic_properties


def parse_additional_properties(
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
    additional_properties_tag: bs4.Tag = label_tag.findNext("div")

    for t in additional_properties_tag.findAll("div"):
        property_title_tag: bs4.Tag = t.select_one("span.itemLabel")
        property_value_tag: bs4.Tag = t.select_one("span.itemValue")

        additional_properties.append(
            AdditionalPropertyModel(
                title=property_title_tag.text,
                value=property_value_tag.text,
            )
        )

    return additional_properties


def parse_aliases(soup: bs4.BeautifulSoup) -> list[str]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Синонимы" in tag.text
    )
    has_aliases: bool = label_tag is not None

    if not has_aliases:
        return []

    aliases: list[str] = []
    aliases_tag: bs4.Tag = label_tag.findNext("div")

    for t in aliases_tag.findAll("div"):
        aliases.append(t.text)

    return aliases


def parse_skin_types(soup: bs4.BeautifulSoup) -> list[str]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Эффективен для типов кожи" in tag.text
    )
    has_skin_types: bool = label_tag is not None

    if not has_skin_types:
        return []

    skin_types: list[str] = []
    skin_types_tag: bs4.Tag = label_tag.findNext("div")

    for t in skin_types_tag.findAll("div"):
        skin_types.append(t.text)

    return skin_types


def parse_recommended_input_percentage(
    soup: bs4.BeautifulSoup,
) -> Optional[InputPercentageModel]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Рекомендуемый процент ввода" in tag.text
    )
    has_recommended_input_percentage: bool = label_tag is not None

    if not has_recommended_input_percentage:
        return None

    from_tag: bs4.Tag = label_tag.findPrevious("div", {"class": "rounded"})
    to_tag: bs4.Tag = label_tag.findNext("div", {"class": "rounded"})

    return InputPercentageModel(
        from_=from_tag.text,
        to_=to_tag.text,
    )


def parse_hlb_value(soup: bs4.BeautifulSoup) -> Optional[float]:
    # Add exceptions handling

    hlb_tag: Optional[bs4.Tag] = soup.select_one("span.hlbCircle")
    return float(hlb_tag.text) if hlb_tag is not None else None


def parse_danger_factor_type(description: str) -> DangerFactorType:
    if description.lower() == "низкий":
        return DangerFactorType.LOW

    if description.lower() == "средний":
        return DangerFactorType.MEDIUM

    return DangerFactorType.HIGH


def parse_danger_factor(soup: bs4.BeautifulSoup) -> Optional[DangerFactorModel]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Фактор опасности" in tag.text
    )
    has_danger_factor: bool = label_tag is not None

    if not has_danger_factor:
        return None

    danger_factor_tag: bs4.Tag = label_tag.findNext("div")
    danger_factor_tag_text: str = danger_factor_tag.text

    danger_factor_value: str = danger_factor_tag.find("span").text
    description_index_start: int = danger_factor_tag_text.find(danger_factor_value) + 1
    danger_factor_description = danger_factor_tag_text[description_index_start:]

    return DangerFactorModel(
        value=danger_factor_value,
        type=parse_danger_factor_type(danger_factor_description),
    )


def parse_naturalness(soup: bs4.BeautifulSoup) -> Optional[NaturalnessType]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Натуральность" in tag.text
    )
    has_naturalness: bool = label_tag is not None

    if not has_naturalness:
        return None

    naturalness_tag: bs4.Tag = label_tag.findNext("span")
    naturalness_value: str = naturalness_tag.text

    return (
        NaturalnessType.SYNTHETIC
        if naturalness_value == "Синтетический"
        else NaturalnessType.NATURAL
    )


def parse_comment(soup: bs4.BeautifulSoup) -> Optional[str]:
    # Add exceptions handling

    label_tag: Optional[bs4.Tag] = soup.find(
        lambda tag: tag.name == "label" and "Комментарий безопасности" in tag.text
    )
    has_comment: bool = label_tag is not None

    if not has_comment:
        return None

    return label_tag.findNext("div").text.strip()


def parse(content: str, url: str) -> ComponentModel:
    # Add exceptions handling

    soup = bs4.BeautifulSoup(content, "html.parser")

    traditional_title, latin_title, inci_title = parse_titles(soup)

    return ComponentModel(
        traditional_title=traditional_title,
        latin_title=latin_title,
        inci_title=inci_title,
        url=url,
        categories=parse_categories(soup),
        cosmetic_properties=parse_cosmetic_properties(soup),
        additional_properties=parse_additional_properties(soup),
        aliases=parse_aliases(soup),
        skin_types=parse_skin_types(soup),
        recommended_input_percentage=parse_recommended_input_percentage(soup),
        danger_factor=parse_danger_factor(soup),
        naturalness=parse_naturalness(soup),
        hlb_value=parse_hlb_value(soup),
        comment=parse_comment(soup),
    )


title = "Ин"
encoded = quote(title)

headers = {
    "authority": "cosmobase.ru",
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://cosmobase.ru",
    "referer": "https://cosmobase.ru/handbook",
    "sec-ch-ua": '"Chromium";v="118", "YaBrowser";v="23", "Not=A?Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.971 "
    "YaBrowser/23.11.3.971 (beta) Yowser/2.5 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

data = f"hbSearch={encoded}&hbGroup=0&hlbFrom=&hlbTo=&factor=&hbEffects=0&hbSkin=0&hbNatural=false&lookDesc=false&start=0&searchType=standart"

url1 = "https://cosmobase.ru/handbook/search"

response = requests.post(url1, headers=headers, data=data)

response_json = response.json()

if response_json["status"] != "success":
    print('Status is not "success"')
else:
    response_data = response_json["data"]
    soup1 = bs4.BeautifulSoup(response_data, "html.parser")
    result = soup1.select("a.componentLink")

    uris = []

    for i in result:
        uris.append(i.attrs.get("href"))

    for uri in uris:
        current_url = f"https://cosmobase.ru/{uri}"
        current_response = requests.get(current_url)
        print(parse(current_response.text, current_url))
        print()
