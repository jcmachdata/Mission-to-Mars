#Mars app
# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Create connection variable
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mission_to_mars'

# Pass connection to the pymongo instance.
mongo = PyMongo(app)

#define home route to initiate index page
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#define route to call scraping function
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)
    

if __name__ == "__main__":
    app.run(debug=True)