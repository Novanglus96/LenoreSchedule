<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center mb-4 flex-wrap gap-2">
      <div class="mr-4">
        <h1 class="text-h5 font-weight-bold">Weekly Schedule</h1>
        <div v-if="schedule" class="text-subtitle-2 text-medium-emphasis">
          Pay Period: {{ selectedYear }} #{{ payPeriodNumber }}
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
      <v-menu v-if="schedule" location="bottom end">
        <template #activator="{ props: menuProps }">
          <v-btn
            prepend-icon="mdi-file-pdf-box"
            append-icon="mdi-chevron-down"
            color="error"
            variant="tonal"
            density="comfortable"
            v-bind="menuProps"
          >
            Download PDF
          </v-btn>
        </template>
        <v-list density="compact" min-width="200">
          <v-list-item
            prepend-icon="mdi-view-list"
            title="All Divisions"
            @click="downloadPdf(schedule, selectedYear, activePage)"
          />
          <v-divider v-if="schedule.divisions.length" />
          <v-list-item
            v-for="div in schedule.divisions"
            :key="div.division_id"
            prepend-icon="mdi-account-group"
            :title="div.division_name"
            @click="downloadPdf(schedule, selectedYear, activePage, div.division_id)"
          />
        </v-list>
      </v-menu>
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
      <div class="d-flex align-center gap-2 mb-4">
        <v-tabs
          v-model="activePage"
          density="compact"
          show-arrows
          color="primary"
          class="flex-grow-1"
        >
          <v-tab
            v-for="week in weeks"
            :key="week.page"
            :value="week.page"
          >
            {{ week.label }}
          </v-tab>
        </v-tabs>
        <v-btn
          v-if="!isOnCurrentWeek"
          size="small"
          variant="tonal"
          color="primary"
          prepend-icon="mdi-calendar-today"
          @click="jumpToCurrentWeek"
        >
          Today
        </v-btn>
      </div>

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
          @confirm-all="confirmAllOverrides"
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

const today = new Date().toISOString().slice(0, 10);

const payPeriodNumber = computed(() => {
  const label = weeks.value?.find((w) => w.page === activePage.value)?.label ?? "";
  const first = label.split(".")[0];
  return isNaN(Number(first)) ? activePage.value + 1 : Number(first);
});

const currentWeekPage = computed(() => {
  const match = weeks.value?.find((w) => w.week_start <= today && today <= w.week_end);
  return match?.page ?? null;
});

const isOnCurrentWeek = computed(
  () => selectedYear.value === currentYear && activePage.value === currentWeekPage.value,
);

function jumpToCurrentWeek() {
  if (selectedYear.value === currentYear) {
    if (currentWeekPage.value !== null) activePage.value = currentWeekPage.value;
  } else {
    // Changing the year triggers watch(weeks) which will land on the current week
    selectedYear.value = currentYear;
  }
}

watch(weeks, (val) => {
  if (!val?.length) return;
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
const { createMutation, updateMutation, deleteMutation, confirmWeekMutation } = useCalendarEntries();

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
    for (const grp of div.groups) {
      const emp = grp.employees.find((e) => e.employee_id === employeeId);
      if (emp) return `${emp.first_name} ${emp.last_name}`;
    }
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
  outer: for (const div of schedule.value?.divisions ?? []) {
    for (const grp of div.groups) {
      const emp = grp.employees.find((e) => e.employee_id === employeeId);
      if (emp) {
        const day = emp.days.find((d) => d.date === date);
        if (day) {
          const entry = day.entries.find((e) => e.calendar_entry_id === calendarEntryId);
          if (entry) item = { ...entry, id: calendarEntryId };
        }
        break outer;
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

function confirmAllOverrides({ employeeId }) {
  if (!schedule.value) return;
  confirmWeekMutation.mutate({
    employee_id: employeeId,
    week_start: schedule.value.week_start,
    week_end: schedule.value.week_end,
  });
}
</script>
