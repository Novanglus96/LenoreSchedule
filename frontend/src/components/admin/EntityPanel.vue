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
          <th v-if="reorderable" style="width: 32px" />
          <th v-for="h in headers" :key="h.key" class="text-left">
            {{ h.label }}
          </th>
          <th class="text-right" style="width: 96px">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!items.length && !loading">
          <td :colspan="headers.length + (reorderable ? 2 : 1)" class="text-center text-disabled py-4">
            No records found.
          </td>
        </tr>
        <tr
          v-for="(item, index) in items"
          :key="item.id"
          :draggable="reorderable"
          :class="{
            'drag-source': reorderable && dragIndex === index,
            'drop-before': reorderable && overIndex === index && dragIndex > index,
            'drop-after': reorderable && overIndex === index && dragIndex < index,
          }"
          @dragstart="onDragStart($event, index)"
          @dragover="onDragOver($event, index)"
          @drop="onDrop($event, index)"
          @dragend="resetDrag"
        >
          <td v-if="reorderable" class="drag-handle" title="Drag to reorder">
            <v-icon icon="mdi-drag-vertical" size="small" />
          </td>
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
import { ref } from "vue";

const props = defineProps({
  title: { type: String, required: true },
  headers: { type: Array, required: true },
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  cellFormatter: { type: Function, default: null },
  // Rows can be dragged; emits `reorder` with every item id in the new order.
  reorderable: { type: Boolean, default: false },
});

const emit = defineEmits(["new", "edit", "delete", "reorder"]);

const dragIndex = ref(null);
const overIndex = ref(null);

function onDragStart(event, index) {
  if (!props.reorderable) return;
  dragIndex.value = index;
  event.dataTransfer.effectAllowed = "move";
  // Firefox will not start a drag without data.
  event.dataTransfer.setData("text/plain", String(props.items[index].id));
}

function onDragOver(event, index) {
  if (dragIndex.value === null) return;
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
  overIndex.value = index;
}

function onDrop(event, index) {
  if (dragIndex.value === null) return;
  event.preventDefault();
  const from = dragIndex.value;
  resetDrag();
  if (from === index) return;
  const ids = props.items.map((i) => i.id);
  const [moved] = ids.splice(from, 1);
  ids.splice(index, 0, moved);
  emit("reorder", ids);
}

function resetDrag() {
  dragIndex.value = null;
  overIndex.value = null;
}

function cellValue(key, item) {
  if (props.cellFormatter) {
    const formatted = props.cellFormatter(key, item);
    if (formatted !== null) return formatted;
  }
  const val = item[key];
  return val ?? "—";
}
</script>

<style scoped>
.drag-handle {
  cursor: grab;
  color: rgba(var(--v-theme-on-surface), 0.5);
}
tr[draggable="true"]:active .drag-handle {
  cursor: grabbing;
}
.drag-source {
  opacity: 0.4;
}
.drop-before td {
  box-shadow: inset 0 2px 0 rgb(var(--v-theme-primary));
}
.drop-after td {
  box-shadow: inset 0 -2px 0 rgb(var(--v-theme-primary));
}
</style>
