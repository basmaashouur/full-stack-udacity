from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catlogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catlog/')
def showCatlog():
    return render_template("catlog.html", category=session.query(Category).all())


@app.route('/catlog/new/', methods=['GET', 'POST'])
def addCategory():
    if request.method == 'POST':
        newcate = Category(title=request.form['title'])
        session.add(newcate)
        session.commit()
        return redirect("/catlog/")
    else:
        return render_template('newcategory.html')
###############################################################################


@app.route('/catlog/<int:category_id>/')
def showCategory(category_id):
	return render_template('category.html', category=session.query(Category).filter_by(id=category_id).one())


@app.route('/catlog/<int:category_id>/items/')
def showItems(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	items = session.query(Item).filter_by(category_id=category_id).all()
	return render_template('items.html', category=category, items=items)


@app.route('/catlog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if request.method == 'POST':
    	editcate = session.query(Category).filter_by(id=category_id).one()
    	editcate.title = request.form['title'] 
        session.add(editcate)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editcategory.html',category_id=category_id)


@app.route('/catlog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
	return "delete items"


###############################################################################


@app.route('/catlog/<int:category_id>/newitem/')
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
