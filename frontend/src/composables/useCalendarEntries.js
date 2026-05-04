import { useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function useCalendarEntries() {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/calendar/create_entry", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
      mainStore.showSnackbar("Override added", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to add override",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) =>
      api.put(`/calendar/update_entry/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
      mainStore.showSnackbar("Override updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update override",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/calendar/delete_entry/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
      mainStore.showSnackbar("Override deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete override",
        "error",
      ),
  });

  const confirmWeekMutation = useMutation({
    mutationFn: (payload) => api.post("/calendar/confirm_week", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
      mainStore.showSnackbar("All overrides confirmed", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to confirm overrides",
        "error",
      ),
  });

  return { createMutation, updateMutation, deleteMutation, confirmWeekMutation };
}
