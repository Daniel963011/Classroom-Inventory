from flask import Flask, render_template, request, redirect, url_for
from models import db, InventoryItem

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    items = InventoryItem.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        category = request.form['category']
        location = request.form['location']
        
        new_item = InventoryItem(name=name, quantity=quantity, category=category, location=location)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = int(request.form['quantity'])
        item.category = request.form['category']
        item.location = request.form['location']
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:item_id>', methods = ['GET', 'POST'])
def delete_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('delete_item.html', item=item)


if __name__ == "__main__":
    app.run(debug=True)