from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Date
from transformers import pipeline
from datetime import date, datetime, timedelta

GEN = pipeline("fill-mask")
app = Flask(__name__)
# ------------------------------- Data Models ----------------------------------

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
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1500))
    due_date: Mapped[date] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[str] = mapped_column(String(6), nullable=True, default='high')
    recurrence: Mapped[str] = mapped_column(String(7), default="once")

    # ************** Parent relationship *****************#
    # "parent_task" refers to the parent_task property in TaskTrackers
    task_trackers = relationship("TaskTracker", back_populates="parent_task", cascade="all, delete") 

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


class TaskTracker(db.Model):
    __tablename__ = "task_trackers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[date] = mapped_column(Date, default=date(datetime.now().year,datetime.now().month, datetime.now().day))
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    #**************** Child relationship ***********************
    # "tasks.id" the tasks refers to the tablename of Task
    # "task_trackers" refers to the task_trackers porperty in the Task Class
    task_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("tasks.id"))
    parent_task = relationship("Task", back_populates="task_trackers")
    def to_dict(self):
        return {
            "start-date": self.start_date,
            "end-date": self.end_date,
            "parent-task": self.task_id
        }

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
    task_tracker = TaskTracker(task_id=new_task.id)
    db.session.add(task_tracker)
    db.session.commit()
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

 
@app.route("/tasks/<int:_id>", methods=["DELETE"])
def delete_task(_id):
    task = db.get_or_404(Task,_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200


#----------------------------------------- AI End-points -------------------------------------------------------
@app.route("/tasks/suggest", methods=["POST"])
def get_task_suggestion():
    text = request.form.get("user-input") + "<mask>"
    return jsonify(response=GEN(text))

@app.route("/tasks/<int:_id>/predict-due-date", methods=["POST"])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
def predict_due_date(_id):
    # get all the tasktracker with due date in the past
    result = db.get_or_404(Task, _id)
    task_trackers = result.task_trackers
    if task_trackers:
        # get the number of days in between start -date and end-date and put in a list
        number_difference = [(task_tracker.end_date - task_tracker.start_date).days for task_tracker in task_trackers if task_tracker.end_date]
        # get calulate the average, add the average number of days to today
        average = sum(number_difference) // len(number_difference)
        print(average)
        today = datetime.now()
        future_in_correct_format = date(today.year, today.month, today.day)  + timedelta(days=average)
        print(future_in_correct_format)
        return jsonify(reponse={"days":str(future_in_correct_format)}), 200
    else:
        return jsonify(response={"error": "No element with that id in the databse"}), 400   
    #return that day as json                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                