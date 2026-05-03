<template>
  <v-row dense>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="payrollYear"
        label="Payroll Year"
        type="number"
        :error-messages="errors.payroll_year"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="payrollStart"
        label="Payroll Start Date"
        type="date"
        :error-messages="errors.payroll_start"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-select
        v-model="payrollFrequency"
        label="Pay Frequency"
        :items="FREQUENCY_OPTIONS"
        :error-messages="errors.payroll_frequency"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-select
        v-model="weekStartDay"
        label="Week Starts On"
        :items="WEEK_START_OPTIONS"
        :error-messages="errors.week_start_day"
        variant="outlined"
        density="comfortable"
      />
    </v-col>

    <template v-if="payrollFrequency === 'monthly' || payrollFrequency === 'semi-monthly'">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="firstDay"
          label="First Pay Day of Month"
          type="number"
          min="1"
          max="31"
          :error-messages="errors.first_day"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
    </template>

    <template v-if="payrollFrequency === 'semi-monthly'">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="secondDay"
          label="Second Pay Day of Month"
          type="number"
          min="1"
          max="31"
          :error-messages="errors.second_day"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
    </template>
  </v-row>
</template>

<script setup>
import { watch } from "vue";
import { useForm, useField } from "vee-validate";

const props = defineProps({
  modelValue: { type: Object, default: null },
});
const emit = defineEmits(["submit"]);

const FREQUENCY_OPTIONS = [
  { title: "Weekly", value: "weekly" },
  { title: "Biweekly", value: "biweekly" },
  { title: "Semi-monthly", value: "semi-monthly" },
  { title: "Monthly", value: "monthly" },
  { title: "Quadriweekly", value: "quadriweekly" },
  { title: "Daily", value: "daily" },
];

const WEEK_START_OPTIONS = [
  { title: "Sunday", value: "sun" },
  { title: "Monday", value: "mon" },
];

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    payroll_year: (v) => {
      const n = parseInt(v);
      if (!v && v !== 0) return "Year is required";
      if (isNaN(n) || n < 2000 || n > 2100) return "Enter a valid year";
      return true;
    },
    payroll_start: (v) => (v ? true : "Start date is required"),
    payroll_frequency: (v) => (v ? true : "Frequency is required"),
    week_start_day: (v) => (v ? true : "Week start day is required"),
  },
  initialValues: {
    payroll_year: new Date().getFullYear(),
    payroll_start: "",
    payroll_frequency: "biweekly",
    week_start_day: "sun",
    first_day: null,
    second_day: null,
  },
});

const { value: payrollYear } = useField("payroll_year");
const { value: payrollStart } = useField("payroll_start");
const { value: payrollFrequency } = useField("payroll_frequency");
const { value: weekStartDay } = useField("week_start_day");
const { value: firstDay } = useField("first_day");
const { value: secondDay } = useField("second_day");

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      setValues({
        payroll_year: val.payroll_year,
        payroll_start: val.payroll_start ?? "",
        payroll_frequency: val.payroll_frequency ?? "biweekly",
        week_start_day: val.week_start_day ?? "sun",
        first_day: val.first_day ?? null,
        second_day: val.second_day ?? null,
      });
    } else {
      resetForm();
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  const payload = {
    payroll_year: parseInt(values.payroll_year),
    payroll_start: values.payroll_start,
    payroll_frequency: values.payroll_frequency,
    week_start_day: values.week_start_day,
    first_day: values.first_day ? parseInt(values.first_day) : null,
    second_day: values.second_day ? parseInt(values.second_day) : null,
  };
  emit("submit", payload);
});

defineExpose({ submit });
</script>
