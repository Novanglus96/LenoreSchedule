<template>
  <v-card class="mb-4 division-card" variant="outlined">
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
        <div class="schedule-scroll">
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
                  @confirm-all="emit('confirm-all', $event)"
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

const emit = defineEmits(["click-day", "click-entry", "confirm-all"]);

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
/* Sticky date header.
   position: sticky binds to the nearest ancestor with overflow != visible,
   so v-card's overflow:hidden and any horizontal scroller must be relaxed
   on wide screens for the header to stick to the page under the app bar. */
.division-card {
  overflow: visible;
}
.schedule-scroll {
  overflow: visible;
}
.schedule-table thead th {
  position: sticky;
  top: 48px; /* compact v-app-bar height */
  z-index: 2;
  background: rgb(var(--v-theme-surface));
  box-shadow: inset 0 -1px 0 rgba(var(--v-border-color), var(--v-border-opacity));
}
.schedule-table thead th.today-col {
  background:
    linear-gradient(rgba(var(--v-theme-primary), 0.06), rgba(var(--v-theme-primary), 0.06)),
    rgb(var(--v-theme-surface));
}
/* Narrow screens need horizontal scrolling, so the table scrolls inside a
   bounded box and the header sticks to the top of that box instead. */
@media (max-width: 959px) {
  .schedule-scroll {
    overflow: auto;
    max-height: calc(100dvh - 140px);
  }
  .schedule-table thead th {
    top: 0;
  }
}
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
