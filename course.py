class Course:
    def __init__(self, name, code, hours):
        self.name = name
        self.code = code
        self.hours = hours


class Category:
    def __init__(self, code, name, weight, assignments):
        self.code = code
        self.name = name
        self.weight = weight
        self.assignments = assignments
        self.entered=0
    