import axios from 'axios'

// Lấy URL backend từ biến môi trường (khai báo trong .env, xem .env.example)
// Khi deploy lên cloud (Render/Netlify), nhớ set VITE_API_BASE_URL trỏ đúng domain backend
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL,
  timeout: 15000, // 15s, tránh treo UI vô thời hạn khi Gemini API trả lời chậm
  headers: {
    'Content-Type': 'application/json',
  },
})

// Tự động gắn JWT token (nếu có) cho các request cần đăng nhập Admin
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
