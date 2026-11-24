from dataclasses import asdict
import logging

from ninja import Router
from ninja.errors import HttpError

from core.utils.auth import get_user_divisions
from planner.api.schemas.dashboard import DashboardOut
from planner.services.dashboard_services import get_dashboard

api_logger = logging.getLogger("api")
error_logger = logging.getLogger("error")

dashboard_router = Router(tags=["Dashboard"])


@dashboard_router.get("/summary", response=DashboardOut)
def get_dashboard_endpoint(request):
    """
    Returns the data for every home-page dashboard widget, limited to the
    divisions the user can see.

    Endpoint:
        - **Path**: `/api/v1/dashboard/summary`
        - **Method**: `GET`

    Returns:
        DashboardOut: Vacations and birthdays this week, upcoming holidays and
        unconfirmed overrides.
    """
    try:
        return asdict(get_dashboard(divisions=get_user_divisions(request)))
    except Exception as e:
        api_logger.error("Dashboard not retrieved")
        error_logger.error(str(e))
        raise HttpError(500, "Dashboard not retrieved")
