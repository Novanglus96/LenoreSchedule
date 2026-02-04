from ninja import Router
from planner.api.views.holiday import holiday_router

router = Router()
router.add_router("/", holiday_router)
