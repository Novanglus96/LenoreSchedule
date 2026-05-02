import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function useEmployees() {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const listQuery = useQuery({
    queryKey: ["employees"],
    queryFn: async () => {
      const { data } = await api.get("/employees/list");
      return data;
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/employees/create", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      mainStore.showSnackbar("Employee created", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to create employee",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) =>
      api.put(`/employees/update/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      mainStore.showSnackbar("Employee updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update employee",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/employees/delete/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      mainStore.showSnackbar("Employee deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete employee",
        "error",
      ),
  });

  return { ...listQuery, createMutation, updateMutation, deleteMutation };
}
