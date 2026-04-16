import { useQuery, useQueryClient } from "@tanstack/vue-query";
import api from "@/api";
import { useMainStore } from "@/stores/main";

async function handleApiError(error, message) {
  const mainstore = useMainStore();
  const backendHealthy = await isBackendHealthy();

  if (!backendHealthy) {
    console.warn("Backend is not healthy. Suppressing error.");
    return null;
  }
  if (error.response) {
    console.error("Response error:", error.response.data);
    console.error("Status code:", error.response.status);
    console.error("Headers", error.response.headers);
  } else if (error.request) {
    console.error("No response received:", error.request);
  } else {
    console.error("Error during request setup:", error.message);
  }
  mainstore.showSnackbar(message + " : " + error.response.data.detail, "error");
  throw error;
}

async function getVersionFunction() {
  try {
    const response = await api.get("/options/version/list");
    return response.data;
  } catch (error) {
    return await handleApiError(error, "Version not fetched: ");
  }
}

export function useVersion() {
  const queryClient = useQueryClient();
  const { data: version, isLoading } = useQuery({
    queryKey: ["version"],
    queryFn: () => getVersionFunction(),
    select: response => response,
    client: queryClient,
  });

  const prefetchVersion = async () => {
    await queryClient.prefetchQuery({
      queryKey: ["version"],
      queryFn: () => getVersionFunction(),
    });
  };

  return {
    isLoading,
    version,
    prefetchVersion,
  };
}

async function isBackendHealthy() {
  try {
    const response = await api.get("/options/health/");
    return response?.data?.status === "ok";
  } catch (e) {
    console.log(e);
    return true;
  }
}
