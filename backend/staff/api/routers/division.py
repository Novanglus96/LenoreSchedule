from ninja import Router
from staff.api.views.division import division_router

router = Router()
router.add_router("/", division_router)
