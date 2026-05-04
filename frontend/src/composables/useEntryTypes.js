import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function useEntryTypes() {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const query = useQuery({
    queryKey: ["entryTypes"],
    queryFn: async () => {
      const { data } = await api.get("/entry_types");
      return data;
    },
    staleTime: 1000 * 60 * 10,
  });

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/entry_types", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entryTypes"] });
      mainStore.showSnackbar("Entry type created", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to create entry type",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) => api.put(`/entry_types/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entryTypes"] });
      mainStore.showSnackbar("Entry type updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update entry type",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/entry_types/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entryTypes"] });
      mainStore.showSnackbar("Entry type deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete entry type",
        "error",
      ),
  });

  return { ...query, createMutation, updateMutation, deleteMutation };
}
