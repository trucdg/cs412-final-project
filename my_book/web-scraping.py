import requests  # HTTP get/post

from bs4 import BeautifulSoup  # HTML parser/tree/search

# start w this url
url = "https://www.si.com/nfl/scoreboard"

page = requests.get(url)

# use BeautifulSoup to tokenize this page
# soup = BeautifulSoup(page.content, "html.parser")

# # examine the webpage in the browser (inspect)
# table = soup.find("div", attrs={"class": "tiles wider"})

# # think of each store as a row in the table:
# rows = table.findAll("a")

# # go through each store:
# for row in rows:
#     # extract the name and address
#     name = row.find("span", attrs={"class": "name"}).text
print(page)
