import csv
import os

import bs4 as bs
import urllib3

# constants go here
URL = 'https://www.mohfw.gov.in/'
FILEPATH = './output.csv'

try:
    os.remove(FILEPATH)
    print("File deleted successfully...")
except:
    print("Error while deleting file ", FILEPATH)

# connect to the website
http = urllib3.PoolManager()
source = http.request('GET', url=URL).data
soup = bs.BeautifulSoup(source, 'html.parser')
# print(soup)

# parse table locating div
# parentDiv = soup.find("div", {"class": "content-newtab"})
parentDiv = soup.find("div", {"class": "data-table table-responsive"})
#
print(parentDiv)

# childDiv = parentDiv.find("div", {"class": "table-responsive"})
table = parentDiv.find('table')
print(table)

# populating table data as list
table_rows = table.find_all('tr')
output_rows = []
row_count = 0
headers = ["S. No."
    , "Name of State / UT"
    , "Total Confirmed cases"
    , "Cured/Discharged"
    , "Death"]

# transform table data for CSV file
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text
               .replace('\n', '')
               .replace('#', '')
               .replace('Union Territory of ', '')
               .replace(' *', '')
               .replace('number of confirmed cases in India', 'cases') for i in td]
    print(row, len(row))
    if len(row) < 5:
        continue
    if len(row) == 5:
        row.insert(0, str(row_count + 1))
    output_rows.append(row)
    row_count += 1

# write table data to CSV
with open(FILEPATH, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(output_rows)

print("Data received ...")
