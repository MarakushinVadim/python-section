import datetime
from datetime import date

from bs4 import BeautifulSoup


def parse_page_links(html: str, start_date: date, end_date: date, url: str):
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    def validity_check(link_href: str) -> bool:
        return "/upload/reports/oil_xls/oil_xls_" in link_href and link_href.endswith(".xls")

    for link in links:
        href = link.get("href")
        if href:
            href = href.split("?")[0]
            if validity_check(href):
                try:
                    file_date = datetime.datetime.strptime(href.split("oil_xls_")[1][:8], "%Y%m%d").date()
                    if start_date <= file_date <= end_date:
                        u = href if href.startswith("http") else f"https://spimex.com{href}"
                        results.append((u, file_date))
                    else:
                        print(f"Ссылка {href} вне диапазона дат")
                except Exception as e:
                    print(f"Не удалось извлечь дату из ссылки {href}: {e}")
    return results
