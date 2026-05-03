<template>
  <v-row dense>
    <v-col cols="12">
      <v-select
        v-model="entryType"
        label="Type"
        :items="ENTRY_TYPE_OPTIONS"
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
    <v-col cols="12">
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

const props = defineProps({
  modelValue: { type: Object, default: null },
});
const emit = defineEmits(["submit"]);

const { data: locations, isLoading: locationsLoading } = useLocations();

const locationItems = computed(
  () =>
    locations.value?.map((l) => ({
      title: l.location_name,
      value: l.id,
    })) ?? [],
);

const ENTRY_TYPE_OPTIONS = [
  { title: "Scheduled", value: "scheduled" },
  { title: "Overtime", value: "overtime" },
  { title: "Shift Swap", value: "swap" },
  { title: "Vacation", value: "vacation" },
  { title: "Sick", value: "sick" },
  { title: "Personal", value: "personal" },
  { title: "Holiday", value: "holiday" },
  { title: "Floating Holiday", value: "floating_holiday" },
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
    entry_type: "scheduled",
    start_time: "",
    end_time: "",
    location_id: null,
    notes: "",
    confirmed: false,
  },
});

const { value: entryType } = useField("entry_type");
const { value: startTime } = useField("start_time");
const { value: endTime } = useField("end_time");
const { value: locationId } = useField("location_id");
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
    notes: values.notes || null,
    confirmed: values.confirmed,
  });
});

defineExpose({ submit });
</script>
