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
    category = session.query(Category).all()
    return render_template("catlog.html", category=category)


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
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('category.html', category=category)


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
        return render_template('editcategory.html', category_id=category_id)


@app.route('/catlog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if request.method == 'POST':
        delcate = session.query(Category).filter_by(id=category_id).one()
        session.delete(delcate)
        session.commit()
        return redirect("/catlog/")
    else:
        return render_template('deletecategory.html', category_id=category_id)


###############################################################################


@app.route('/catlog/<int:category_id>/newitem/', methods=['GET', 'POST'])
def addItem(category_id):
    if request.method == 'POST':
        newitem = Item(title=request.form['title'], description=request.form['description'], img=request.form['img'],
                       category_id=category_id)
        session.add(newitem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


@app.route('/catlog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template("item.html", item=item)


@app.route('/catlog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if request.method == 'POST':
        edititem = session.query(Item).filter_by(id=item_id).one()
        if request.form['title']:
            edititem.title = request.form['title']
        if request.form['description']:
            edititem.description = request.form['description']
        if request.form['img']:
            edititem.img = request.form['img']
        session.add(edititem)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id))
    else:
        return render_template("edititem.html", category_id=category_id, item_id=item_id)


@app.route('/catlog/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id, methods=['GET', 'POST']):
    if request.method == 'POST':
        delitem = session.query(Item).filter_by(id=item_id).one()
        session.delete(delitem)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id))
    else:
        return render_template('deleteitem.html', category_id=category_id, item_id=item_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
