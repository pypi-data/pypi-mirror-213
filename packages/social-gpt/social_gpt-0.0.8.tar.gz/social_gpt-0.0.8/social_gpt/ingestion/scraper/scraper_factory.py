from social_scraper import SocialScraper
from youtube_scraper import YoutubeScraper


class ScraperFactory:
    @staticmethod
    def get_scraper(social_media, username) -> SocialScraper:
        if social_media == "youtube":
            return YoutubeScraper(username)
