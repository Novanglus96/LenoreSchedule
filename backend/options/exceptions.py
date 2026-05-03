class PayrollInfoAlreadyExists(Exception):
    pass


class PayrollInfoCreationError(Exception):
    pass


class PayrollInfoDoesNotExist(Exception):
    def __init__(self, payroll_into_id: int):
        super().__init__(f"Payroll Info {payroll_into_id} does not exist")
        self.payrollinfo_id = payroll_into_id


class PayrollInfoInvalidFrequencyError(Exception):
    pass


class PayrollInfoInvalidFirstDay(Exception):
    pass


class PayrollInfoInvalidSecondDay(Exception):
    pass


class PayrollInfoInvalidStart(Exception):
    pass
