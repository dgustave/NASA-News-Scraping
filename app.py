# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
from Missions_to_Mars import scrape_mars
import os



# Create an instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
app.config['MONGO_DBNAME'] = 'mars_app'
mongo = PyMongo(app)
print ("MongoDB Database:", mongo.db)


# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 
    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
    # Run scrapped functions
    mars_dict = mongo.db.mars_dict
    scrape_all = scrape_mars.run()
    # scrape_news = scrape_mars.scrape_news()
    # scrape_news = scrape_mars.scrape_featured() 
    # scrape_table = scrape_mars.scrape_table()
    # scrape_hemisphere = scrape_mars.scrape_hemisphere()
    mars_dict.update({}, scrape_all, upsert = True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
