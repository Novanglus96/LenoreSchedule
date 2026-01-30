class GroupAlreadyExists(Exception):
    pass


class GroupCreationError(Exception):
    pass


class GroupDoesNotExist(Exception):
    def __init__(self, group_id: int):
        super().__init__(f"Group {group_id} does not exist")
        self.group_id = group_id


class DivisionAlreadyExists(Exception):
    pass


class DivisionCreationError(Exception):
    pass


class DivisionDoesNotExist(Exception):
    def __init__(self, division_id: int):
        super().__init__(f"Division {division_id} does not exist")
        self.division_id = division_id


class EmployeeAlreadyExists(Exception):
    pass


class EmployeeCreationError(Exception):
    pass


class EmployeeDoesNotExist(Exception):
    def __init__(self, employee_id: int):
        super().__init__(f"Employee {employee_id} does not exist")
        self.employee_id = employee_id


class LocationAlreadyExists(Exception):
    pass


class LocationCreationError(Exception):
    pass


class LocationDoesNotExist(Exception):
    def __init__(self, location_id: int):
        super().__init__(f"Location {location_id} does not exist")
        self.location_id = location_id
