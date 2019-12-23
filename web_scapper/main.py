import argparse
import logging
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

# Internal imports
import news_page_objects as news
from common import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r"^https?://.+/.+$")  # https://conexe.co/hello
is_root_path = re.compile(r"^/.+$")  # /hello


def _news_scraper(news_site_uid):
    host = config()["news_sites"][news_site_uid]["url"]

    logger.info(f"Beginning scraper for {host}")
    logger.info('Finding links in homepage...')

    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info("¡¡¡Yei, Article fetched!!!")
            articles.append(article)
            print(article.title)

    print(len(articles))


def _fetch_article(news_site_uid, host, link):

    logger.info(f"Start fetching article at {link}")

    article = None

    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warn("Error While fetching the article", exc_info=False)

    if article and not article.body:
        logger.warn("Invalid article, There is no body.")
        return None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f"{host}{link}"
    else:
        return f"{host}/{link}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    news_site_choises = list(config()["news_sites"].keys())
    parser.add_argument(
        "news_site",
        help="The news site that you want to scrape",
        type=str,
        choices=news_site_choises,
    )

    args = parser.parse_args()
    _news_scraper(args.news_site)
