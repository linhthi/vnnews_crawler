from bs4 import BeautifulSoup
import requests
import csv
import argparse
import tqdm

def get_urls_of_type(article_type: str) -> list[str]:
    """
    Get urls of articles in specific type 
    @param article_type (str): type of articles to get urls
    @return articles_urls (list(str)): list of urls
    """
    articles_urls = list()
    content = requests.get(f"https://thanhnien.vn/{article_type}").content
    soup = BeautifulSoup(content, "html.parser")
    titles = soup.find_all(class_="box-title-text")

    if (len(titles) == 0):
        print(f"Couldn't find any news in the category {article_type}")

    for title in titles:
        link = title.find_all("a")[0]
        articles_urls.append(link.get("href"))

    return articles_urls

def main(category, output_folder):
    if category == "all":
        categories = [
            "thoi-su",
            "the-gioi",
            "kinh-te",
            "doi-song",
            "suc-khoe",
            "gioi-tre",
            "tieu-dung-thong-minh",
            "giao-duc", 
            "du-lich",
            "van-hoa",
            "giai-tri",
            "the-thao",
            "cong-nghe-game",
            "xe",
            "thoi-trang-tre",
        ]
    else:
        categories = [category]

    for category in categories:
        urls = get_urls_of_type(category)

        # Fetch content of articles
        articles = []
        for link in urls:
            link_ = "https://thanhnien.vn{0}".format(link)
            print(link_)
            article_page = BeautifulSoup(requests.get(link_).content, 'html.parser')
            article_title = article_page.find('title').get_text()
            tags = article_page.find('meta', {"name": 'keywords'})
            if tags:
                article_tags = tags.get('content')
            else:
                article_tags = None
            
            article_url = article_page.find('meta', {'property': 'og:url'})['content']
            author_tag = article_page.find('meta', {'property': 'dable:author'}) or article_page.find('meta', {'name': 'author'})
            if author_tag:
                article_author = author_tag.get('content')
            else:
                article_author = None
            published_time = article_page.find('meta', {'property': 'article:published_time'})
            if published_time:
                article_published_time = published_time.get('content')
            else:
                article_published_time = None 
            article_content = ""
            article_contents = article_page.find_all('p')
            for content in article_contents:
                article_content = article_content + " " + content.get_text()

            article = {
                "url": article_url,
                "title": article_title,
                "author": article_author,
                "published_time": article_published_time,
                "tags": article_tags,
                "content": article_content
            }
            articles.append(article)

        print(f"Number of articles downloaded from {category}: {len(articles)}")
        # Save data to a CSV file
        with open(f'{output_folder}/{category}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["url", "title", "author", "published_time", "tags", "content"])
            writer.writeheader()
            writer.writerows(articles)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape articles from VnExpress.net')
    parser.add_argument('-c', '--category', type=str, default="all", help="Category of articles to scrape. Available options: giao-duc, khoa-hoc, the-thao, kinh-doanh, suc-khoe, the-gioi, giai-tri, du-lich, so-hoa, thoi-su, phap-luat")
    parser.add_argument('-o', '--output', type=str, default="./dataset_thanhnien", help="Output folder to store the scraped data")
    args = parser.parse_args()

    main(args.category, args.output)
