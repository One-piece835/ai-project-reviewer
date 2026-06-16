import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const reviewProject = async (repoUrl) => {
  const response = await api.post(
    "/api/review/",
    {
      repo_url: repoUrl,
    }
  );

  console.log("API Response:", response.data); // Log the entire response data for debugging

  return response.data;
};



export default api;