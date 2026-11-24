import { useQuery } from "@tanstack/vue-query";
import api from "@/api/index.js";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const { data } = await api.get("/dashboard/summary");
      return data;
    },
  });
}
