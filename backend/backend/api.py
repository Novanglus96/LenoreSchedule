from ninja import NinjaAPI
from ninja.security import django_auth
from core.utils.auth import GlobalAuth
from core.utils.version import get_version

# Import routers from apps
from core.api.auth import router
from options.api.routers.health import health_router
from options.api.routers.version import version_router
from staff.api.routers.group import group_router
from staff.api.routers.department import department_router
from staff.api.routers.employee import employee_router

api = NinjaAPI(auth=[django_auth, GlobalAuth()])
api.title = "LenoreSchedule"
api.version = get_version()
api.description = "API documetation for LenoreSchedule"

# Add routers to the API
api.add_router("/accounts", router)
api.add_router("/options/health", health_router)
api.add_router("/options/version", version_router)
api.add_router("/groups", group_router)
api.add_router("/departments", department_router)
api.add_router("/employess", employee_router)
