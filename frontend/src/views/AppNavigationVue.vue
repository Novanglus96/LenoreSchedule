<template>
  <div>
    <v-navigation-drawer color="primary" permanent v-if="mdAndUp">
      <v-list density="compact" nav class="d-flex flex-column h-100">
        <div class="d-flex flex-column align-center">
          <v-img :width="200" aspect-ratio="1/1" cover src="logov2.png"></v-img>
          <span class="text-caption font-weight-bold">v{{ version }}</span>
        </div>
        <v-list-item
          prepend-icon="mdi-view-dashboard-variant"
          color="selected"
          title="Dashboard"
        ></v-list-item>

        <v-spacer />

        <!-- User info + logout at the bottom -->
        <v-divider class="mb-2" />
        <v-list-item
          :prepend-icon="authStore.isStaff ? 'mdi-shield-account' : 'mdi-account'"
          :title="authStore.username"
          subtitle="Signed in"
          density="compact"
        />
        <v-list-item
          prepend-icon="mdi-logout"
          title="Sign Out"
          color="error"
          @click="handleLogout"
        />
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
              title="Dashboard"
            ></v-list-item>
            <v-divider />
            <v-list-item
              :prepend-icon="authStore.isStaff ? 'mdi-shield-account' : 'mdi-account'"
              :title="authStore.username"
              density="compact"
              disabled
            />
            <v-list-item
              prepend-icon="mdi-logout"
              title="Sign Out"
              @click="handleLogout"
            />
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
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const theme = useTheme();
const themeStore = useThemeStore();
const authStore = useAuthStore();
const router = useRouter();

theme.change(themeStore.currentTheme);

const isDark = computed({
  get: () => themeStore.currentTheme === "myCustomDarkTheme",
  set: (value) => {
    themeStore.setTheme(value ? "myCustomDarkTheme" : "myCustomLightTheme");
  },
});

const version = import.meta.env.VITE_APP_VERSION;

const { mdAndUp, smAndDown } = useDisplay();
const isMobile = smAndDown;

watch(
  () => themeStore.currentTheme,
  (newTheme) => {
    theme.change(newTheme);
  },
);

function handleToggle() {
  themeStore.toggleTheme();
}

async function handleLogout() {
  await authStore.logout();
  router.push({ name: "login" });
}
</script>
