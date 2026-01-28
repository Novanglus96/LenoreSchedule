class GroupAlreadyExists(Exception):
    pass


class GroupCreationError(Exception):
    pass


class GroupDoesNotExist(Exception):
    def __init__(self, group_id: int):
        super().__init__(f"Group {group_id} does not exist")
        self.group_id = group_id
