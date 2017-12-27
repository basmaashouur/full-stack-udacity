from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


app.route('/')
@app.route('/catlog/')
def showcatlog():
	return "This the catlog page"


@app.route('/catlog/new/')
def addCategory():
	return "Here you can add a new catogry"

###############################################################################


@app.route('/catlog/<int:category_id>/')
def showCategory(category_id):
	return "Here is that catogry name"


@app.route('/catlog/<int:category_id>/items/')
def showItems(category_id):
	return "This is all the items of that catogryname"


@app.route('/catlog/<int:category_id>/edit/')
def editCategory(category_id):
	return "Here yo can edit catogry name"


@app.route('/catlog/<int:category_id>/delete/')
def deleteCategory(category_id):
	return "Here yo can delete catogry name"


###############################################################################


@app.route('/catlog/<int:category_id>/items/newitem/')
def addItem(category_id):
	return "Here you can add a new item"


@app.route('/catlog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
	return "this is an item of that catogryname"


@app.route('/catlog/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
	return "Here you can edit that item name"



@app.route('/catlog/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
	return "Here you can delete that item name"



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
