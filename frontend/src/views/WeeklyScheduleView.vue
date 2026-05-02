<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center mb-4 flex-wrap gap-2">
      <h1 class="text-h5 font-weight-bold mr-4">Weekly Schedule</h1>
      <v-select
        v-model="selectedYear"
        :items="availableYears"
        label="Year"
        density="compact"
        hide-details
        style="max-width: 120px"
      />
    </div>

    <template v-if="weeksLoading">
      <v-progress-linear indeterminate color="primary" />
    </template>

    <template v-else-if="weeksError">
      <v-alert type="error" text="Failed to load payroll weeks." />
    </template>

    <template v-else-if="weeks && weeks.length">
      <v-tabs
        v-model="activePage"
        density="compact"
        show-arrows
        color="primary"
        class="mb-4"
      >
        <v-tab
          v-for="week in weeks"
          :key="week.page"
          :value="week.page"
        >
          {{ week.label }}
        </v-tab>
      </v-tabs>

      <template v-if="scheduleLoading">
        <v-row>
          <v-col v-for="n in 3" :key="n" cols="12">
            <v-skeleton-loader type="table-row-divider" />
          </v-col>
        </v-row>
      </template>

      <template v-else-if="scheduleError">
        <v-alert type="error" text="Failed to load schedule for this week." />
      </template>

      <template v-else-if="schedule">
        <DivisionScheduleCard
          v-for="div in schedule.divisions"
          :key="div.division_id"
          :division="div"
        />
        <v-alert
          v-if="!schedule.divisions.length"
          type="info"
          text="No divisions found for your account."
        />
      </template>
    </template>

    <template v-else>
      <v-alert type="info" text="No payroll weeks found for this year." />
    </template>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { usePayrollWeeks } from "@/composables/usePayrollWeeks.js";
import { useWeeklySchedule } from "@/composables/useWeeklySchedule.js";
import DivisionScheduleCard from "@/components/schedule/DivisionScheduleCard.vue";

const currentYear = new Date().getFullYear();
const availableYears = [currentYear - 1, currentYear, currentYear + 1];
const selectedYear = ref(currentYear);
const activePage = ref(0);

const {
  data: weeks,
  isLoading: weeksLoading,
  isError: weeksError,
} = usePayrollWeeks(computed(() => selectedYear.value));

// Jump to the current week when weeks load
watch(weeks, (val) => {
  if (!val?.length) return;
  const today = new Date().toISOString().slice(0, 10);
  const match = val.find((w) => w.week_start <= today && today <= w.week_end);
  if (match) activePage.value = match.page;
});

// Reset to page 0 when year changes
watch(selectedYear, () => {
  activePage.value = 0;
});

const {
  data: schedule,
  isLoading: scheduleLoading,
  isError: scheduleError,
} = useWeeklySchedule(
  computed(() => activePage.value),
  computed(() => selectedYear.value),
);
</script>
