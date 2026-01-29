from ninja import Router
from staff.api.views.department import department_router

router = Router()
router.add_router("/", department_router)
