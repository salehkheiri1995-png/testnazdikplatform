import axios from 'axios';

const axiosClient = axios.create({
  // با proxy در vite.config.ts دیگه نیاز به URL کامل نیست
  baseURL: '',
  headers: { 'Content-Type': 'application/json' },
});

axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default axiosClient;
