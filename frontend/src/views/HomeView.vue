<template>
  <v-container fluid class="pa-4">
    <h1 class="text-h5 font-weight-bold mb-6">Dashboard</h1>

    <v-row>
      <!-- Vacations This Week -->
      <v-col cols="12" md="6" lg="4">
        <DashboardCard
          title="Vacations This Week"
          icon="mdi-beach"
          icon-color="teal"
        >
          <div class="text-body-2 text-medium-emphasis font-italic">Coming soon</div>
        </DashboardCard>
      </v-col>

      <!-- Upcoming Holidays -->
      <v-col cols="12" md="6" lg="4">
        <DashboardCard
          title="Upcoming Holidays"
          icon="mdi-calendar-star"
          icon-color="orange"
        >
          <div class="text-body-2 text-medium-emphasis font-italic">Coming soon</div>
        </DashboardCard>
      </v-col>

      <!-- Unconfirmed Overrides -->
      <v-col cols="12" md="6" lg="4">
        <DashboardCard
          title="Unconfirmed Overrides"
          icon="mdi-clock-alert-outline"
          icon-color="blue"
        >
          <div class="text-body-2 text-medium-emphasis font-italic">Coming soon</div>
        </DashboardCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import DashboardCard from "@/components/dashboard/DashboardCard.vue";
</script>
