<template>
  <v-row dense>
    <v-col cols="12">
      <v-select
        v-model="employeeId"
        label="Employee"
        :items="employeeItems"
        :error-messages="errors.employee_id"
        variant="outlined"
        density="comfortable"
        :loading="employeesLoading"
      />
    </v-col>

    <!-- Create mode: multi-day checkboxes -->
    <v-col v-if="!isEditing" cols="12">
      <div class="text-body-2 mb-1">Days of Week</div>
      <div class="d-flex flex-wrap gap-x-2">
        <v-checkbox
          v-for="day in DAY_OPTIONS"
          :key="day.value"
          v-model="selectedDays"
          :label="day.title"
          :value="day.value"
          density="comfortable"
          hide-details
          class="mr-1"
        />
      </div>
      <div v-if="daysError" class="text-error text-caption mt-1">{{ daysError }}</div>
    </v-col>

    <!-- Edit mode: single day select -->
    <v-col v-else cols="12" sm="4">
      <v-select
        v-model="dayOfWeek"
        label="Day of Week"
        :items="DAY_OPTIONS"
        :error-messages="errors.day_of_week"
        variant="outlined"
        density="comfortable"
      />
    </v-col>

    <v-col cols="12" sm="4">
      <v-text-field
        v-model="startTime"
        label="Start Time"
        type="time"
        :error-messages="errors.start_time"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="4">
      <v-text-field
        v-model="endTime"
        label="End Time"
        type="time"
        :error-messages="errors.end_time"
        variant="outlined"
        density="comfortable"
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
  </v-row>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useForm, useField } from "vee-validate";
import { useEmployees } from "@/composables/useEmployees.js";
import { useLocations } from "@/composables/useLocations.js";

const props = defineProps({
  modelValue: { type: Object, default: null },
  preselectedEmployeeId: { type: Number, default: null },
});
const emit = defineEmits(["submit"]);

const isEditing = computed(() => props.modelValue != null);

const { data: employees, isLoading: employeesLoading } = useEmployees();
const { data: locations, isLoading: locationsLoading } = useLocations();

const employeeItems = computed(
  () =>
    employees.value?.map((e) => ({
      title: `${e.last_name}, ${e.first_name}`,
      value: e.id,
    })) ?? [],
);

const locationItems = computed(
  () =>
    locations.value?.map((l) => ({
      title: l.location_name,
      value: l.id,
    })) ?? [],
);

const DAY_OPTIONS = [
  { title: "Mon", value: 0 },
  { title: "Tue", value: 1 },
  { title: "Wed", value: 2 },
  { title: "Thu", value: 3 },
  { title: "Fri", value: 4 },
  { title: "Sat", value: 5 },
  { title: "Sun", value: 6 },
];

const selectedDays = ref([0, 1, 2, 3, 4]);
const daysError = ref("");

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    employee_id: (v) => (v != null ? true : "Employee is required"),
    day_of_week: (v) => {
      if (isEditing.value) return v != null ? true : "Day of week is required";
      return true;
    },
    start_time: (v) => (v ? true : "Start time is required"),
    end_time: (v) => (v ? true : "End time is required"),
  },
  initialValues: {
    employee_id: null,
    day_of_week: null,
    start_time: "",
    end_time: "",
    location_id: null,
  },
});

const { value: employeeId } = useField("employee_id");
const { value: dayOfWeek } = useField("day_of_week");
const { value: startTime } = useField("start_time");
const { value: endTime } = useField("end_time");
const { value: locationId } = useField("location_id");

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      setValues({
        employee_id: val.employee?.id ?? val.employee_id ?? null,
        day_of_week: val.day_of_week ?? null,
        start_time: val.start_time ?? "",
        end_time: val.end_time ?? "",
        location_id: val.location?.id ?? val.location_id ?? null,
      });
    } else {
      resetForm();
      selectedDays.value = [0, 1, 2, 3, 4];
      daysError.value = "";
      if (props.preselectedEmployeeId) {
        setValues({ employee_id: props.preselectedEmployeeId });
      }
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  if (!isEditing.value) {
    if (selectedDays.value.length === 0) {
      daysError.value = "Select at least one day";
      return;
    }
    daysError.value = "";
    emit("submit", {
      employee_id: values.employee_id,
      days_of_week: [...selectedDays.value].sort((a, b) => a - b),
      start_time: values.start_time,
      end_time: values.end_time,
      location_id: values.location_id ?? null,
    });
  } else {
    emit("submit", {
      employee_id: values.employee_id,
      day_of_week: values.day_of_week,
      start_time: values.start_time,
      end_time: values.end_time,
      location_id: values.location_id ?? null,
    });
  }
});

defineExpose({ submit });
</script>
