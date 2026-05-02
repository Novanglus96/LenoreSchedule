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
    <v-col cols="12" sm="4">
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
import { computed, watch } from "vue";
import { useForm, useField } from "vee-validate";
import { useEmployees } from "@/composables/useEmployees.js";
import { useLocations } from "@/composables/useLocations.js";

const props = defineProps({
  modelValue: { type: Object, default: null },
  preselectedEmployeeId: { type: Number, default: null },
});
const emit = defineEmits(["submit"]);

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
  { title: "Monday", value: 0 },
  { title: "Tuesday", value: 1 },
  { title: "Wednesday", value: 2 },
  { title: "Thursday", value: 3 },
  { title: "Friday", value: 4 },
  { title: "Saturday", value: 5 },
  { title: "Sunday", value: 6 },
];

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    employee_id: (v) => (v != null ? true : "Employee is required"),
    day_of_week: (v) => (v != null ? true : "Day of week is required"),
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
      if (props.preselectedEmployeeId) {
        setValues({ employee_id: props.preselectedEmployeeId });
      }
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  emit("submit", {
    employee_id: values.employee_id,
    day_of_week: values.day_of_week,
    start_time: values.start_time,
    end_time: values.end_time,
    location_id: values.location_id ?? null,
  });
});

defineExpose({ submit });
</script>
