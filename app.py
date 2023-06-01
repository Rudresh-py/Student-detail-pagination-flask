from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    grade = db.Column(db.String(10))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade
        }


# @app.route('/students', methods=['GET'])
# def get_students():
#     page = int(request.args.get('page', 1))
#     # page_size = int(request.args.get('page_size', 10))
#     page_size = 10
#     # Query the database to retrieve paginated students
#     students = Student.query.paginate(page=page, per_page=page_size)
#
#     return render_template('students.html', students=students.items, page=students.page, total_pages=students.pages, page_size=page_size)

#
@app.route('/students', methods=['GET'])
def get_students():

    page = int(request.args.get('page', 1))
    # page_size = int(request.args.get('page_size', 10))
    page_size = 10
    search_query = request.args.get('search', '')

    # Query the database to retrieve paginated students
    if search_query:
        students = Student.query.filter(Student.name.ilike(f'%{search_query}%')).paginate(page=page, per_page=page_size)
    else:
        students = Student.query.paginate(page=page, per_page=page_size)

    # Prepare the response data
    response_data = [student.to_dict() for student in students.items]
    response = {
        'page': students.page,
        'total_pages': students.pages,
        'total_records': students.total,
        'students': response_data
    }

    return render_template('students.html', students=response['students'], total_pages=response['total_pages'],
                           total_records=response['total_records'], page=response['page'],
                           )


if __name__ == '__main__':
    app.run(debug=True)


# from flask import render_template
#
# @app.route('/students', methods=['GET'])
# def get_students():
#     page = int(request.args.get('page', 1))
#     page_size = int(request.args.get('page_size', 10))
#
#     # Query the database to retrieve paginated students
#     students = Student.query.paginate(page=page, per_page=page_size)
#
#     return render_template('students.html', students=students.items, page=students.page, total_pages=students.pages, page_size=page_size)
