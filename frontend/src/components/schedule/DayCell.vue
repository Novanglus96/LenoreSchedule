<template>
  <div
    class="day-cell pa-1 d-flex flex-column align-center"
    :class="{ 'day-cell--staff': isStaff }"
    @click="isStaff && emit('click-day')"
  >
    <div v-if="entries.length === 0" class="text-caption text-disabled">—</div>
    <div v-for="(entry, i) in entries" :key="i" class="entry-block mb-1">
      <v-chip
        :color="chipColor(entry)"
        :variant="chipVariant(entry)"
        size="x-small"
        :title="chipTitle(entry)"
        :class="{ 'cursor-pointer': isStaff }"
        @click="handleChipClick(entry, $event)"
      >
        <span class="text-truncate" style="max-width: 110px">
          {{ chipLabel(entry) }}
        </span>
        <v-icon
          v-if="isStaff && entry.source === 'calendar'"
          size="10"
          class="ml-1"
          icon="mdi-pencil"
        />
      </v-chip>
      <div v-if="locationLabel(entry)" class="location-label">
        {{ locationLabel(entry) }}
      </div>
      <div v-if="entry.notes && entry.source === 'calendar'" class="notes-label">
        {{ entry.notes }}
      </div>
    </div>
    <v-btn
      v-if="isStaff"
      class="add-btn"
      icon
      size="x-small"
      variant="flat"
      color="primary"
      title="Add override"
      @click.stop="emit('click-day')"
    >
      <v-icon size="12">mdi-plus</v-icon>
    </v-btn>
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
  if (entry.start_time && entry.end_time) {
    const hours = calcHours(entry.start_time, entry.end_time, entry.break_minutes || 0);
    const timeStr = `${fmtTime(entry.start_time)} – ${fmtTime(entry.end_time)}`;
    const base = hours ? `${timeStr} (${hours})` : timeStr;
    return entry.entry_type ? `${base} · ${entry.entry_type}` : base;
  }
  return entry.entry_type || "—";
}

function locationLabel(entry) {
  // Location is only relevant for calendar overrides, not templates or holidays
  if (entry.source !== "calendar") return null;
  if (!entry.location) return null;
  // Hide when entry location matches the employee's default location
  if (props.defaultLocationId !== null && entry.location.id === props.defaultLocationId) return null;
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

function calcHours(startTime, endTime, breakMinutes = 0) {
  if (!startTime || !endTime) return null;
  const [sh, sm] = startTime.split(":").map(Number);
  const [eh, em] = endTime.split(":").map(Number);
  const totalMinutes = eh * 60 + em - (sh * 60 + sm) - breakMinutes;
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
  position: relative;
  min-width: 90px;
}
.day-cell--staff {
  cursor: pointer;
}
.day-cell--staff:hover {
  background: rgba(var(--v-theme-primary), 0.04);
  border-radius: 4px;
}
.add-btn {
  opacity: 0;
  transition: opacity 0.15s;
  width: 18px !important;
  height: 18px !important;
}
.day-cell--staff:hover .add-btn {
  opacity: 1;
}
.entry-block {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.location-label {
  font-size: 10px;
  line-height: 1.3;
  color: rgb(var(--v-theme-primary));
  margin-top: 1px;
}
.notes-label {
  font-size: 10px;
  line-height: 1.3;
  color: rgba(var(--v-theme-on-surface), 0.55);
  margin-top: 1px;
  font-style: italic;
  max-width: 110px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
