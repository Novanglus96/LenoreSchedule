<template>
  <v-card variant="outlined" height="100%">
    <v-card-title class="d-flex align-center gap-2 py-3 px-4">
      <v-icon :icon="icon" :color="iconColor" size="20" />
      <span class="text-body-1 font-weight-bold">{{ title }}</span>
      <v-spacer />
      <slot name="actions" />
    </v-card-title>
    <v-divider />
    <v-card-text class="pa-4">
      <slot />
    </v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  icon: { type: String, required: true },
  iconColor: { type: String, default: "primary" },
});
</script>
