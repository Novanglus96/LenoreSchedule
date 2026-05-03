from ninja import Router
from staff.api.views.employee import employee_router

router = Router()
router.add_router("/", employee_router)
