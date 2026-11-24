<template>
  <v-row dense>
    <v-col cols="12" sm="8">
      <v-text-field
        v-model="name"
        label="Division Name"
        :error-messages="errors.division_name"
        variant="outlined"
        density="comfortable"
        autofocus
      />
    </v-col>
    <v-col cols="12" sm="4">
      <v-text-field
        v-model.number="sortOrder"
        label="Sort Order"
        type="number"
        min="0"
        :error-messages="errors.sort_order"
        variant="outlined"
        density="comfortable"
        hint="Lower numbers list first; ties sort by name"
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
    division_name: (v) => (v?.trim() ? true : "Division Name is required"),
    sort_order: (v) =>
      v === "" || v == null || (Number.isInteger(Number(v)) && Number(v) >= 0)
        ? true
        : "Must be a whole number, 0 or more",
  },
  initialValues: { division_name: "", sort_order: 0 },
});

const { value: name } = useField("division_name");
const { value: sortOrder } = useField("sort_order");

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      setValues({ division_name: val.division_name ?? "", sort_order: val.sort_order ?? 0 });
    } else {
      resetForm();
    }
  },
  { immediate: true },
);

const submit = handleSubmit((values) => {
  emit("submit", {
    division_name: values.division_name.trim(),
    sort_order: values.sort_order === "" || values.sort_order == null ? 0 : Number(values.sort_order),
  });
});

defineExpose({ submit });
</script>
