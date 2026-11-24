<template>
  <v-container fluid class="pa-4">
    <div class="d-flex align-center flex-wrap mb-6 gap-2">
      <h1 class="text-h5 font-weight-bold">Dashboard</h1>
      <v-spacer />
      <span v-if="dashboard" class="text-body-2 text-medium-emphasis">
        This week: {{ fmtRange(dashboard.week_start, dashboard.week_end) }}
      </span>
    </div>

    <v-alert v-if="isError" type="error" variant="tonal" class="mb-4">
      Could not load the dashboard.
    </v-alert>

    <v-row>
      <!-- Vacations This Week -->
      <v-col cols="12" md="6" lg="3">
        <DashboardCard title="Vacations This Week" icon="mdi-beach" icon-color="teal">
          <v-progress-linear v-if="isLoading" indeterminate color="teal" />
          <div v-else-if="!dashboard?.vacations.length" class="empty">
            No vacations this week
          </div>
          <v-list v-else density="compact" class="pa-0 bg-transparent">
            <v-list-item
              v-for="v in dashboard.vacations"
              :key="v.employee_id"
              class="px-0"
              :title="fullName(v)"
              :subtitle="v.dates.map(fmtDay).join(', ')"
            />
          </v-list>
        </DashboardCard>
      </v-col>

      <!-- Birthdays This Week -->
      <v-col cols="12" md="6" lg="3">
        <DashboardCard title="Birthdays This Week" icon="mdi-cake-variant" icon-color="pink">
          <v-progress-linear v-if="isLoading" indeterminate color="pink" />
          <div v-else-if="!dashboard?.birthdays.length" class="empty">
            No birthdays this week
          </div>
          <v-list v-else density="compact" class="pa-0 bg-transparent">
            <v-list-item
              v-for="b in dashboard.birthdays"
              :key="b.employee_id"
              class="px-0"
              :title="fullName(b)"
              :subtitle="fmtDay(b.birthday_date)"
            />
          </v-list>
        </DashboardCard>
      </v-col>

      <!-- Upcoming Holidays -->
      <v-col cols="12" md="6" lg="3">
        <DashboardCard title="Upcoming Holidays" icon="mdi-calendar-star" icon-color="orange">
          <v-progress-linear v-if="isLoading" indeterminate color="orange" />
          <div v-else-if="!dashboard?.holidays.length" class="empty">
            No holidays in the next 90 days
          </div>
          <v-list v-else density="compact" class="pa-0 bg-transparent">
            <v-list-item
              v-for="h in dashboard.holidays"
              :key="`${h.holiday_date}-${h.holiday_name}`"
              class="px-0"
              :title="h.holiday_name"
              :subtitle="`${fmtDay(h.holiday_date)} · ${daysUntil(h.holiday_date)}`"
            />
          </v-list>
        </DashboardCard>
      </v-col>

      <!-- Unconfirmed Overrides -->
      <v-col cols="12" md="6" lg="3">
        <DashboardCard
          title="Unconfirmed Overrides"
          icon="mdi-clock-alert-outline"
          icon-color="blue"
        >
          <template #actions>
            <v-chip
              v-if="dashboard?.unconfirmed_total"
              size="small"
              color="blue"
              variant="flat"
            >
              {{ dashboard.unconfirmed_total }}
            </v-chip>
          </template>
          <v-progress-linear v-if="isLoading" indeterminate color="blue" />
          <div v-else-if="!dashboard?.unconfirmed.length" class="empty">
            Everything is confirmed
          </div>
          <template v-else>
            <v-list density="compact" class="pa-0 bg-transparent">
              <v-list-item
                v-for="u in dashboard.unconfirmed"
                :key="u.calendar_entry_id"
                class="px-0"
                :title="fullName(u)"
                :subtitle="`${fmtDay(u.calendar_date)} · ${u.entry_type}`"
              />
            </v-list>
            <div
              v-if="dashboard.unconfirmed_total > dashboard.unconfirmed.length"
              class="text-caption text-medium-emphasis mt-1"
            >
              + {{ dashboard.unconfirmed_total - dashboard.unconfirmed.length }} more
            </div>
            <v-btn
              to="/schedule"
              variant="text"
              color="blue"
              size="small"
              class="mt-2 px-0"
              append-icon="mdi-arrow-right"
            >
              Open schedule
            </v-btn>
          </template>
        </DashboardCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import DashboardCard from "@/components/dashboard/DashboardCard.vue";
import { useDashboard } from "@/composables/useDashboard.js";
import { localIsoDate } from "@/utils/employeeStatus.js";

const { data: dashboard, isLoading, isError } = useDashboard();

// API dates are plain YYYY-MM-DD; parse as local dates, not UTC.
const toDate = (iso) => new Date(`${iso}T00:00:00`);

function fmtDay(iso) {
  return toDate(iso).toLocaleDateString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

function fmtRange(start, end) {
  const opts = { month: "short", day: "numeric" };
  return `${toDate(start).toLocaleDateString(undefined, opts)} – ${toDate(end).toLocaleDateString(undefined, opts)}`;
}

function daysUntil(iso) {
  const days = Math.round((toDate(iso) - toDate(localIsoDate())) / 86400000);
  if (days === 0) return "today";
  if (days === 1) return "tomorrow";
  return `in ${days} days`;
}

const fullName = (p) => `${p.first_name} ${p.last_name}`;
</script>

<style scoped>
.empty {
  font-size: 0.875rem;
  font-style: italic;
  color: rgba(var(--v-theme-on-surface), var(--v-medium-emphasis-opacity));
}
</style>
