from django.db import IntegrityError, transaction
from options.models import PayrollInfo
from options.dto import DomainPayrollInfo, DomainPayrollInfoIn
from options.exceptions import (
    PayrollInfoAlreadyExists,
    PayrollInfoCreationError,
    PayrollInfoDoesNotExist,
    PayrollInfoInvalidFirstDay,
    PayrollInfoInvalidFrequencyError,
    PayrollInfoInvalidSecondDay,
    PayrollInfoInvalidStart,
)
from options.mappers import (
    domain_payroll_info_to_model,
    model_to_domain_payroll_info,
)
from typing import List
from django.core.exceptions import ValidationError


def get_payroll_info_model_or_raise(payroll_info_id: int) -> PayrollInfo:
    """
    `get_payroll_info_model_or_raise` gets a payroll_info or raises an error
    if not found.

    Args:
        payroll_info_id (int): The id of the payroll_info to get.

    Raises:
        PayrollInfoDoesNotExist: PayrollInfo does not exist.

    Returns:
        PayrollInfo: A payroll_info model object.
    """
    try:
        return PayrollInfo.objects.get(id=payroll_info_id)
    except PayrollInfo.DoesNotExist:
        raise PayrollInfoDoesNotExist(payroll_info_id)


def create_payroll_info(dto: DomainPayrollInfoIn) -> DomainPayrollInfo:
    """
    `create_payroll_info` creates a payroll_info if a duplicate payroll_info does
    not exist.

    Args:
        dto (DomainPayrollInfoIn): A domain payroll_info object.

    Raises:
        PayrollInfoAlreadyExists: PayrollInfo already exists.
        PayrollInfoCreationError: PayrollInfoe creation error.

    Returns:
        DomainPayrollInfo: A domain payroll_info object.
    """
    if PayrollInfo.objects.filter(payroll_year=dto.payroll_year).exists():
        raise PayrollInfoAlreadyExists()

    payroll_info = domain_payroll_info_to_model(dto)
    try:
        payroll_info.full_clean()
    except ValidationError as exc:
        if "payroll_frequency" in exc.message_dict:
            raise PayrollInfoInvalidFrequencyError(
                f"Invalid payroll_frequency: {dto.payroll_frequency}"
            ) from exc
        raise  # re-raise anything else

    if (
        payroll_info.payroll_start.year != payroll_info.payroll_year
        and payroll_info.payroll_start.year != payroll_info.payroll_year - 1
    ):
        raise PayrollInfoInvalidStart()
    if payroll_info.payroll_frequency == "monthly":
        if payroll_info.first_day is None:
            raise PayrollInfoInvalidFirstDay()
        elif payroll_info.first_day < 1 or payroll_info.first_day > 31:
            raise PayrollInfoInvalidFirstDay()

    if payroll_info.payroll_frequency == "semi-monthly":
        if payroll_info.first_day is None:
            raise PayrollInfoInvalidFirstDay()
        if payroll_info.second_day is None:
            raise PayrollInfoInvalidSecondDay()
        if (
            payroll_info.first_day
            and payroll_info.second_day
            and payroll_info.second_day <= payroll_info.first_day
        ):
            raise PayrollInfoInvalidSecondDay()

    try:
        with transaction.atomic():
            payroll_info.save()
    except IntegrityError as e:
        raise PayrollInfoCreationError() from e

    return model_to_domain_payroll_info(payroll_info)


def update_payroll_info(
    payroll_info_id: int, dto: DomainPayrollInfoIn
) -> DomainPayrollInfo:
    """
    `update_payroll_info` updates a payroll_info

    Args:
        payroll_info_id (int): ID of the payroll_info to update.
        dto (DomainPayrollInfoIn): The updated domain payroll_info object.

    Raises:
        PayrollInfoAlreadyExists: PayrollInfo already exists.

    Returns:
        DomainPayrollInfo: A domain payroll_info object.
    """
    payroll_info = get_payroll_info_model_or_raise(payroll_info_id)

    if PayrollInfo.objects.filter(payroll_year=dto.payroll_year).exclude(id=payroll_info_id).exists():
        raise PayrollInfoAlreadyExists()

    if dto.payroll_year is not None:
        payroll_info.payroll_year = dto.payroll_year

    if dto.payroll_start is not None:
        payroll_info.payroll_start = dto.payroll_start

    if dto.payroll_frequency is not None:
        payroll_info.payroll_frequency = dto.payroll_frequency

    if dto.payroll_frequency == "monthly":
        if dto.first_day is not None:
            payroll_info.first_day = dto.first_day
        else:
            raise PayrollInfoInvalidFirstDay()
    if dto.payroll_frequency == "semi-monthly":
        if dto.first_day is not None:
            payroll_info.first_day = dto.first_day
        else:
            raise PayrollInfoInvalidFirstDay()
        if (
            dto.second_day is not None
            and dto.first_day is not None
            and dto.second_day > dto.first_day
        ):
            payroll_info.second_day = dto.second_day
        else:
            raise PayrollInfoInvalidSecondDay()
    payroll_info.save()

    return model_to_domain_payroll_info(payroll_info)


def get_payroll_info(payroll_info_id: int) -> DomainPayrollInfo:
    """
    `get_payroll_info` returns a domain payroll_info object.

    Args:
        payroll_info_id (int): ID of the payroll_info to get.

    Returns:
        DomainPayrollInfo: The domain payroll_info object.
    """
    payroll_info = get_payroll_info_model_or_raise(payroll_info_id)

    return model_to_domain_payroll_info(payroll_info)


def get_ordered_list_of_payroll_infos() -> List[DomainPayrollInfo]:
    """
    `get_ordered_list_of_payroll_infos` gets a list of domain payroll_info objects, ordered
    by payroll_year descending.

    Returns:
        List[DomainPayrollInfo]: A list of domain payroll_info objects.
    """
    payroll_infos = PayrollInfo.objects.all().order_by("-payroll_year")

    return [model_to_domain_payroll_info(g) for g in payroll_infos]


def delete_payroll_info(payroll_info_id: int) -> str:
    """
    `delete_payroll_info` deletes a payroll_info and returns the deleted payroll_info name.

    Args:
        payroll_info_id (int): The id of the payroll_info to delete.

    Returns:
        (int): The year of the deleted payroll_info.
    """
    payroll_info = get_payroll_info_model_or_raise(payroll_info_id)
    payroll_year = payroll_info.payroll_year

    payroll_info.delete()
    return payroll_year
