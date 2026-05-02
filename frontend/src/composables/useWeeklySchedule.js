import { useQuery } from "@tanstack/vue-query";
import { toValue } from "vue";
import api from "@/api/index.js";

export function useWeeklySchedule(page, payrollYear) {
  return useQuery({
    queryKey: ["weeklySchedule", page, payrollYear],
    queryFn: async () => {
      const { data } = await api.get("/calendar/weekly_schedule", {
        params: { page: toValue(page), payroll_year: toValue(payrollYear) },
      });
      return data;
    },
    staleTime: 1000 * 60 * 5,
  });
}
