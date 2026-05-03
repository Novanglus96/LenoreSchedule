from ninja import Router
from staff.api.views.location import location_router

router = Router()
router.add_router("/", location_router)
