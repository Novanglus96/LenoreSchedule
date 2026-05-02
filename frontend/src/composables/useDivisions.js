import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function useDivisions() {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const listQuery = useQuery({
    queryKey: ["divisions"],
    queryFn: async () => {
      const { data } = await api.get("/divisions/list");
      return data;
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/divisions/create", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["divisions"] });
      mainStore.showSnackbar("Division created", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to create division",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) =>
      api.put(`/divisions/update/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["divisions"] });
      mainStore.showSnackbar("Division updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update division",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/divisions/delete/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["divisions"] });
      mainStore.showSnackbar("Division deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete division",
        "error",
      ),
  });

  return { ...listQuery, createMutation, updateMutation, deleteMutation };
}
