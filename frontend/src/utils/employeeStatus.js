// An employee is inactive once their end_date has passed. Employees with no
// end_date (or one today / in the future) are active.

export function localIsoDate(d = new Date()) {
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export function isEmployeeActive(employee, onDate = localIsoDate()) {
  return !employee?.end_date || employee.end_date >= onDate;
}
