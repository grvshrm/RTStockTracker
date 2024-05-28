from flask import Flask
import pandas as pd

bbgapp = Flask(__name__)
amzn_data = pd.read_csv("AMZN_Data.csv")
msft_data = pd.read_csv("MSFT_Data.csv")
tsla_data = pd.read_csv("TSLA_Data.csv")

@bbgapp.route("/getdata/", methods = ["GET", "POST"])
def index():
    print("Stock API called")
    data = {
    "AMZN": amzn_data.sample(1).to_dict(orient = "records")[0],
    "MSFT": msft_data.sample(1).to_dict(orient = "records")[0],
    "TSLA": tsla_data.sample(1).to_dict(orient = "records")[0]
    }
    return data

if __name__ == "__main__":
    bbgapp.run(debug = True, port = 4000)