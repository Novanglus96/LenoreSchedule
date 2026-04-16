<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5" lg="4">
        <v-card elevation="8" rounded="lg">
          <v-card-item class="text-center pt-6 pb-2">
            <v-img
              src="/logov2.png"
              height="80"
              contain
              class="mx-auto mb-2"
            />
            <v-card-title class="text-h5 font-weight-bold">
              LenoreSchedule
            </v-card-title>
            <v-card-subtitle>Sign in to continue</v-card-subtitle>
          </v-card-item>

          <v-card-text class="px-6 pb-6">
            <v-form ref="formRef" @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                density="comfortable"
                autocomplete="username"
                :rules="[(v) => !!v || 'Username is required']"
                :disabled="loading"
                class="mb-3"
              />

              <v-text-field
                v-model="password"
                label="Password"
                prepend-inner-icon="mdi-lock-outline"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                density="comfortable"
                autocomplete="current-password"
                :rules="[(v) => !!v || 'Password is required']"
                :disabled="loading"
              />

              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                density="compact"
                class="mb-4 mt-1"
                closable
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mt-2"
              >
                Sign In
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const formRef = ref(null);
const username = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");

async function handleLogin() {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  loading.value = true;
  errorMessage.value = "";

  try {
    await authStore.login(username.value, password.value);
    const redirect = route.query.redirect || "/";
    router.push(redirect);
  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = "Invalid username or password.";
    } else {
      errorMessage.value = "Unable to connect. Please try again.";
    }
  } finally {
    loading.value = false;
  }
}
</script>
