import requests
from bs4 import BeautifulSoup


class Parser:
    SITE = "https://www.smashingmagazine.com/category/wallpapers"

    def parse(self, month, year, size):
        page_url = self.format_url(month, year)
        page_content = self.get_url(page_url)
        image_links = self.grab_all_links(size, page_content)
        self.save_files(image_links)

    def get_url(self, url):
        return requests.get(url)

    def format_url(self, month, year):
        month_list = ("january", "february", "march", "april", "may",
                      "june", "july", "august", "september", "october",
                      "november", "december")
        url = f"{self.SITE}/{year}/{month_list.index(month)}/"
        url += f"desktop-wallpaper-calendars-{month}-{year}/"
        return url

    def grab_all_links(self, size, html):
        links = {}
        soup = BeautifulSoup(html, 'html.parser')
        for ul in soup.find_all('ul'):
            for li in ul.find_all('li'):
                content = li.contents
                if content[0] == 'without calendar: ':
                    for a_tag in content:
                        if a_tag.contents[0] == size:
                            title = a_tag['title']
                            link = a_tag['href']
                            links['title'] = link
        return links

    def save_files(self, links):
        for title, link in links.values():
            title += '.png'
            with open(title, 'wb') as f:
                image = self.get_url(link)
                f.write(image.content)
