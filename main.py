# build_dist.py

from bs4 import BeautifulSoup
from pathlib import Path
import base64

entryFile = input("Entry File? leave it empty in case of index.html \n")


def getPath(relativePath):
    print("Merging -> "+relativePath)
    return "."+relativePath


if(entryFile == ""):
    entryFile = "index.html"

original_html_text = Path(entryFile).read_text(encoding="utf-8")
soup = BeautifulSoup(original_html_text, features="html.parser")


def rightFile(url):
    substring = ".png"
    if substring in url:
        return False
    else:
        return True


def isLocal(url):
    substring = "http"
    if substring in url:
        return False
    else:
        return True


def allowMerge(url):
    if((isLocal(url) == True) and (rightFile(url) == True)):
        return True
    else:
        return False


# Find link tags. example: <link rel="stylesheet" href="css/somestyle.css">
for tag in soup.find_all('link', rel="stylesheet"):
    if tag.has_attr('href'):
        if(allowMerge(tag['href']) == True):
            file_text = Path(getPath(tag['href'])).read_text(encoding="utf-8")

            # remove the tag from soup
            tag.extract()

            # insert style element
            new_style = soup.new_tag('style')
            new_style.string = file_text
            soup.html.head.append(new_style)


# Find script tags. example: <script src="js/somescript.js"></script>
for tag in soup.find_all('script', src=True):
    if tag.has_attr('src'):
        if(allowMerge(tag['src']) == True):
            file_text = Path(getPath(tag['src'])).read_text()

            # remove the tag from soup
            tag.extract()

            # insert script element
            new_script = soup.new_tag('script')
            new_script.string = "\n"+file_text.replace("</", "<\/")
            soup.html.body.append(new_script)


# Save onefile
with open("./dist/index.html", "w", encoding="utf-8") as outfile:
    outfile.write(str(soup))

print("success. Output file: ./dist/index.html")
