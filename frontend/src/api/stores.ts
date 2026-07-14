import { useQuery } from '@tanstack/react-query';
import axiosClient from './axiosClient';

export interface Store {
  id: number;
  name: string;
  description?: string;
  phone?: string;
  city: string;
  neighborhood?: string;
  address?: string;
  rating?: number;
  review_count?: number;
  is_verified: boolean;
  created_at: string;
}

export interface StoreListResponse {
  items: Store[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface StoreFilters {
  page?: number;
  page_size?: number;
  search?: string;
  city?: string;
}

export const useStores = (filters: StoreFilters = {}) => {
  return useQuery<StoreListResponse>({
    queryKey: ['stores', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set('page', String(filters.page));
      if (filters.page_size) params.set('page_size', String(filters.page_size));
      if (filters.search) params.set('search', filters.search);
      if (filters.city) params.set('city', filters.city);
      const res = await axiosClient.get<StoreListResponse>(`/api/v1/stores/?${params}`);
      return res.data;
    },
  });
};

export const useStore = (id: number) => {
  return useQuery<Store>({
    queryKey: ['store', id],
    queryFn: async () => {
      const res = await axiosClient.get<Store>(`/api/v1/stores/${id}/`);
      return res.data;
    },
    enabled: !!id,
  });
};
