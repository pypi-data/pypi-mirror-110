""" Data display method """
from dataclasses import dataclass, field


@dataclass
class NewsItemDisplay:
    """
    Class defines the news item display method

        Methods:
        print_news_item(self) - prints news item in stdout
    """

    feed_title: str = ""
    title: str = ""
    summary: str = ""
    date: str = ""
    link: str = ""
    source: str = ""
    image_links: list = field(default_factory=list)

    def print_news_item(self):
        print('-----------------------'+ '\n')
        print("Feed title: " + self.feed_title + '\n',
              "News title: " + self.title + '\n',
              "Summary: " + self.summary + '\n',
              "Publication date: " + self.date + '\n',
              "Source: " + self.source + '\n',
              "Link: " + self.link + '\n',
              sep='\n')

        if self.image_links:
            print("Images links: ")
            for num, img_link in enumerate(self.image_links):
                if img_link:
                    print(f"[{num+1}] {img_link}")
