#George Brown College - 2021-2022 Program Finder - Scrapper
#Made by Otavio Barbosa - May,2021

#Imports
from bs4 import BeautifulSoup
import requests
import xlsxwriter #as I'm saving in a XLSX file this module is important

#Declarations
schoolNameGroup = []
programNameGroup = []
internationalGroup = []
finalLinkGroup = []
programCredentialGroup = []
overviewGroup = []
durationGroup = []

#Basic Soup Function
def getData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') #makes no real difference which parser you're going to use
    return soup
        
#This function "finds" the program block and then every table in it.
#If the program is not in any table the function will not show it.
def getCourses(soup):
    school = soup.find("div", id = "block-program-finder-content")
    for schools in school.find_all("table", class_ = "views-table views-view-table cols-7 program-finder-table"):
        schoolName = schools.h3.span.text
        for programsData in schools.find_all("tbody"):
            for programRow in programsData.find_all("tr", class_ = "program-row"):
                programName = programRow.a.text
                international = programRow.find("span", class_ = "intern-availability").text
                finalLink = f"https://www.georgebrown.ca/{programRow.a.get('href')}" #As GBC uses drupal, their original url is node/number
                for programCredentialData in programRow.find_all("td", class_ = "views-field views-field-field-credential"):
                    programCredential = programCredentialData.text.strip()
                    #lots of appends to the declared lists
                    schoolNameGroup.append(schoolName)
                    programNameGroup.append(programName)
                    programCredentialGroup.append(programCredential)
                    internationalGroup.append(international)
                    finalLinkGroup.append(finalLink)
            for overviewRow in programsData.find_all("tr", class_ = "program-overview"): #a new for loop just for the overview and the duration. They're hard-coded on the page but only visible using JS dropdown
                overview = overviewRow.find("div", class_ = "program-overview-content overview").text.strip()
                duration = overviewRow.find("div", class_ = "program-overview-content duration").text.replace("Duration:", "")
                overviewGroup.append(overview)
                durationGroup.append(duration)

#This function creates the excel file and then saves it.
def writeExcel():
    row = 0
    workbook = xlsxwriter.Workbook("GBC2021Programs.xlsx")
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

    #This loop grabs the items from their original list and insert on the cell by row and column.
    for i in range(len(schoolNameGroup)):
        worksheet.write(row, 0, schoolNameGroup[i], cell_format)
        worksheet.write(row+1, 1, programNameGroup[i], cell_format)
        worksheet.write(row+1, 2, programCredentialGroup[i], cell_format)
        worksheet.write(row+1, 3, durationGroup[i], cell_format)
        worksheet.write(row+1, 4, internationalGroup[i], cell_format)
        worksheet.write(row+1, 5, overviewGroup[i], cell_format)
        worksheet.write(row+1, 6, finalLinkGroup[i], cell_format)
        row += 1

    workbook.close()

#I've decided to call page by page using their number instead of using BS4 pagination
#It starts from 0 till page 4 or to regular person 1 to 5
#Every call makes a soup of the content, finds the programs, and then writes them in the Excel file.
for i in range (0, 4):
    url=f"https://www.georgebrown.ca/program-finder?year=2021&search=&page={i}"
    soup = getData(url)
    getCourses(soup)
    writeExcel()