# import pandas as pd
# import tablib
# from flask import Flask, render_template
#
# app = Flask(__name__)
# dataset = tablib.Dataset()
#
# dataset.csv = pd.read_csv('./output.csv')
# table = pd.read_csv('./output.csv')
#
#
# @app.route("/")
# def index():
#     # data = dataset
#     # return dataset.html
#     # return render_template('index.html', data=data)
#     # data = list(dataset.csv.values.flatten())
#     table_html = table.to_html()
#     return render_template('index.html', data=table_html)
#
#
# if __name__ == "__main__":
#     app.run()

import pandas as pd
import tablib
from flask import Flask, render_template
from flask import session
import csv
import os

import bs4 as bs
import urllib3


def webscrape():
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
    # print(parentDiv)

    # childDiv = parentDiv.find("div", {"class": "table-responsive"})
    table = parentDiv.find('table')
    # print(table)

    # populating table data as list
    table_rows = table.find_all('tr')
    # print(table_rows)
    output_rows = []
    row_count = 0
    headers = ["S. No."
        , "Name of State / UT"
        , "Total Confirmed cases"
        , "Cured/Discharged"
        , "Death"]

    # transform table data for CSV file
    state = []
    affected = []
    cured = []
    death = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text
                   .replace('\n', '')
                   .replace('#', '')
                   .replace('Union Territory of ', '')
                   .replace(' *', '')
                   .replace('number of confirmed cases in India', 'cases') for i in td]
        print(row, len(row))
        if (len(row) == 5):
            state.append(row[1])
            affected.append(row[2])
            cured.append(row[3])
            death.append(row[4])
        if len(row) < 5:
            continue
        if len(row) == 5:
            row.insert(0, str(row_count + 1))
        output_rows.append(row)
        row_count += 1
    print(state)
    length = len(state)
    session['length'] = length
    session['state'] = state
    session['affected'] = affected
    session['cured']= cured
    session['death'] = death
    # write table data to CSV
    with open(FILEPATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(output_rows)

    print("Data received ...")
    return length


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# dataset = tablib.Dataset()
#
# dataset.csv = pd.read_csv('./output.csv')
# table = pd.read_csv('./output.csv')


@app.route("/")
def index():
    # data = dataset
    # return dataset.html
    # return render_template('index.html', data=data)
    # data = list(dataset.csv.values.flatten())

    # table_html = table.to_html()
    table_html = "Corono Information"
    return render_template('index.html', data=table_html)
@app.route("/table")
def table():
    length = webscrape()
    return render_template('table.html', **locals())
@app.route("/bar")
def bar():
    length = webscrape()
    return render_template('bar.html',max=17000,**locals())

if __name__ == "__main__":
    app.debug=True
    app.run()
