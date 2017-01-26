from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurant_database import Base, Restaurant, MenuItem 

engine = create_engine('sqlite:///restaurant_menutracker.db')
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurant = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurant=restaurant)

@app.route('/restaurant/new/',methods=['GET','POST'])
def newRestaurant():
	if request.method=='POST':
		newrestaurant = Restaurant(name=request.form['name'], city=request.form['city'])
		session.add(newrestaurant)
		session.commit()
		flash("New Restaurant added!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/delete/',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	restauranttodelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restauranttodelete)
		session.commit()
		return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
		return render_template('deleterestaurant.html', restaurant=restauranttodelete)



@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return render_template('menu.html', items=items, restaurant=restaurant) 


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method=='POST':
		addeditem=MenuItem(name=request.form['name'], review=request.form['review'], price=request.form['price'], restaurant_id=restaurant_id)
		session.add(addeditem)
		session.commit()
		return redirect(url_for('showMenu',restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
	return render_template('newmenuitem.html',restaurant=restaurant)
       
@app.route('/restaurant/restaurant_id/menu/menu_id/edit')
def editMenuitem():
	return render_template('editmenuitem.html', item=item) 

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuitem(restaurant_id, menu_id):
	itemdelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method=='POST':
		session.delete(itemdelete)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', item=itemdelete)
	

if __name__=='__main__':
	app.secret_key='super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000 )









