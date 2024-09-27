from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Date
from datetime import date

app = Flask(__name__)

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
class Tasks(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1500))
    due_date: Mapped[date] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[str] = mapped_column(String(6))
    recurrence: Mapped[str] = mapped_column(String(7))

    def __repr__(self):
        return f"<Task {self.title}>"

# Create a table schema
with app.app_context():
    db.create_all()
