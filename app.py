from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from logger import setup_logger

app = Flask(__name__)
logger = setup_logger()
# for deploy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@postgres-service:5432/your_database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@postgres-service:5432/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Note %r>' % self.id

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET'])
def index():
    logger.info("Page accessed")
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        data = request.get_json()
        content = data.get('content')
        if content:
            note = Note(content=content)
            db.session.add(note)
            db.session.commit()
            logger.info('Note created successfully')
            return jsonify({'message': 'Note created successfully', 'id': note.id, 'content': note.content}), 201
        else:
            logger.error('Content cannot be empty')
            return jsonify({'error': 'Content cannot be empty'}), 400
    else:
        notes = Note.query.all()
        notes_list = [{'id': note.id, 'content': note.content} for note in notes]
        logger.info('Notes fetched successfully')
        return jsonify(notes_list)

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        logger.info(f'Note {note_id} deleted successfully')
        return jsonify({'message': 'Note deleted successfully'}), 200
    else:
        logger.error(f'Note {note_id} not found')
        return jsonify({'error': 'Note not found'}), 404

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0')