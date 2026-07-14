import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useServices } from '../api/services';
import { formatPrice } from '../utils/helpers';
import './ServicesPage.css';

const ServicesPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [categoryId, setCategoryId] = useState<number | undefined>(undefined);
  
  const { data, isLoading, error } = useServices({
    page,
    page_size: 12,
    search: search || undefined,
    category_id: categoryId,
  });

  if (isLoading) {
    return <div className="loading">در حال بارگذاری...</div>;
  }

  if (error) {
    return <div className="error">خطا در بارگذاری خدمات</div>;
  }

  return (
    <div className="services-page">
      <div className="page-header">
        <h1>خدمات محلی</h1>
        <p>بهترین خدمات را در محله خود پیدا کنید</p>
      </div>

      <div className="filters">
        <input 
          type="text" 
          placeholder="جستجو در خدمات..." 
          className="search-input"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select 
          className="filter-select"
          value={categoryId || ''}
          onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : undefined)}
        >
          <option value="">همه دسته‌بندی‌ها</option>
          <option value="1">نظافت</option>
          <option value="2">تعمیرات</option>
          <option value="3">آموزش</option>
        </select>
      </div>

      <div className="grid grid-3">
        {data?.items.map((service) => (
          <Link to={`/services/${service.id}`} key={service.id} className="service-card card">
            <div className="service-image">{service.image_url || '🛠️'}</div>
            <h3>{service.title}</h3>
            <p className="provider-name">{service.provider?.business_name || 'ارائه‌دهنده'}</p>
            <div className="service-footer">
              <div className="rating">⭐ {service.rating?.toFixed(1) || 'جدید'}</div>
              <div className="price">{formatPrice(service.final_price || service.price)}</div>
            </div>
          </Link>
        ))}
      </div>

      {data && data.total_pages > 1 && (
        <div className="pagination">
          <button 
            onClick={() => setPage(p => Math.max(1, p - 1))} 
            disabled={page === 1}
            className="btn btn-secondary"
          >
            قبلی
          </button>
          <span>صفحه {page} از {data.total_pages}</span>
          <button 
            onClick={() => setPage(p => Math.min(data.total_pages, p + 1))} 
            disabled={page === data.total_pages}
            className="btn btn-secondary"
          >
            بعدی
          </button>
        </div>
      )}
    </div>
  );
};

export default ServicesPage;
