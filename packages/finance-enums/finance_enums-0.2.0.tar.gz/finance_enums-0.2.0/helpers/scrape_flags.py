import httpx
from bs4 import BeautifulSoup

resp = httpx.get("https://en.wikipedia.org/wiki/ISO_3166-1")
soup = BeautifulSoup(resp.text)
data = soup.find_all("table")[1]
rows = data.find_all("tr")[1:]

for row in rows:
    try:
        name = f"flags/{row.find_all('span')[1].text}.png"
        resp = httpx.get(f'https:{row.find("img").attrs["src"]}')
        with open(name, "wb") as fp:
            fp.write(resp.read())
    except:
        with open(name + "_not_found.txt", "w"):
            ...

# strip extra data
# for item in `ls`; do convert $item -strip $item; done
