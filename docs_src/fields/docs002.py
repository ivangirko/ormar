import databases
import sqlalchemy

import ormar

database = databases.Database("sqlite:///db.sqlite")
metadata = sqlalchemy.MetaData()


class Department(ormar.Model):
    __database__ = database
    __metadata__ = metadata

    id = ormar.Integer(primary_key=True)
    name = ormar.String(length=100)


class Course(ormar.Model):
    __database__ = database
    __metadata__ = metadata

    id = ormar.Integer(primary_key=True)
    name = ormar.String(length=100)
    completed = ormar.Boolean(default=False)
    department = ormar.ForeignKey(Department, related_name="my_courses")

department = Department(name='Science')
course = Course(name='Math', completed=False, department=department)

print(department.my_courses[0])
# Will produce:
# Course(id=None,
#        name='Math',
#        completed=False,
#        department=Department(id=None, name='Science'))
