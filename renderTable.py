import pandas as pd
import tablib
from flask import Flask, render_template

app = Flask(__name__)
dataset = tablib.Dataset()

dataset.csv = pd.read_csv('./output.csv')
table = pd.read_csv('./output.csv')


@app.route("/")
def index():
    # data = dataset
    # return dataset.html
    # return render_template('index.html', data=data)
    # data = list(dataset.csv.values.flatten())
    table_html = table.to_html()
    return render_template('index.html', data=table_html)


if __name__ == "__main__":
    app.run()
