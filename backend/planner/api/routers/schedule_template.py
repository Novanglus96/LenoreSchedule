from ninja import Router
from planner.api.views.schedule_template import schedule_template_router

router = Router()
router.add_router("/", schedule_template_router)
