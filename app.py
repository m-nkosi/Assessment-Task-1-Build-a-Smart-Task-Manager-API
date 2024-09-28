from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Date
from datetime import date


app = Flask(__name__)

# ------------------------------- Data Model ----------------------------------

## Create Database
class Base(DeclarativeBase):
    pass

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# Create the extention
db = SQLAlchemy(model_class=Base)
# initial the app with the extention
db.init_app(app)


# Create table
class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1500))
    due_date: Mapped[date] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[str] = mapped_column(String(6), nullable=True, default='once')
    recurrence: Mapped[str] = mapped_column(String(7), default="once")

    def to_dict(self):
        """returns the object's attributes as a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description":self.description,
            "due_date": self.due_date,
            "completed": self.completed,
            "periority": self.priority,
            "recurrence": self.recurrence
        }
    
    def __repr__(self):
        return f"<Task {self.title}>"

# Create a table schema
with app.app_context():
    db.create_all()


#--------------------End-points--------------------------------------------
def str_to_date(string) -> date:
    """convert a string with format YYYY-MM-DD into date object"""
    date_data = string.split('-')
    date_data = list(map(int, date_data))
    return date(date_data[0], date_data[1], date_data[2])

@app.route("/tasks", methods=["POST"])
def post_new_task():
    try:

        new_task = Task(
            title=request.form.get("title"),
            description=request.form.get("description"),
            due_date=str_to_date(request.form.get("due date"))
        )
        db.session.add(new_task)
        db.session.commit()
    except:
        # this code block will run if useer provided invalid body
        return jsonify(response={"Bad Request": "make sure you provide all reuqired key, value arguements as star=ted in documentation"}), 400
    return jsonify(response={"Success": "A new task has been added"}), 200



@app.route("/tasks")
def get_all_tasks():
    result = db.session.execute(db.select(Task).order_by(Task.id))
    tasks = result.scalars().all()
    return [task.to_dict() for task in tasks]


@app.route("/tasks/<int:_id>")
def get_task_by_id(_id):
    result = db.get_or_404(Task,_id, description={"adhgsjd"})
    return jsonify(task=result.to_dict()), 200


@app.route("/tasks/<int:_id>", methods=["PUT"])
def update_task(_id):
    task = db.get_or_404(Task, _id, description="task with that id not found")
    try:
        task.title = request.form.get('title')
        task.description = request.form.get("description")
        task.due_date = str_to_date(request.form.get("due date"))
        db.session.commit()
    except:
        # this will run if the user inserted invalid key, value argument
        return jsonify(response={"Bad Request": "make sure you provide all reuqired key, value arguements as stated in documentation"}), 400

    # this code block will run only if update was success
    return jsonify(response={"Success": "Successfully updated the details."}), 200 