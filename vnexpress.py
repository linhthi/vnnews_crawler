from bs4 import BeautifulSoup
import requests
import csv
import argparse
import tqdm

def get_urls_of_type(article_type: str, total_pages: int = 1) -> list[str]:
    """
    Get urls of articles in specific type 
    @param article_type (str): type of articles to get urls
    @param total_pages (int): number of pages to get urls
    @return articles_urls (list(str)): list of urls
    """
    articles_urls = list()
    for i in tqdm.tqdm(range(1, total_pages+1)):
        content = requests.get(f"https://vnexpress.net/{article_type}-p{i}").content
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all(class_="title-news")

        if (len(titles) == 0):
            # print(f"Couldn't find any news in the category {article_type} on page {i}")
            continue

        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))

    return articles_urls

def main(category, page):
    if category == "all":
        categories = ["giao-duc", "khoa-hoc", "the-thao", "kinh-doanh", "suc-khoe", "the-gioi", "giai-tri", "du-lich", "so-hoa", "thoi-su", "phap-luat"]
    else:
        categories = [category]

    for category in categories:
        urls = get_urls_of_type(category, page)

        # Fetch content of articles
        articles = []
        for link in urls:
            article_page = BeautifulSoup(requests.get(link).content, 'html.parser')
            article_id = article_page.find('meta', {"name": 'its_id'})['content']
            article_author = article_page.find('meta', {"name": 'its_author'})['content']
            article_wordcount = article_page.find('meta', {"name": 'its_wordcount'})['content']
            article_updatetime = article_page.find('meta', {"name": 'article_updatetime'})['content']
            articel_publication = article_page.find('meta', {"name": 'its_publication'})['content']
            article_title = article_page.find('meta', {"name": 'its_title'})['content']
            article_tags = article_page.find('meta', {"name": 'its_tag'})['content']
            article_content = ""
            article_contents = article_page.find_all('p', class_="Normal")
            for content in article_contents:
                article_content = article_content + " " + content.get_text()

            article = {
                "id": article_id,
                "title": article_title,
                "url: link,
                "author": article_author,
                "updatetime": article_updatetime,
                "wordcount": article_wordcount,
                "publication": articel_publication,
                "tags": article_tags,
                "content": article_content
            }
            articles.append(article)

        print(f"Number of articles downloaded from {category}: {len(articles)}")
        # Save data to a CSV file
        with open(f'./dataset_vnexpress/{category}_page{page}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "author", "updatetime", "wordcount", "publication", "tags", "content"])
            writer.writeheader()
            writer.writerows(articles)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape articles from VnExpress.net')
    parser.add_argument('-c', '--category', type=str, default="all", help="Category of articles to scrape. Available options: giao-duc, khoa-hoc, the-thao, kinh-doanh, suc-khoe, the-gioi, giai-tri, du-lich, so-hoa, thoi-su, phap-luat")
    parser.add_argument('-p', '--page', type=int, default=1, help="Number of pages to scrape")
    args = parser.parse_args()

    main(args.category, args.page)
