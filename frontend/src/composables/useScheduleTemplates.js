import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import api from "@/api/index.js";
import { useMainStore } from "@/stores/main";

export function useScheduleTemplates(employeeId) {
  const queryClient = useQueryClient();
  const mainStore = useMainStore();

  const listQuery = useQuery({
    queryKey: ["scheduleTemplates", employeeId],
    queryFn: async () => {
      const { data } = await api.get(
        `/schedule_templates/employee/${employeeId.value}`,
      );
      return data;
    },
    enabled: () => !!employeeId.value,
  });

  const createMutation = useMutation({
    mutationFn: (payload) => api.post("/schedule_templates/create", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["scheduleTemplates"] });
      mainStore.showSnackbar("Template created", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to create template",
        "error",
      ),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, ...payload }) =>
      api.put(`/schedule_templates/update/${id}`, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["scheduleTemplates"] });
      mainStore.showSnackbar("Template updated", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to update template",
        "error",
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/schedule_templates/delete/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["scheduleTemplates"] });
      mainStore.showSnackbar("Template deleted", "success");
    },
    onError: (e) =>
      mainStore.showSnackbar(
        e.response?.data?.detail || "Failed to delete template",
        "error",
      ),
  });

  return { ...listQuery, createMutation, updateMutation, deleteMutation };
}
