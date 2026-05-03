from ninja import Router
from planner.api.views.weekly_schedule import weekly_schedule_router

router = Router()
router.add_router("/", weekly_schedule_router)
