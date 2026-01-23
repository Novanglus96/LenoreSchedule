from ninja import Router
from groups.api.views.group import group_router

router = Router()
router.add_router("/", group_router)
