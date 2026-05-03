import { useQuery } from "@tanstack/vue-query";
import api from "@/api/index.js";

export function usePayrollWeeks(year) {
  return useQuery({
    queryKey: ["payrollWeeks", year],
    queryFn: async () => {
      const { data } = await api.get(`/options/payroll_infos/${year}/weeks`);
      return data;
    },
    staleTime: 1000 * 60 * 10,
    retry: (failureCount, error) => error?.response?.status !== 404,
  });
}
