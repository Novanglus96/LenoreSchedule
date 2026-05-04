<template>
  <v-card class="mb-4" variant="outlined">
    <v-card-title
      class="d-flex align-center cursor-pointer py-2 px-4"
      @click="open = !open"
    >
      <v-icon :icon="open ? 'mdi-chevron-down' : 'mdi-chevron-right'" class="mr-2" />
      {{ division.division_name }}
      <v-chip class="ml-2" size="x-small" variant="tonal">
        {{ totalEmployees }}
      </v-chip>
    </v-card-title>

    <v-expand-transition>
      <div v-show="open">
        <v-divider />
        <div class="overflow-x-auto">
          <table class="schedule-table w-100">
            <thead>
              <tr>
                <th class="text-left pa-2 employee-col">Employee</th>
                <th
                  v-for="day in dayHeaders"
                  :key="day.date"
                  class="text-center pa-2 day-col"
                  :class="{ 'today-col': day.isToday }"
                >
                  <div class="text-caption font-weight-bold">{{ day.weekday }}</div>
                  <div class="text-caption">{{ day.label }}</div>
                </th>
              </tr>
            </thead>
            <tbody>
              <template v-for="group in division.groups" :key="group.group_name">
                <tr class="group-header-row">
                  <td :colspan="dayHeaders.length + 1" class="group-header-cell px-3 py-1">
                    {{ group.group_name }}
                  </td>
                </tr>
                <EmployeeWeekRow
                  v-for="emp in group.employees"
                  :key="emp.employee_id"
                  :employee="emp"
                  :is-staff="isStaff"
                  @click-day="emit('click-day', $event)"
                  @click-entry="emit('click-entry', $event)"
                />
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script setup>
import { ref, computed } from "vue";
import EmployeeWeekRow from "./EmployeeWeekRow.vue";

const props = defineProps({
  division: { type: Object, required: true },
  isStaff: { type: Boolean, default: false },
});

const emit = defineEmits(["click-day", "click-entry"]);

const open = ref(true);

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const today = new Date().toISOString().slice(0, 10);

const totalEmployees = computed(() =>
  props.division.groups.reduce((sum, g) => sum + g.employees.length, 0),
);

const dayHeaders = computed(() => {
  const firstEmp = props.division.groups[0]?.employees[0];
  if (!firstEmp) return [];
  return firstEmp.days.map((d) => {
    const dt = new Date(d.date + "T00:00:00");
    return {
      date: d.date,
      weekday: WEEKDAYS[dt.getDay()],
      label: `${dt.getMonth() + 1}/${dt.getDate()}`,
      isToday: d.date === today,
    };
  });
});
</script>

<style scoped>
.schedule-table {
  border-collapse: collapse;
}
.schedule-table th,
.schedule-table td {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  vertical-align: top;
}
.employee-col {
  min-width: 140px;
}
.day-col {
  min-width: 96px;
}
.today-col {
  background: rgba(var(--v-theme-primary), 0.06);
}
.group-header-row {
  background: rgba(var(--v-theme-surface-variant), 0.5);
}
.group-header-cell {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: rgba(var(--v-theme-on-surface), 0.6);
}
</style>
