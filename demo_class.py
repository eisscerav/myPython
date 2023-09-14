class Person:
    def __init__(self, name='', age=0):
        self.name = name
        self.age = age

    def show(self):
        print(f"Hello {self.name} you are {self.age} years old\n")


class Student(Person):
    def __init__(self, name, age, grade=0):
        super().__init__(name, age)
        self.grade = grade

    def set_grade(self, grade_):
        self.grade = grade_

    def show(self):
        super().show()
        print(f"and you are in grade {self.grade}\n")


if __name__ == "__main__":
    stu = Student("ffan", 30, 8)
    stu.show()

