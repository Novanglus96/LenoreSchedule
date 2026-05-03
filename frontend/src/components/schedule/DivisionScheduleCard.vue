<template>
  <v-card class="mb-4" variant="outlined">
    <v-card-title
      class="d-flex align-center cursor-pointer py-2 px-4"
      @click="open = !open"
    >
      <v-icon :icon="open ? 'mdi-chevron-down' : 'mdi-chevron-right'" class="mr-2" />
      {{ division.division_name }}
      <v-chip class="ml-2" size="x-small" variant="tonal">
        {{ division.employees.length }}
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
              <EmployeeWeekRow
                v-for="emp in division.employees"
                :key="emp.employee_id"
                :employee="emp"
                :is-staff="isStaff"
                @click-day="emit('click-day', $event)"
                @click-entry="emit('click-entry', $event)"
              />
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

const dayHeaders = computed(() => {
  if (!props.division.employees.length) return [];
  return props.division.employees[0].days.map((d) => {
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
</style>
