<template>
  <tr>
    <td class="employee-name text-body-2 font-weight-medium pa-2" style="white-space: nowrap">
      <div class="d-flex align-center gap-1">
        <span>{{ employee.last_name }}, {{ employee.first_name }}</span>
        <v-tooltip
          v-if="isStaff && needsConfirmation"
          text="Confirm schedule for the week"
          location="right"
        >
          <template #activator="{ props: tooltipProps }">
            <v-btn
              v-bind="tooltipProps"
              icon
              size="x-small"
              variant="text"
              color="success"
              @click.stop="emit('confirm-week', { employeeId: employee.employee_id })"
            >
              <v-icon size="14">mdi-check-all</v-icon>
            </v-btn>
          </template>
        </v-tooltip>
      </div>
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
import { computed } from "vue";
import DayCell from "./DayCell.vue";

const props = defineProps({
  employee: { type: Object, required: true },
  isStaff: { type: Boolean, default: false },
});

const emit = defineEmits(["click-day", "click-entry", "confirm-week"]);

// Shown while anything this week is unconfirmed: a day still falling back to
// the default (template) schedule, or an override not yet confirmed.
const needsConfirmation = computed(() =>
  props.employee.days.some((d) =>
    d.entries.some(
      (e) => e.source === "template" || (e.source === "calendar" && !e.confirmed),
    ),
  ),
);
</script>
