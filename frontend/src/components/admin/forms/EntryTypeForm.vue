<template>
  <v-row dense>
    <v-col cols="12" sm="8">
      <v-text-field
        v-model="name"
        label="Name"
        :error-messages="errors.name"
        variant="outlined"
        density="comfortable"
        autofocus
      />
    </v-col>
    <v-col cols="12" sm="4">
      <v-text-field
        v-model="code"
        label="Code (3 letters)"
        :error-messages="errors.code"
        variant="outlined"
        density="comfortable"
        maxlength="3"
        hint="Displayed on schedule and PDF"
        persistent-hint
      />
    </v-col>
  </v-row>
</template>

<script setup>
import { watch } from "vue";
import { useForm, useField } from "vee-validate";

const props = defineProps({
  modelValue: { type: Object, default: null },
});
const emit = defineEmits(["submit"]);

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    name: (v) => (v?.trim() ? true : "Name is required"),
    code: (v) => {
      if (!v?.trim()) return "Code is required";
      if (v.trim().length > 3) return "Code must be 3 characters or fewer";
      return true;
    },
  },
  initialValues: { name: "", code: "" },
});

const { value: name } = useField("name");
const { value: code } = useField("code");

watch(
  () => props.modelValue,
  (val) => {
    if (val) setValues({ name: val.name ?? "", code: val.code ?? "" });
    else resetForm();
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  emit("submit", { name: values.name.trim(), code: values.code.trim().toUpperCase() });
});

defineExpose({ submit });
</script>
