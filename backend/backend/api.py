from ninja import NinjaAPI
from ninja.security import django_auth
from core.utils.auth import GlobalAuth
from core.utils.version import get_version

# Import routers from apps
from core.api.auth import router
from options.api.routers.health import health_router
from options.api.routers.version import version_router
from staff.api.routers.group import group_router
from staff.api.routers.division import division_router
from staff.api.routers.employee import employee_router
from staff.api.routers.location import location_router
from planner.api.routers.holiday import holiday_router
from planner.api.routers.calendar_entry import calendar_entry_router
from planner.api.routers.schedule_template import router as schedule_template_router
from options.api.routers.payroll_info import router as payroll_info_router

api = NinjaAPI(auth=[django_auth, GlobalAuth()])
api.title = "LenoreSchedule"
api.version = get_version()
api.description = "API documetation for LenoreSchedule"

# Add routers to the API
api.add_router("/accounts", router)
api.add_router("/options/health", health_router)
api.add_router("/options/version", version_router)
api.add_router("/groups", group_router)
api.add_router("/divisions", division_router)
api.add_router("/employees", employee_router)
api.add_router("/locations", location_router)
api.add_router("/calendar/holidays", holiday_router)
api.add_router("/calendar/", calendar_entry_router)
api.add_router("/schedule_templates", schedule_template_router)
api.add_router("/options/payroll_infos", payroll_info_router)
