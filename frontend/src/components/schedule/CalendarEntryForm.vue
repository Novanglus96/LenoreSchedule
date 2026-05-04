<template>
  <v-row dense>
    <v-col cols="12">
      <v-select
        v-model="entryType"
        label="Type"
        :items="entryTypeItems"
        :loading="entryTypesLoading"
        :error-messages="errors.entry_type"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="startTime"
        label="Start Time (leave blank for full day)"
        type="time"
        :error-messages="errors.start_time"
        variant="outlined"
        density="comfortable"
        clearable
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="endTime"
        label="End Time"
        type="time"
        :error-messages="errors.end_time"
        variant="outlined"
        density="comfortable"
        clearable
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-select
        v-model="locationId"
        label="Location (optional)"
        :items="locationItems"
        :error-messages="errors.location_id"
        variant="outlined"
        density="comfortable"
        :loading="locationsLoading"
        clearable
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-select
        v-model="breakMinutes"
        label="Break"
        :items="BREAK_OPTIONS"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12">
      <v-textarea
        v-model="notes"
        label="Notes (optional)"
        :error-messages="errors.notes"
        variant="outlined"
        density="comfortable"
        rows="2"
        auto-grow
      />
    </v-col>
    <v-col cols="12">
      <v-checkbox
        v-model="confirmed"
        label="Confirmed"
        density="comfortable"
        hide-details
      />
    </v-col>
  </v-row>
</template>

<script setup>
import { computed, watch } from "vue";
import { useForm, useField } from "vee-validate";
import { useLocations } from "@/composables/useLocations.js";
import { useEntryTypes } from "@/composables/useEntryTypes.js";

const props = defineProps({
  modelValue: { type: Object, default: null },
});
const emit = defineEmits(["submit"]);

const { data: locations, isLoading: locationsLoading } = useLocations();
const { data: entryTypeData, isLoading: entryTypesLoading } = useEntryTypes();

const locationItems = computed(
  () =>
    locations.value?.map((l) => ({
      title: l.location_name,
      value: l.id,
    })) ?? [],
);

const entryTypeItems = computed(
  () =>
    entryTypeData.value?.map((t) => ({
      title: `${t.code} – ${t.name}`,
      value: t.code,
    })) ?? [],
);

const BREAK_OPTIONS = [
  { title: "No break", value: 0 },
  { title: "15 min", value: 15 },
  { title: "30 min", value: 30 },
  { title: "45 min", value: 45 },
  { title: "1 hr", value: 60 },
  { title: "1 hr 15 min", value: 75 },
  { title: "1 hr 30 min", value: 90 },
  { title: "1 hr 45 min", value: 105 },
  { title: "2 hr", value: 120 },
];

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    entry_type: (v) => (v ? true : "Type is required"),
    start_time: (v, ctx) => {
      if (!v) return true;
      if (!ctx.form.end_time) return "End time is required when start time is set";
      return true;
    },
    end_time: (v, ctx) => {
      if (!v) return true;
      if (!ctx.form.start_time) return "Start time is required when end time is set";
      if (v <= ctx.form.start_time) return "End time must be after start time";
      return true;
    },
  },
  initialValues: {
    entry_type: "SCH",
    start_time: "",
    end_time: "",
    location_id: null,
    break_minutes: 0,
    notes: "",
    confirmed: false,
  },
});

const { value: entryType } = useField("entry_type");
const { value: startTime } = useField("start_time");
const { value: endTime } = useField("end_time");
const { value: locationId } = useField("location_id");
const { value: breakMinutes } = useField("break_minutes");
const { value: notes } = useField("notes");
const { value: confirmed } = useField("confirmed");

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      setValues({
        entry_type: val.entry_type ?? "scheduled",
        start_time: val.start_time ?? "",
        end_time: val.end_time ?? "",
        location_id: val.location?.id ?? val.location_id ?? null,
        break_minutes: val.break_minutes ?? 0,
        notes: val.notes ?? "",
        confirmed: val.confirmed ?? false,
      });
    } else {
      resetForm();
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  emit("submit", {
    entry_type: values.entry_type,
    start_time: values.start_time || null,
    end_time: values.end_time || null,
    location_id: values.location_id ?? null,
    break_minutes: values.break_minutes ?? 0,
    notes: values.notes || null,
    confirmed: values.confirmed,
  });
});

defineExpose({ submit });
</script>
