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
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
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
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
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
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
      mainStore.showSnackbar("Division deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete division",
        "error",
      ),
  });

  // Drag-and-drop reorder. Applies the new order to the cached list at once so
  // the row does not jump back while the request is in flight; rolls back on
  // failure.
  const reorderMutation = useMutation({
    mutationFn: (divisionIds) =>
      api.post("/divisions/reorder", { division_ids: divisionIds }),
    onMutate: async (divisionIds) => {
      await queryClient.cancelQueries({ queryKey: ["divisions"] });
      const previous = queryClient.getQueryData(["divisions"]);
      if (previous) {
        const byId = new Map(previous.map((d) => [d.id, d]));
        queryClient.setQueryData(
          ["divisions"],
          divisionIds.map((id, i) => ({ ...byId.get(id), sort_order: i + 1 })),
        );
      }
      return { previous };
    },
    onError: (e, _ids, context) => {
      if (context?.previous) {
        queryClient.setQueryData(["divisions"], context.previous);
      }
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to reorder divisions",
        "error",
      );
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["divisions"] });
      queryClient.invalidateQueries({ queryKey: ["weeklySchedule"] });
    },
  });

  return {
    ...listQuery,
    createMutation,
    updateMutation,
    deleteMutation,
    reorderMutation,
  };
}
