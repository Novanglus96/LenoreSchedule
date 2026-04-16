from ninja import Router
from options.api.views.payroll_info import payroll_info_router

router = Router()
router.add_router("/", payroll_info_router)
