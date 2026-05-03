<template>
  <div
    class="day-cell pa-1 d-flex flex-column align-center"
    :class="{ 'day-cell--clickable': isStaff }"
    :title="isStaff ? 'Click to add override' : undefined"
    @click="isStaff && emit('click-day')"
  >
    <div v-if="entries.length === 0" class="text-caption text-disabled">—</div>
    <v-chip
      v-for="(entry, i) in entries"
      :key="i"
      :color="chipColor(entry)"
      :variant="chipVariant(entry)"
      size="x-small"
      class="mb-1"
      :title="chipTitle(entry)"
      :class="{ 'cursor-pointer': isStaff }"
      @click="handleChipClick(entry, $event)"
    >
      <span class="text-truncate" style="max-width: 130px">
        {{ chipLabel(entry) }}
      </span>
      <v-icon
        v-if="isStaff && entry.source === 'calendar'"
        size="10"
        class="ml-1"
        icon="mdi-pencil"
      />
    </v-chip>
  </div>
</template>

<script setup>
const props = defineProps({
  entries: { type: Array, default: () => [] },
  isStaff: { type: Boolean, default: false },
  defaultLocationId: { type: Number, default: null },
});

const emit = defineEmits(["click-day", "click-entry"]);

function handleChipClick(entry, event) {
  if (!props.isStaff) return;
  if (entry.source === "calendar") {
    event.stopPropagation();
    emit("click-entry", entry.calendar_entry_id);
  }
}

function chipColor(entry) {
  if (entry.source === "holiday") return "orange";
  if (entry.source === "calendar") return "blue";
  return "grey";
}

function chipVariant(entry) {
  if (entry.source === "calendar") {
    return entry.confirmed ? "flat" : "outlined";
  }
  return "tonal";
}

function chipLabel(entry) {
  if (entry.source === "holiday") return entry.holiday_name || "Holiday";
  if (entry.entry_type === "day_off") return "Day Off";
  if (entry.start_time && entry.end_time) {
    const hours = calcHours(entry.start_time, entry.end_time);
    const timeStr = `${fmtTime(entry.start_time)} – ${fmtTime(entry.end_time)}`;
    const base = hours ? `${timeStr} (${hours})` : timeStr;
    const loc = locationLabel(entry);
    return loc ? `${base} @ ${loc}` : base;
  }
  const loc = locationLabel(entry);
  return loc ? `${entry.entry_type} @ ${loc}` : entry.entry_type;
}

function locationLabel(entry) {
  if (!entry.location) return null;
  if (entry.location.id === props.defaultLocationId) return null;
  return entry.location.location_name;
}

function chipTitle(entry) {
  const parts = [];
  if (entry.source === "calendar") parts.push(entry.confirmed ? "Override (confirmed)" : "Override (unconfirmed)");
  if (entry.source === "template") parts.push("Template");
  if (entry.source === "holiday") parts.push("Holiday");
  if (entry.location?.location_name) parts.push(entry.location.location_name);
  if (entry.notes) parts.push(entry.notes);
  return parts.join(" · ");
}

function calcHours(startTime, endTime) {
  if (!startTime || !endTime) return null;
  const [sh, sm] = startTime.split(":").map(Number);
  const [eh, em] = endTime.split(":").map(Number);
  const totalMinutes = eh * 60 + em - (sh * 60 + sm);
  if (totalMinutes <= 0) return null;
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return m === 0 ? `${h}h` : `${h}h${m}m`;
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
.day-cell--clickable {
  cursor: pointer;
}
.day-cell--clickable:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  border-radius: 4px;
}
</style>
