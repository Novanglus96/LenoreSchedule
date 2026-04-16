from options.dto import DomainPayrollInfo, DomainPayrollInfoIn
from options.api.schemas.payroll_info import PayrollInfoIn, PayrollInfoOut
from options.models import PayrollInfo


def domain_payroll_info_to_schema(payroll: DomainPayrollInfo) -> PayrollInfoOut:
    return PayrollInfoOut(
        id=payroll.id,
        payroll_year=payroll.payroll_year,
        payroll_start=payroll.payroll_start,
        payroll_frequency=payroll.payroll_frequency,
        first_day=payroll.first_day,
        second_day=payroll.second_day,
    )


def schema_to_domain_payroll_info(schema: PayrollInfoIn) -> DomainPayrollInfoIn:
    return DomainPayrollInfoIn(
        payroll_year=schema.payroll_year,
        payroll_start=schema.payroll_start,
        payroll_frequency=schema.payroll_frequency,
        first_day=schema.first_day,
        second_day=schema.second_day,
    )


def domain_payroll_info_to_model(dto: DomainPayrollInfoIn) -> PayrollInfo:
    return PayrollInfo(
        payroll_year=dto.payroll_year,
        payroll_start=dto.payroll_start,
        payroll_frequency=dto.payroll_frequency,
        first_day=dto.first_day,
        second_day=dto.second_day,
    )


def model_to_domain_payroll_info(model: PayrollInfo) -> DomainPayrollInfo:
    return DomainPayrollInfo(
        id=model.id,
        payroll_year=model.payroll_year,
        payroll_start=model.payroll_start,
        payroll_frequency=model.payroll_frequency,
        first_day=model.first_day,
        second_day=model.second_day,
    )
