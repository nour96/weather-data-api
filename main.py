from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    
    temperature = df.loc[df["    DATE"]==date]["   TG"].squeeze() / 10
    # squeeze : to remove the index from the series we get, so we only get the temperature 
    
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }
    
@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    # orient = records:: Give me a list of dictionaries, where each row in the dataframe
    # becomes one dictionary (a record)
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    # we removed parse_date cuz we want python to read date as an integer, not as a date, then we can
    # convert it into string
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    
    return result
    
    

if __name__ == "__main__":
    app.run(debug=True)