from ninja import Router
from planner.api.views.calendar_entry import calendar_entry_router

router = Router()
router.add_router("/", calendar_entry_router)
