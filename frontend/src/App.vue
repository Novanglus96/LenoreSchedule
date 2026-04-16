<template>
  <v-app>
    <!-- Loading: backend not yet up or auth not yet resolved -->
    <LogoLoader
      v-if="!appReady"
      logo="/logov2.png"
      :size="150"
      :duration="5"
      :opacity="0.8"
      direction="alternate"
      :messages="['Funny loading message...']"
    />

    <!-- Unauthenticated layout (login page) -->
    <template v-else-if="!authStore.isAuthenticated">
      <v-main class="bg-background">
        <router-view />
      </v-main>
    </template>

    <!-- Authenticated layout -->
    <template v-else>
      <VueQueryDevtools button-position="bottom-left" />
      <AppNavigationVue />
      <v-main>
        <v-container class="bg-background h-100" fluid>
          <router-view />
        </v-container>
        <v-snackbar
          v-model="mainstore.snackbar"
          :color="mainstore.snackbarColor"
          :timeout="mainstore.snackbarTimeout"
          content-class="centered-text"
        >
          {{ mainstore.snackbarText }}
        </v-snackbar>
        <v-snackbar
          v-model="showBanner"
          color="primary"
          location="top"
          timeout="-1"
          :multi-line="true"
        >
          There's been an update to the application. Click refresh to get the
          new changes!
          <template v-slot:actions>
            <v-btn color="secondary" variant="text" @click="showBanner = false">
              Close
            </v-btn>
            <v-btn color="secondary" variant="text" @click="reloadPage">
              Refresh
            </v-btn>
          </template>
        </v-snackbar>
      </v-main>
    </template>
  </v-app>
</template>

<script setup>
import AppNavigationVue from "@/views/AppNavigationVue.vue";
import { useMainStore } from "@/stores/main";
import { useAuthStore } from "@/stores/authStore";
import { onMounted, computed, ref, watch, onUnmounted } from "vue";
import { useVersion } from "@/composables/versionComposable";
import { VueQueryDevtools } from "@tanstack/vue-query-devtools";
import { useBackendReady } from "@/composables/useBackendReady";
import { useRouter, useRoute } from "vue-router";
import LogoLoader from "./components/LogoLoader.vue";

const { backendReady } = useBackendReady();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const appReady = ref(false);

// After the backend is confirmed up, resolve auth state then redirect if needed
// before revealing the app — prevents the login flash on page reload
watch(backendReady, async (ready) => {
  if (ready) {
    await authStore.fetchMe();

    if (route.meta?.requiresAuth && !authStore.isAuthenticated) {
      await router.replace({ name: "login", query: { redirect: route.fullPath } });
    } else if (route.name === "login" && authStore.isAuthenticated) {
      const dest = route.query.redirect || "/";
      await router.replace(dest);
    }

    appReady.value = true;
  }
});

const reloadPage = () => {
  window.location.reload();
};
const mainstore = useMainStore();
const { prefetchVersion, version } = useVersion();
const showBanner = ref(false);

const checkVersion = computed(() => {
  return (
    version.value &&
    version.value.version_number !== import.meta.env.VITE_APP_VERSION
  );
});

const updateBanner = () => {
  showBanner.value = checkVersion.value;
};

onMounted(() => {
  prefetchVersion();
  updateBanner();

  const handleVisibilityChange = () => {
    if (!document.hidden) {
      prefetchVersion().then(() => {
        updateBanner();
      });
    }
  };

  document.addEventListener("visibilitychange", handleVisibilityChange);

  onUnmounted(() => {
    document.removeEventListener("visibilitychange", handleVisibilityChange);
  });
});

watch(checkVersion, (newValue) => {
  showBanner.value = newValue;
});
</script>

<style>
.loading-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 1.5rem;
}
</style>
