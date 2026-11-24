from ninja import Router
from planner.api.views.dashboard import dashboard_router

router = Router()
router.add_router("/", dashboard_router)
