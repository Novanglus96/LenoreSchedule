// useBackendReady.js
import { ref, onMounted } from "vue";
import api from "@/api";

const backendReady = ref(false);

export function useBackendReady() {
  onMounted(async () => {
    while (!backendReady.value) {
      try {
        const res = await api.get("/options/health/");

        if (res.status === 200) {
          backendReady.value = true;
        }
      } catch (err) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log(err);
      }
    }
  });

  return { backendReady };
}
