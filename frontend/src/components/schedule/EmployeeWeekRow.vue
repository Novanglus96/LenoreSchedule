<template>
  <tr>
    <td class="employee-name text-body-2 font-weight-medium pa-2" style="white-space: nowrap">
      {{ employee.last_name }}, {{ employee.first_name }}
      <div class="text-caption text-disabled">{{ employee.group_name }}</div>
    </td>
    <td v-for="day in employee.days" :key="day.date" class="pa-1 align-top">
      <DayCell
        :entries="day.entries"
        :is-staff="isStaff"
        :default-location-id="employee.default_location_id ?? null"
        @click-day="emit('click-day', { employeeId: employee.employee_id, date: day.date })"
        @click-entry="(calendarEntryId) => emit('click-entry', { calendarEntryId, employeeId: employee.employee_id, date: day.date })"
      />
    </td>
  </tr>
</template>

<script setup>
import DayCell from "./DayCell.vue";

defineProps({
  employee: { type: Object, required: true },
  isStaff: { type: Boolean, default: false },
});

const emit = defineEmits(["click-day", "click-entry"]);
</script>
