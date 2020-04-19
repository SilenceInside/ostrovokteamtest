import argparse
import re
import requests
from bs4 import BeautifulSoup


class Parser:
    SITE = "https://www.smashingmagazine.com"
    ALL_WALLPAPERS = "https://www.smashingmagazine.com/category/wallpapers"

    def parse(self, month, year, resolution):
        page_url = self.format_url(month, year)
        page_content = self.get_url(page_url)
        image_links = self.grab_all_links(resolution, page_content)
        self.save_files(image_links)

    def get_url(self, url):
        return requests.get(url)

    def format_url(self, month, year):
        month = month.lower()
        month_list = ("january", "february", "march", "april", "may",
                      "june", "july", "august", "september", "october",
                      "november", "december")
        url = f"{self.SITE}/{year}/{month_list.index(month):02d}/" \
              f"desktop-wallpaper-calendars-{month}-{year}/"
        return url

    def grab_all_links(self, resolution, html):
        links = {}
        soup = BeautifulSoup(html.text, 'html.parser')
        for li in soup.find_all(text=re.compile('without calendar: ')):
            tag = li.parent.find(text=re.compile(resolution))
            if tag:
                tp = tag.parent
                link = str(tag.parent['href'])
                file_extension = link[-4:]
                name = str(tag.parent['title']) + file_extension
                links[name] = link
        return links

    def save_files(self, links):
        for title in links.keys():
            with open(title, 'wb') as f:
                image = self.get_url(links[title])
                f.write(image.content)


if __name__ == '__main__':
    app_description = """Download wallpaper from 
    https://www.smashingmagazine.com in current directory which published
    at chosen month year with preferred resolution"""
    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument('month', help='name of month in English',
                        choices=["january", "february", "march", "april",
                                 "may", "june", "july", "august",
                                 "september", "october", "november",
                                 "december"])
    parser.add_argument('year', type=int, help='year of publication')
    parser.add_argument('resolution', type=str, help='image resolution',
                        choices=['800x480', '1024x768', '1280x720',
                                 '1280x1024', ' 1600x1050', '1400x1050',
                                 '1600x1200', '1920x1200', '2560x1440',
                                 '3475x4633'])
    args = parser.parse_args()
    img_parser = Parser()
    img_parser.parse(month=args.month, year=args.year, resolution=args.resolution)
