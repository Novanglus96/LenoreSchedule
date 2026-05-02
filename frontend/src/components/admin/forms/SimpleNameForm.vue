<template>
  <v-text-field
    v-model="nameValue"
    :label="fieldLabel"
    :error-messages="errors.name"
    variant="outlined"
    density="comfortable"
    autofocus
  />
</template>

<script setup>
import { watch } from "vue";
import { useForm, useField } from "vee-validate";

const props = defineProps({
  modelValue: { type: Object, default: null },
  fieldLabel: { type: String, required: true },
  fieldKey: { type: String, required: true },
});

const emit = defineEmits(["submit"]);

const { handleSubmit, errors, resetForm, setValues } = useForm({
  validationSchema: {
    name: (val) => (val?.trim() ? true : `${props.fieldLabel} is required`),
  },
  initialValues: { name: "" },
});

const { value: nameValue } = useField("name");

watch(
  () => props.modelValue,
  (val) => {
    if (val) setValues({ name: val[props.fieldKey] ?? "" });
    else resetForm();
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  emit("submit", { [props.fieldKey]: values.name.trim() });
});

defineExpose({ submit });
</script>
