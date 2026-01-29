class GroupAlreadyExists(Exception):
    pass


class GroupCreationError(Exception):
    pass


class GroupDoesNotExist(Exception):
    def __init__(self, group_id: int):
        super().__init__(f"Group {group_id} does not exist")
        self.group_id = group_id


class DepartmentAlreadyExists(Exception):
    pass


class DepartmentCreationError(Exception):
    pass


class DepartmentDoesNotExist(Exception):
    def __init__(self, department_id: int):
        super().__init__(f"Department {department_id} does not exist")
        self.department_id = department_id


class EmployeeAlreadyExists(Exception):
    pass


class EmployeeCreationError(Exception):
    pass


class EmployeeDoesNotExist(Exception):
    def __init__(self, employee_id: int):
        super().__init__(f"Employee {employee_id} does not exist")
        self.employee_id = employee_id
