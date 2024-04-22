# app.py
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db = SQLAlchemy(app)

# Define SQLAlchemy model for rooms
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, unique=True)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(200))

# Wrap database creation in an application context
with app.app_context():
    # Create the database tables
    db.create_all()

    # Check if rooms exist in the database, if not, add them
    if not Room.query.all():
        default_rooms = [
            {'room_number': 401, 'image_url': 'https://media.istockphoto.com/id/1390233984/photo/modern-luxury-bedroom.jpg?s=612x612&w=0&k=20&c=po91poqYoQTbHUpO1LD1HcxCFZVpRG-loAMWZT7YRe4=', 'description': 'Modern Luxury Bedroom'},
            {'room_number': 405, 'image_url': 'https://media.istockphoto.com/id/1334009789/photo/luxurious-living-room-interior-at-night-with-sofa-christmas-tree-and-gift-boxes.jpg?s=612x612&w=0&k=20&c=XHdeb70eSD2c2PW7Y0pHRyEZvYyuTBDDwuv5eic7qI0=', 'description': 'Luxurious Bedroom Interior'},
            {'room_number': 408, 'image_url': 'https://media.istockphoto.com/id/1361555489/photo/modern-luxury-beautiful-interior-with-panoramic-windows-and-winter-view-design-bedroom-with.jpg?s=612x612&w=0&k=20&c=xyozz9kTJ2v5Jq6iY3Mnd6MgOyR6t8QH1KSj033M_J8=', 'description': 'Modern luxury beautiful interior with panoramic windows'}
        ]

        for room_data in default_rooms:
            room = Room(**room_data)
            db.session.add(room)

        db.session.commit()

@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('home.html', rooms=rooms)

@app.route('/room/<int:room_id>')
def room_details(room_id):
    room = Room.query.get(room_id)
    return render_template('room_details.html', room=room)

@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room_route(room_id):
    if request.method == 'POST':
        # Here you can add the logic to book the room
        # For example, you might update the database to mark the room as booked
        return redirect(url_for('room_booked', room_id=room_id))
    else:
        room = Room.query.get(room_id)
        return render_template('room_details.html', room=room)

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        image_url = request.form['image_url']
        description = request.form['description']
        new_room = Room(room_number=room_number, image_url=image_url, description=description)
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add_room.html')

if __name__ == '__main__':
    app.run(debug=True)
