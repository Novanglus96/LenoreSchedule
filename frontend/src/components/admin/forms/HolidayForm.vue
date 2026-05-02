<template>
  <v-row dense>
    <v-col cols="12">
      <v-text-field
        v-model="holidayName"
        label="Holiday Name"
        :error-messages="errors.holiday_name"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-select
        v-model="ruleType"
        label="Rule Type"
        :items="RULE_TYPE_OPTIONS"
        :error-messages="errors.rule_type"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-select
        v-model="observedRule"
        label="Observed Rule"
        :items="OBSERVED_RULE_OPTIONS"
        :error-messages="errors.observed_rule"
        variant="outlined"
        density="comfortable"
      />
    </v-col>

    <!-- fixed_date: month + day -->
    <template v-if="ruleType === 'fixed_date'">
      <v-col cols="12" sm="6">
        <v-select
          v-model="month"
          label="Month"
          :items="MONTH_OPTIONS"
          :error-messages="errors.month"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="day"
          label="Day of Month"
          type="number"
          min="1"
          max="31"
          :error-messages="errors.day"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
    </template>

    <!-- nth_weekday: month + weekday + week -->
    <template v-if="ruleType === 'nth_weekday'">
      <v-col cols="12" sm="4">
        <v-select
          v-model="month"
          label="Month"
          :items="MONTH_OPTIONS"
          :error-messages="errors.month"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col cols="12" sm="4">
        <v-select
          v-model="weekday"
          label="Weekday"
          :items="WEEKDAY_OPTIONS"
          :error-messages="errors.weekday"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col cols="12" sm="4">
        <v-select
          v-model="week"
          label="Week of Month"
          :items="WEEK_OPTIONS"
          :error-messages="errors.week"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
    </template>

    <!-- last_weekday: month + weekday -->
    <template v-if="ruleType === 'last_weekday'">
      <v-col cols="12" sm="6">
        <v-select
          v-model="month"
          label="Month"
          :items="MONTH_OPTIONS"
          :error-messages="errors.month"
          variant="outlined"
          density="comfortable"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-select
          v-model="weekday"
          label="Last Weekday"
          :items="WEEKDAY_OPTIONS"
          :error-messages="errors.weekday"
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

const RULE_TYPE_OPTIONS = [
  { title: "Fixed Date (e.g. Jul 4)", value: "fixed_date" },
  { title: "Nth Weekday of Month (e.g. 3rd Monday)", value: "nth_weekday" },
  { title: "Last Weekday of Month", value: "last_weekday" },
  { title: "Custom", value: "custom" },
];

const OBSERVED_RULE_OPTIONS = [
  { title: "None", value: "none" },
  { title: "Next Business Day", value: "next_business_day" },
  { title: "Nearest Weekday", value: "nearest_weekday" },
];

const MONTH_OPTIONS = [
  { title: "January", value: 1 },
  { title: "February", value: 2 },
  { title: "March", value: 3 },
  { title: "April", value: 4 },
  { title: "May", value: 5 },
  { title: "June", value: 6 },
  { title: "July", value: 7 },
  { title: "August", value: 8 },
  { title: "September", value: 9 },
  { title: "October", value: 10 },
  { title: "November", value: 11 },
  { title: "December", value: 12 },
];

const WEEKDAY_OPTIONS = [
  { title: "Monday", value: 0 },
  { title: "Tuesday", value: 1 },
  { title: "Wednesday", value: 2 },
  { title: "Thursday", value: 3 },
  { title: "Friday", value: 4 },
  { title: "Saturday", value: 5 },
  { title: "Sunday", value: 6 },
];

const WEEK_OPTIONS = [
  { title: "1st", value: 1 },
  { title: "2nd", value: 2 },
  { title: "3rd", value: 3 },
  { title: "4th", value: 4 },
  { title: "5th", value: 5 },
];

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    holiday_name: (v) => (v?.trim() ? true : "Holiday name is required"),
    rule_type: (v) => (v ? true : "Rule type is required"),
  },
  initialValues: {
    holiday_name: "",
    rule_type: "fixed_date",
    observed_rule: "none",
    month: null,
    day: null,
    weekday: null,
    week: null,
  },
});

const { value: holidayName } = useField("holiday_name");
const { value: ruleType } = useField("rule_type");
const { value: observedRule } = useField("observed_rule");
const { value: month } = useField("month");
const { value: day } = useField("day");
const { value: weekday } = useField("weekday");
const { value: week } = useField("week");

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      setValues({
        holiday_name: val.holiday_name ?? "",
        rule_type: val.rule_type ?? "fixed_date",
        observed_rule: val.observed_rule ?? "none",
        month: val.month ?? null,
        day: val.day ?? null,
        weekday: val.weekday ?? null,
        week: val.week ?? null,
      });
    } else {
      resetForm();
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  const payload = {
    holiday_name: values.holiday_name.trim(),
    rule_type: values.rule_type,
    observed_rule: values.observed_rule || "none",
    month: values.month ? parseInt(values.month) : null,
    day: values.day ? parseInt(values.day) : null,
    weekday: values.weekday != null ? parseInt(values.weekday) : null,
    week: values.week ? parseInt(values.week) : null,
  };
  emit("submit", payload);
});

defineExpose({ submit });
</script>
