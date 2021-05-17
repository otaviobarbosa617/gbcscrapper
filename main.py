from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://www.georgebrown.ca/program-finder?year=2021").text
soup = BeautifulSoup(html_text, "lxml")

for name in soup.find_all("table", class_ = "views-table views-view-table cols-7 program-finder-table"):
    for title in name.find_all("span", class_ = "field field--name-title field--type-string field--label-hidden"):
        for programName in name.find_all("a", class_ = "program-title-link"):
            credential = name.find("td", class_ = "views-field views-field-field-credential").text
            international = name.find("span", class_ = "intern-availability").text
            duration = name.find("div", class_ = "program-overview-content duration").text.replace("Duration:", "")
            print(f"{title.get_text()} - {programName.get_text()} - {credential.strip()} - {international} - {duration}")