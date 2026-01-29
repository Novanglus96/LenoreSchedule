from ninja import Router
from staff.api.views.group import group_router

router = Router()
router.add_router("/", group_router)
