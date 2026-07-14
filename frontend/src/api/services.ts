import { useQuery } from '@tanstack/react-query';
import axiosClient from './axiosClient';

export interface ServiceProvider {
  id: number;
  business_name: string;
  phone: string;
  city: string;
  neighborhood?: string;
  is_verified: boolean;
}

export interface Service {
  id: number;
  title: string;
  description?: string;
  price: number;
  final_price?: number;
  discount_percent?: number;
  rating?: number;
  review_count?: number;
  view_count?: number;
  city: string;
  neighborhood?: string;
  image_url?: string;
  provider?: ServiceProvider;
  created_at: string;
}

export interface ServiceListResponse {
  items: Service[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ServiceFilters {
  page?: number;
  page_size?: number;
  search?: string;
  category_id?: number;
}

export const useServices = (filters: ServiceFilters = {}) => {
  return useQuery<ServiceListResponse>({
    queryKey: ['services', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set('page', String(filters.page));
      if (filters.page_size) params.set('page_size', String(filters.page_size));
      if (filters.search) params.set('search', filters.search);
      if (filters.category_id) params.set('category_id', String(filters.category_id));
      const res = await axiosClient.get<ServiceListResponse>(`/api/v1/services/?${params}`);
      return res.data;
    },
  });
};

export const useService = (id: number) => {
  return useQuery<Service>({
    queryKey: ['service', id],
    queryFn: async () => {
      const res = await axiosClient.get<Service>(`/api/v1/services/${id}/`);
      return res.data;
    },
    enabled: !!id,
  });
};
