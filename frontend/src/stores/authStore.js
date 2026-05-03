import { defineStore } from "pinia";
import api from "@/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null, // { username, is_staff, divisions: [id, ...] }
    initialized: false, // true once fetchMe() has completed at least once
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
    username: (state) => state.user?.username ?? "",
    isStaff: (state) => state.user?.is_staff ?? false,
    divisions: (state) => state.user?.divisions ?? [],
  },

  actions: {
    async fetchMe() {
      try {
        const { data } = await api.get("/accounts/auth/me");
        this.user = data;
      } catch {
        this.user = null;
      } finally {
        this.initialized = true;
      }
    },

    async login(username, password) {
      await api.post("/accounts/auth/login", { username, password });
      await this.fetchMe();
    },

    async logout() {
      try {
        await api.post("/accounts/auth/logout");
      } finally {
        this.user = null;
      }
    },
  },
});
