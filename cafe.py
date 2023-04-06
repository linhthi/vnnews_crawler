from bs4 import BeautifulSoup
import requests
import csv
import argparse
import tqdm

url = "https://cafef.vn/"

cat_id = {
    "xa-hoi": "188112"
}

def get_urls_of_type(article_type: str, total_pages: int = 1) -> list[str]:
    """
    Get urls of articles in specific type 
    @param article_type (str): type of articles to get urls
    @param total_pages (int): number of pages to get urls
    @return articles_urls (list(str)): list of urls
    """
    articles_urls = list()
    for i in tqdm.tqdm(range(1, total_pages+1)):
        content = requests.get(f"https://cafef.vn/timelinelist/188112/{i}.chn").content
        print(str(content)[:100], len(content))
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all("h3")

        if (len(titles) == 0):
            # print(f"Couldn't find any news in the category {article_type} on page {i}")
            continue
        print(len(titles), titles[0])
        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))

    return articles_urls

def main(category, page, output_folder):
    if category == "all":
        categories = ["xa-hoi",]
    else:
        categories = [category]

    for category in categories:
        urls = get_urls_of_type(category, page)
        print(urls)

        # Fetch content of articles
        articles = []
        for link in urls:
            article_page = BeautifulSoup(requests.get(url+link).content, 'html.parser')
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
                print(content.text)
                print(content.get_text())
                exit(0)
            
            article = {
                "id": article_id,
                "title": article_title,
                "url": link,
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
        with open(f'{output_folder}/{category}_page{page}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "url", "author", "updatetime", "wordcount", "publication", "tags", "content"])
            writer.writeheader()
            writer.writerows(articles)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape articles from VnExpress.net')
    parser.add_argument('-c', '--category', type=str, default="all", help="Category of articles to scrape. Available options: giao-duc, khoa-hoc, the-thao, kinh-doanh, suc-khoe, the-gioi, giai-tri, du-lich, so-hoa, thoi-su, phap-luat")
    parser.add_argument('-p', '--page', type=int, default=1, help="Number of pages to scrape")
    parser.add_argument('-o', '--output', type=str, default="./dataset_vnexpress", help="Output folder to store the scraped data")
    args = parser.parse_args()

    main(args.category, args.page, args.output)
