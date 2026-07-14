import { useQuery } from '@tanstack/react-query';
import axiosClient from './axiosClient';

export interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  final_price?: number;
  discount_percent?: number;
  stock_quantity?: number;
  rating?: number;
  review_count?: number;
  store_id: number;
  image_url?: string;
  created_at: string;
}

export interface ProductListResponse {
  items: Product[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProductFilters {
  page?: number;
  page_size?: number;
  search?: string;
  store_id?: number;
  category_id?: number;
}

export const useProducts = (filters: ProductFilters = {}) => {
  return useQuery<ProductListResponse>({
    queryKey: ['products', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.page) params.set('page', String(filters.page));
      if (filters.page_size) params.set('page_size', String(filters.page_size));
      if (filters.search) params.set('search', filters.search);
      if (filters.store_id) params.set('store_id', String(filters.store_id));
      if (filters.category_id) params.set('category_id', String(filters.category_id));
      const res = await axiosClient.get<ProductListResponse>(`/api/v1/products/?${params}`);
      return res.data;
    },
  });
};

export const useProduct = (id: number) => {
  return useQuery<Product>({
    queryKey: ['product', id],
    queryFn: async () => {
      const res = await axiosClient.get<Product>(`/api/v1/products/${id}/`);
      return res.data;
    },
    enabled: !!id,
  });
};
