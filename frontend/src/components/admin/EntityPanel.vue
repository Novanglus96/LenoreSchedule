<template>
  <div>
    <div class="d-flex align-center mb-3">
      <h2 class="text-h6">{{ title }}</h2>
      <v-spacer />
      <v-btn
        prepend-icon="mdi-plus"
        color="primary"
        variant="flat"
        size="small"
        @click="$emit('new')"
      >
        New {{ title.replace(/s$/, "") }}
      </v-btn>
    </div>

    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-2" />

    <v-table density="compact" class="rounded border">
      <thead>
        <tr>
          <th v-for="h in headers" :key="h.key" class="text-left">
            {{ h.label }}
          </th>
          <th class="text-right" style="width: 96px">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!items.length && !loading">
          <td :colspan="headers.length + 1" class="text-center text-disabled py-4">
            No records found.
          </td>
        </tr>
        <tr v-for="item in items" :key="item.id">
          <td v-for="h in headers" :key="h.key">
            {{ cellValue(h.key, item) }}
          </td>
          <td class="text-right">
            <v-btn
              icon="mdi-pencil"
              size="x-small"
              variant="text"
              @click="$emit('edit', item)"
            />
            <v-btn
              icon="mdi-delete"
              size="x-small"
              variant="text"
              color="error"
              @click="$emit('delete', item)"
            />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, required: true },
  headers: { type: Array, required: true },
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  cellFormatter: { type: Function, default: null },
});

defineEmits(["new", "edit", "delete"]);

function cellValue(key, item) {
  if (props.cellFormatter) {
    const formatted = props.cellFormatter(key, item);
    if (formatted !== null) return formatted;
  }
  const val = item[key];
  return val ?? "—";
}
</script>
