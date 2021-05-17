from bs4 import BeautifulSoup
import requests
import xlsxwriter

html_text = requests.get("https://www.georgebrown.ca/program-finder?year=2021")
soup = BeautifulSoup(html_text.text, "lxml")
print(f"Status code is: {html_text.status_code}")
print("")

workbook = xlsxwriter.Workbook("test.xlsx")
worksheet = workbook.add_worksheet("George Brown")
cell_format = workbook.add_format()
cell_format.set_text_wrap()
cell_format.set_align("center")
cell_format.set_align("vcenter")
worksheet.write("A1", "School Name")
worksheet.write("B1", "Course Name")
worksheet.write("C1", "Credential Name")
worksheet.write("D1", "Duration")
worksheet.write("E1", "International?")
worksheet.write("F1", "Overview")
worksheet.write("G1", "Link")
worksheet.set_column("A:C", 30, cell_format)
worksheet.set_column("F:G", 68, cell_format)

row = 0

for name in soup.find_all("table", class_ = "views-table views-view-table cols-7 program-finder-table"):
    for title in name.find_all("span", class_ = "field field--name-title field--type-string field--label-hidden"):
        for programName in name.find_all("a", class_ = "program-title-link"):
            credential = name.find("td", class_ = "views-field views-field-field-credential").text
            international = name.find("span", class_ = "intern-availability").text
            duration = name.find("div", class_ = "program-overview-content duration").text.replace("Duration:", "")
            overview = name.find("div", class_ = "program-overview-content overview").text
            titleName = title.get_text()
            programNameName = programName.get_text()
            finalLink = f"https://www.georgebrown.ca/{programName.get('href')}"
            worksheet.write(row+1, 0, titleName, cell_format)
            worksheet.write(row+1, 1, programNameName, cell_format)
            worksheet.write(row+1, 2, credential.strip(), cell_format)
            worksheet.write(row+1, 3, duration, cell_format)
            worksheet.write(row+1, 4, international, cell_format)
            worksheet.write(row+1, 5, overview, cell_format)
            worksheet.write(row+1, 6, finalLink, cell_format)
            row += 1

            # print(f"{title.get_text()} - {programName.get_text()} - {credential.strip()} - {international} - {duration} - https://www.georgebrown.ca/{programName.get('href')}")


workbook.close()
