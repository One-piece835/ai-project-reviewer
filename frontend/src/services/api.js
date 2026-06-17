import axios from "axios";

const api = axios.create({
  baseURL: "https://ai-project-reviewer.onrender.com",
});

export const reviewProject = async (repoUrl) => {
  const response = await api.post(
    "/api/review/",
    {
      repo_url: repoUrl,
    }
  );

  return response.data;
};



export default api;