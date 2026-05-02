<template>
  <div class="day-cell pa-1">
    <div v-if="entries.length === 0" class="text-caption text-disabled">—</div>
    <v-chip
      v-for="(entry, i) in entries"
      :key="i"
      :color="chipColor(entry)"
      size="x-small"
      variant="tonal"
      class="mb-1 d-flex"
      :title="chipTitle(entry)"
    >
      <span class="text-truncate" style="max-width: 90px">
        {{ chipLabel(entry) }}
      </span>
    </v-chip>
  </div>
</template>

<script setup>
defineProps({
  entries: {
    type: Array,
    default: () => [],
  },
});

function chipColor(entry) {
  if (entry.source === "holiday") return "orange";
  if (entry.source === "calendar") return "blue";
  return "grey";
}

function chipLabel(entry) {
  if (entry.source === "holiday") return entry.holiday_name || "Holiday";
  if (entry.entry_type === "day_off") return "Day Off";
  if (entry.start_time && entry.end_time)
    return `${fmtTime(entry.start_time)} – ${fmtTime(entry.end_time)}`;
  return entry.entry_type;
}

function chipTitle(entry) {
  const parts = [];
  if (entry.source === "calendar") parts.push("Override");
  if (entry.source === "template") parts.push("Template");
  if (entry.source === "holiday") parts.push("Holiday");
  if (entry.location?.name) parts.push(entry.location.name);
  if (entry.notes) parts.push(entry.notes);
  if (!entry.confirmed) parts.push("Unconfirmed");
  return parts.join(" · ");
}

function fmtTime(t) {
  if (!t) return "";
  const [h, m] = t.split(":");
  const hour = parseInt(h);
  const ampm = hour >= 12 ? "pm" : "am";
  return `${hour % 12 || 12}:${m}${ampm}`;
}
</script>

<style scoped>
.day-cell {
  min-width: 90px;
}
</style>
