import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function useLocations() {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const listQuery = useQuery({
    queryKey: ["locations"],
    queryFn: async () => {
      const { data } = await api.get("/locations/list");
      return data;
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/locations/create", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["locations"] });
      mainStore.showSnackbar("Location created", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to create location",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) =>
      api.put(`/locations/update/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["locations"] });
      mainStore.showSnackbar("Location updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update location",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/locations/delete/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["locations"] });
      mainStore.showSnackbar("Location deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete location",
        "error",
      ),
  });

  return { ...listQuery, createMutation, updateMutation, deleteMutation };
}
