# VnNews crawler
This is a Python script for crawling articles from the VnExpress news website and saving them to CSV files. You can specify the category of articles and the number of pages to crawl using command-line arguments.

## Installation
Clone this repository to your local machine:
```
git clone https://github.com/your_username/vnexpress-crawler.git
```
Install the required dependencies by running the following command in the terminal:
```
pip install -r requirements.txt
```
## Usage
You can run the script using the following command in the terminal:
```
python scrape_vnexpress.py -c <category> -p <pages> -o <output_folder>
```
Replace category with the category of articles you want to crawl (e.g. giao-duc, khoa-hoc, the-thao, kinh-doanh, suc-khoe, the-gioi, giai-tri, du-lich, so-hoa, thoi-su, phap-luat, or all for all categories), and page with the number of pages you want to crawl (default is 1).

For example, to crawl all articles from the giao-duc category on the first 2 pages, run the following command:

```
python scrape_vnexpress.py -c giao-duc -p 2 -o data_vnexpress
```
The script will create a directory named dataset_vnexpress in the current directory and save the crawled articles to CSV files inside this directory, with each file named category_pageX.csv, where category is the name of the category and X is the page number.

## Output format
The CSV files contain the following fields for each article:

- id: the unique ID of the article
- title: the title of the article
- url: url of the article
- author: the author of the article
- updatetime: the date and time when the article was last updated
- wordcount: the word count of the article
- publication: the name of the publication that the article belongs to
- tags: the tags associated with the article
- content: the content of the article
## License
This script is released under the [MIT License](https://opensource.org/licenses/MIT).
