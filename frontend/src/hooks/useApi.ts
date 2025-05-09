import { useState, useCallback } from 'react';
import axios, { AxiosRequestConfig } from 'axios';

// Base API URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

interface ApiResponse<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
}

export function useApi<T>() {
  const [state, setState] = useState<ApiResponse<T>>({
    data: null,
    error: null,
    loading: false,
  });

  const request = useCallback(
    async (endpoint: string, options: AxiosRequestConfig = {}) => {
      try {
        setState({ data: null, error: null, loading: true });
        
        const url = endpoint.startsWith('http') ? endpoint : `${API_URL}${endpoint}`;
        const response = await axios({ ...options, url });
        
        setState({ data: response.data, error: null, loading: false });
        return response.data;
      } catch (error) {
        const errorObject = error instanceof Error ? error : new Error('An unknown error occurred');
        setState({ data: null, error: errorObject, loading: false });
        throw errorObject;
      }
    },
    []
  );

  return { ...state, request };
}

export default useApi;
