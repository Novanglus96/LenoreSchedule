<template>
  <v-row dense>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="firstName"
        label="First Name"
        :error-messages="errors.first_name"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="lastName"
        label="Last Name"
        :error-messages="errors.last_name"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12">
      <v-text-field
        v-model="email"
        label="Email"
        type="email"
        :error-messages="errors.email"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="4">
      <v-select
        v-model="divisionId"
        label="Division"
        :items="divisions || []"
        item-title="division_name"
        item-value="id"
        :error-messages="errors.division_id"
        variant="outlined"
        density="comfortable"
        :loading="divisionsLoading"
      />
    </v-col>
    <v-col cols="12" sm="4">
      <v-select
        v-model="groupId"
        label="Group"
        :items="groups || []"
        item-title="group_name"
        item-value="id"
        :error-messages="errors.group_id"
        variant="outlined"
        density="comfortable"
        :loading="groupsLoading"
      />
    </v-col>
    <v-col cols="12" sm="4">
      <v-select
        v-model="locationId"
        label="Location"
        :items="locations || []"
        item-title="location_name"
        item-value="id"
        :error-messages="errors.location_id"
        variant="outlined"
        density="comfortable"
        :loading="locationsLoading"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="startDate"
        label="Start Date"
        type="date"
        :error-messages="errors.start_date"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
    <v-col cols="12" sm="6">
      <v-text-field
        v-model="endDate"
        label="End Date"
        type="date"
        :error-messages="errors.end_date"
        variant="outlined"
        density="comfortable"
      />
    </v-col>
  </v-row>
</template>

<script setup>
import { watch } from "vue";
import { useForm, useField } from "vee-validate";
import { useGroups } from "@/composables/useGroups.js";
import { useDivisions } from "@/composables/useDivisions.js";
import { useLocations } from "@/composables/useLocations.js";

const props = defineProps({
  modelValue: { type: Object, default: null },
});
const emit = defineEmits(["submit"]);

const { data: groups, isLoading: groupsLoading } = useGroups();
const { data: divisions, isLoading: divisionsLoading } = useDivisions();
const { data: locations, isLoading: locationsLoading } = useLocations();

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    first_name: (v) => (v?.trim() ? true : "First name is required"),
    last_name: (v) => (v?.trim() ? true : "Last name is required"),
    email: (v) => {
      if (!v?.trim()) return "Email is required";
      if (!EMAIL_RE.test(v)) return "Invalid email address";
      return true;
    },
    division_id: (v) => (v != null ? true : "Division is required"),
    group_id: (v) => (v != null ? true : "Group is required"),
    location_id: (v) => (v != null ? true : "Location is required"),
  },
  initialValues: {
    first_name: "",
    last_name: "",
    email: "",
    division_id: null,
    group_id: null,
    location_id: null,
    start_date: "",
    end_date: "",
  },
});

const { value: firstName } = useField("first_name");
const { value: lastName } = useField("last_name");
const { value: email } = useField("email");
const { value: divisionId } = useField("division_id");
const { value: groupId } = useField("group_id");
const { value: locationId } = useField("location_id");
const { value: startDate } = useField("start_date");
const { value: endDate } = useField("end_date");

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      setValues({
        first_name: val.first_name ?? "",
        last_name: val.last_name ?? "",
        email: val.email ?? "",
        division_id: val.division?.id ?? null,
        group_id: val.group?.id ?? null,
        location_id: val.location?.id ?? null,
        start_date: val.start_date ?? "",
        end_date: val.end_date ?? "",
      });
    } else {
      resetForm();
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  const payload = {
    first_name: values.first_name.trim(),
    last_name: values.last_name.trim(),
    email: values.email.trim(),
    division_id: values.division_id,
    group_id: values.group_id,
    location_id: values.location_id,
    start_date: values.start_date || null,
    end_date: values.end_date || null,
  };
  emit("submit", payload);
});

defineExpose({ submit });
</script>
