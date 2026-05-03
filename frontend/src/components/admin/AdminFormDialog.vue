<template>
  <v-dialog :model-value="open" :max-width="maxWidth" persistent>
    <v-card>
      <v-card-title class="pt-4 pb-2">{{ title }}</v-card-title>
      <v-card-text class="pb-0">
        <slot />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" :disabled="saving" @click="$emit('cancel')">
          Cancel
        </v-btn>
        <v-btn color="primary" variant="flat" :loading="saving" @click="$emit('save')">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
defineProps({
  open: { type: Boolean, required: true },
  title: { type: String, required: true },
  saving: { type: Boolean, default: false },
  maxWidth: { type: [String, Number], default: 560 },
});
defineEmits(["cancel", "save"]);
</script>
