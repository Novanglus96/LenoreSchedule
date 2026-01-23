from ninja import Router
from groups.models import Group
import logging

api_logger = logging.getLogger("api")
db_logger = logging.getLogger("db")
error_logger = logging.getLogger("error")
task_logger = logging.getLogger("task")

group_router = Router(tags=["Groups"])
