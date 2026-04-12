import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateIdeas = async (profile) => {
  const response = await api.post('/idea/generate', profile);
  return response.data;
};

export const generateFullPlan = async (profile) => {
  const response = await api.post('/idea/full-plan', profile);
  return response.data;
};

export const expandIdea = async (profile, selectedIdea) => {
  const response = await api.post('/idea/expand', {
    profile,
    selected_idea: selectedIdea
  });
  return response.data;
};

export const getIdeaDetails = async (id, profile) => {
  const response = await api.post(`/idea/${id}/details`, profile);
  return response.data;
};

export default api;
