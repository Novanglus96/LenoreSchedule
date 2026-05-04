from ninja import Router
from planner.api.views.entry_type import entry_type_router

router = Router()
router.add_router("/", entry_type_router)
