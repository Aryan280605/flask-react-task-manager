from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    comments = db.relationship('Comment', backref='task', cascade="all, delete-orphan")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)

# Simple route to test
@app.route('/')
def home():
    return {"message": "It works!"}



from flask import request, jsonify

# 1. Add comment
@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    comment = Comment(task_id=task_id, content=content)
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment added", "id": comment.id}), 201


# 2. Edit comment
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    comment.content = content
    db.session.commit()

    return jsonify({"message": "Comment updated"}), 200


# 3. Delete comment
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        data = request.get_json()
        # Do something with data
        return jsonify(data), 201
    else:
        # Return the list of tasks
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)