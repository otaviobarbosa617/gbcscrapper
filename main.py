from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://www.georgebrown.ca/program-finder?year=2021").text
soup = BeautifulSoup(html_text, "lxml")

allPrograms = soup.find("div", id = "block-program-finder-content")
school = allPrograms.find("span", class_ = "field field--name-title field--type-string field--label-hidden").text
program = allPrograms.find("a", class_ = "program-title-link").text
credential = allPrograms.find("td", class_ = "views-field views-field-field-credential").text
international = allPrograms.find("span", class_ = "intern-availability").text

print(f"Program name is {program}, the credential is {credential.strip()}. Accepts international students? {international}")