from flask import Flask, render_template
from scrape_nint import collect_game_data

app = Flask(__name__)

@app.route('/')
def scrape():
    my_data = collect_game_data()
    return render_template("scraped_nint.html", data=my_data)

if __name__ == "__main__":
    app.run(debug=True, port=4000)