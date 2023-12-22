from flask import Flask, jsonify
from scraper import Scrape,initilize_driver  # Import the Scrape function
global driver
global action

driver, action = initilize_driver()

app = Flask(__name__)


# Route to trigger the scraping and return JSON
@app.route('/scrape', methods=['GET'])
def scrape_and_return_json():
    global driver, action
    data,driver,action = Scrape(driver,action)  
    return jsonify(data)  


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False,host='0.0.0.0', port=8000)
