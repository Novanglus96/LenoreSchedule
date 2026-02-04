from ninja import Router
from staff.api.views.holiday import holiday_router

router = Router()
router.add_router("/", holiday_router)
