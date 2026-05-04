from ninja import Router
from ninja.errors import HttpError
from datetime import date
import logging

from planner.api.schemas.weekly_schedule import WeeklyScheduleOut
from planner.services.weekly_schedule_services import get_weekly_division_schedule
from core.utils.auth import get_user_divisions
from options.exceptions import PayrollInfoDoesNotExist

api_logger = logging.getLogger("api")
error_logger = logging.getLogger("error")

weekly_schedule_router = Router(tags=["WeeklySchedule"])


@weekly_schedule_router.get("/weekly_schedule", response=WeeklyScheduleOut)
def get_weekly_schedule(request, page: int = 0, payroll_year: int = None):
    """
    Returns a merged weekly schedule for all employees in the user's
    accessible divisions, grouped by division.

    Endpoint:
        - **Path**: `/api/v1/calendar/weekly_schedule`
        - **Method**: `GET`

    Query params:
        page (int): 0-based week index within the payroll year. Defaults to 0.
        payroll_year (int): Payroll year to use. Defaults to the current year.

    Returns:
        WeeklyScheduleOut: Weekly schedule with pagination metadata and
        division/employee/day entries.
    """
    if payroll_year is None:
        payroll_year = date.today().year

    try:
        domain = get_weekly_division_schedule(
            page=page,
            payroll_year=payroll_year,
            divisions=get_user_divisions(request),
        )
    except PayrollInfoDoesNotExist:
        raise HttpError(404, f"No payroll info found for year {payroll_year}")
    except IndexError as e:
        raise HttpError(400, str(e))
    except Exception as e:
        api_logger.error("Weekly schedule not retrieved")
        error_logger.error(str(e))
        raise HttpError(500, "Weekly schedule not retrieved")

    return WeeklyScheduleOut(
        week_label=domain.week_label,
        week_start=domain.week_start,
        week_end=domain.week_end,
        page=domain.page,
        total_pages=domain.total_pages,
        current_page=domain.current_page,
        divisions=[
            {
                "division_id": div.division_id,
                "division_name": div.division_name,
                "groups": [
                    {
                        "group_name": grp.group_name,
                        "employees": [
                            {
                                "employee_id": emp.employee_id,
                                "first_name": emp.first_name,
                                "last_name": emp.last_name,
                                "group_name": emp.group_name,
                                "default_location_id": emp.default_location_id,
                                "days": [
                                    {
                                        "date": day.date,
                                        "entries": [
                                            {
                                                "source": e.source,
                                                "entry_type": e.entry_type,
                                                "start_time": e.start_time,
                                                "end_time": e.end_time,
                                                "location": e.location,
                                                "confirmed": e.confirmed,
                                                "notes": e.notes,
                                                "holiday_name": e.holiday_name,
                                                "calendar_entry_id": e.calendar_entry_id,
                                            }
                                            for e in day.entries
                                        ],
                                    }
                                    for day in emp.days
                                ],
                            }
                            for emp in grp.employees
                        ],
                    }
                    for grp in div.groups
                ],
            }
            for div in domain.divisions
        ],
    )
