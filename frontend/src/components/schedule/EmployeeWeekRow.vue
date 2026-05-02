<template>
  <tr>
    <td class="employee-name text-body-2 font-weight-medium pa-2" style="white-space: nowrap">
      {{ employee.last_name }}, {{ employee.first_name }}
      <div class="text-caption text-disabled">{{ employee.group_name }}</div>
    </td>
    <td v-for="day in employee.days" :key="day.date" class="pa-1 align-top">
      <DayCell :entries="day.entries" />
    </td>
  </tr>
</template>

<script setup>
import DayCell from "./DayCell.vue";

defineProps({
  employee: {
    type: Object,
    required: true,
  },
});
</script>
