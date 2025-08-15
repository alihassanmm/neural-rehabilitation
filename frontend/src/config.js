// API Configuration for Replit Deployment
const config = {
  // For Replit deployment, the backend runs on the same domain
  // Users should update this to match their Repl URL
  API_BASE_URL: window.location.origin,
  
  // Development fallback
  isDevelopment: import.meta.env.DEV,
  
  // Get the appropriate API base URL
  getApiUrl: () => {
    // In Replit, both frontend and backend run on the same domain
    // The backend serves the frontend static files
    return window.location.origin;
  }
};

export default config;

