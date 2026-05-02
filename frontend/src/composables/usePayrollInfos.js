import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function usePayrollInfos() {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const listQuery = useQuery({
    queryKey: ["payrollInfos"],
    queryFn: async () => {
      const { data } = await api.get("/options/payroll_infos/list");
      return data;
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/options/payroll_infos/create", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["payrollInfos"] });
      queryClient.invalidateQueries({ queryKey: ["payrollWeeks"] });
      mainStore.showSnackbar("Payroll info created", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to create payroll info",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) =>
      api.put(`/options/payroll_infos/update/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["payrollInfos"] });
      queryClient.invalidateQueries({ queryKey: ["payrollWeeks"] });
      mainStore.showSnackbar("Payroll info updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update payroll info",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/options/payroll_infos/delete/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["payrollInfos"] });
      queryClient.invalidateQueries({ queryKey: ["payrollWeeks"] });
      mainStore.showSnackbar("Payroll info deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete payroll info",
        "error",
      ),
  });

  return { ...listQuery, createMutation, updateMutation, deleteMutation };
}
