<template>
  <div>
    <v-navigation-drawer color="primary" permanent v-if="mdAndUp">
      <v-list density="compact" nav>
        <div class="d-flex flex-column align-center">
          <v-img :width="200" aspect-ratio="1/1" cover src="logov2.png"></v-img>
          <span class="text-caption font-weight-bold">v{{ version }}</span>
        </div>
        <v-list-item
          prepend-icon="mdi-view-dashboard-variant"
          v-bind="props"
          color="selected"
          @click="setAccount(null, True)"
          title="Dashboard"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar color="surface" density="compact">
      <template v-slot:prepend>
        <v-menu v-if="isMobile" width="200">
          <template v-slot:activator="{ props }">
            <v-app-bar-nav-icon v-bind="props"></v-app-bar-nav-icon>
          </template>
          <v-list>
            <v-list-item
              prepend-icon="mdi-view-dashboard-variant"
              color="selected"
              @click="setAccount(null, True)"
              title="Dashboard"
            ></v-list-item>
          </v-list>
        </v-menu>
      </template>
      <v-btn
        icon="mdi-theme-light-dark"
        @click="handleToggle"
        :color="isDark ? '#F5F5F5' : '#121212'"
        size="small"
      ></v-btn>
    </v-app-bar>
  </div>
</template>
<script setup>
import { watch, computed } from "vue";
import { useDisplay, useTheme } from "vuetify";
import { useThemeStore } from "@/stores/themeStore";

const theme = useTheme();
const themeStore = useThemeStore();

theme.change(themeStore.currentTheme);

const isDark = computed({
  get: () => themeStore.currentTheme === "myCustomDarkTheme",
  set: value => {
    themeStore.setTheme(value ? "myCustomDarkTheme" : "myCustomLightTheme");
  },
});

const version = import.meta.env.VITE_APP_VERSION;

const { mdAndUp, smAndDown } = useDisplay();
const isMobile = smAndDown;

watch(
  () => themeStore.currentTheme,
  newTheme => {
    theme.change(newTheme);
  },
);

function handleToggle() {
  themeStore.toggleTheme();
}
</script>
