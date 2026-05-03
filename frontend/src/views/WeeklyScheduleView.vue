<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center mb-4 flex-wrap gap-2">
      <div class="mr-4">
        <h1 class="text-h5 font-weight-bold">Weekly Schedule</h1>
        <div v-if="schedule" class="text-subtitle-2 text-medium-emphasis">
          Pay Period: {{ selectedYear }} #{{ activePage + 1 }}
        </div>
      </div>
      <v-select
        v-model="selectedYear"
        :items="availableYears"
        label="Year"
        density="compact"
        hide-details
        style="max-width: 120px"
      />
      <v-spacer />
      <v-btn
        v-if="schedule"
        prepend-icon="mdi-file-pdf-box"
        color="error"
        variant="tonal"
        density="comfortable"
        @click="downloadPdf(schedule, selectedYear, activePage)"
      >
        Download PDF
      </v-btn>
    </div>

    <template v-if="weeksLoading">
      <v-progress-linear indeterminate color="primary" />
    </template>

    <template v-else-if="weeksError">
      <v-alert
        v-if="weeksErrorStatus === 404"
        type="info"
        variant="tonal"
        icon="mdi-calendar-alert"
      >
        No payroll configuration found for <strong>{{ selectedYear }}</strong>.
        <template v-if="isStaff">
          Go to
          <router-link :to="{ name: 'management' }" class="text-primary">Management → Payroll</router-link>
          to set up a payroll info record for this year.
        </template>
        <template v-else>
          Contact your administrator to configure payroll for this year.
        </template>
      </v-alert>
      <v-alert v-else type="error" text="Failed to load payroll weeks. Please try again." />
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
          :is-staff="isStaff"
          @click-day="openCreateOverride"
          @click-entry="openEditOverride"
        />
        <v-alert
          v-if="!schedule.divisions.length"
          type="info"
          text="No divisions are assigned to your account for this week."
        />
      </template>
    </template>

    <template v-else>
      <v-alert type="info" text="No payroll weeks found for this year." />
    </template>
  </v-container>

  <!-- ── Override dialog ──────────────────────────────────── -->
  <v-dialog v-model="overrideDialog.open" max-width="520" persistent>
    <v-card>
      <v-card-title class="pt-4 px-4">{{ overrideDialog.title }}</v-card-title>
      <v-card-text class="px-4 pb-0">
        <CalendarEntryForm
          ref="overrideFormRef"
          :model-value="overrideDialog.item"
          @submit="onOverrideSubmit"
        />
      </v-card-text>
      <v-card-actions class="px-4 pb-4">
        <v-btn
          v-if="overrideDialog.item"
          color="error"
          variant="text"
          :loading="deleteMutation.isPending.value"
          @click="deleteOverride"
        >
          Delete
        </v-btn>
        <v-spacer />
        <v-btn variant="text" @click="closeOverrideDialog">Cancel</v-btn>
        <v-btn
          color="primary"
          variant="flat"
          :loading="createMutation.isPending.value || updateMutation.isPending.value"
          @click="overrideFormRef?.submit()"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { usePayrollWeeks } from "@/composables/usePayrollWeeks.js";
import { useWeeklySchedule } from "@/composables/useWeeklySchedule.js";
import { useCalendarEntries } from "@/composables/useCalendarEntries.js";
import { useSchedulePdf } from "@/composables/useSchedulePdf.js";
import { useAuthStore } from "@/stores/authStore.js";
import DivisionScheduleCard from "@/components/schedule/DivisionScheduleCard.vue";
import CalendarEntryForm from "@/components/schedule/CalendarEntryForm.vue";

const authStore = useAuthStore();
const isStaff = computed(() => authStore.isStaff);

const currentYear = new Date().getFullYear();
const availableYears = [currentYear - 1, currentYear, currentYear + 1];
const selectedYear = ref(currentYear);
const activePage = ref(0);

const {
  data: weeks,
  isLoading: weeksLoading,
  isError: weeksError,
  error: weeksErrorObj,
} = usePayrollWeeks(computed(() => selectedYear.value));

const weeksErrorStatus = computed(() => weeksErrorObj.value?.response?.status);

watch(weeks, (val) => {
  if (!val?.length) return;
  const today = new Date().toISOString().slice(0, 10);
  const match = val.find((w) => w.week_start <= today && today <= w.week_end);
  if (match) activePage.value = match.page;
});

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

const { downloadPdf } = useSchedulePdf();

// ── Override dialog ───────────────────────────────────────
const { createMutation, updateMutation, deleteMutation } = useCalendarEntries();

const overrideFormRef = ref(null);
const overrideDialog = ref({
  open: false,
  title: "",
  employeeId: null,
  employeeName: "",
  date: null,
  item: null,
});

function employeeName(employeeId) {
  for (const div of schedule.value?.divisions ?? []) {
    const emp = div.employees.find((e) => e.employee_id === employeeId);
    if (emp) return `${emp.first_name} ${emp.last_name}`;
  }
  return "";
}

function fmtDate(isoDate) {
  const dt = new Date(isoDate + "T00:00:00");
  return dt.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function openCreateOverride({ employeeId, date }) {
  overrideDialog.value = {
    open: true,
    title: `Add Override — ${employeeName(employeeId)}, ${fmtDate(date)}`,
    employeeId,
    date,
    item: null,
  };
}

function openEditOverride({ calendarEntryId, employeeId, date }) {
  // Find the existing entry data from the schedule to pre-fill the form
  let item = null;
  for (const div of schedule.value?.divisions ?? []) {
    const emp = div.employees.find((e) => e.employee_id === employeeId);
    if (emp) {
      const day = emp.days.find((d) => d.date === date);
      if (day) {
        const entry = day.entries.find((e) => e.calendar_entry_id === calendarEntryId);
        if (entry) item = { ...entry, id: calendarEntryId };
      }
    }
  }
  overrideDialog.value = {
    open: true,
    title: `Edit Override — ${employeeName(employeeId)}, ${fmtDate(date)}`,
    employeeId,
    date,
    item,
  };
}

function closeOverrideDialog() {
  overrideDialog.value = { open: false, title: "", employeeId: null, date: null, item: null };
}

function onOverrideSubmit(values) {
  const { employeeId, date, item } = overrideDialog.value;
  if (item) {
    updateMutation.mutate(
      { id: item.id, employee_id: employeeId, calendar_date: date, ...values },
      { onSuccess: closeOverrideDialog },
    );
  } else {
    createMutation.mutate(
      { employee_id: employeeId, calendar_date: date, ...values },
      { onSuccess: closeOverrideDialog },
    );
  }
}

function deleteOverride() {
  const { item } = overrideDialog.value;
  if (!item) return;
  deleteMutation.mutate(item.id, { onSuccess: closeOverrideDialog });
}
</script>
