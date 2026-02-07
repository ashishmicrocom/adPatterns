// API Configuration
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// API Endpoints
export const API_ENDPOINTS = {
  // Auth
  login: `${API_URL}/api/auth/login/json`,
  register: `${API_URL}/api/auth/register`,
  logout: `${API_URL}/api/auth/logout`,
  
  // Campaigns
  campaigns: `${API_URL}/api/campaigns`,
  generateSuggestions: `${API_URL}/api/generate-suggestions`,
  
  // Health Check
  health: `${API_URL}/health`,
};

export default API_URL;
