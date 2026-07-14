import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useStores } from '../api/stores';
import './StoresPage.css';

const StoresPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [city, setCity] = useState('');
  
  const { data, isLoading, error } = useStores({
    page,
    page_size: 12,
    search: search || undefined,
    city: city || undefined,
  });

  if (isLoading) {
    return <div className="loading">در حال بارگذاری...</div>;
  }

  if (error) {
    return <div className="error">خطا در بارگذاری فروشگاه‌ها</div>;
  }

  return (
    <div className="stores-page">
      <div className="page-header">
        <h1>فروشگاه‌های محلی</h1>
        <p>بهترین فروشگاه‌ها را در محله خود پیدا کنید</p>
      </div>

      <div className="filters">
        <input 
          type="text" 
          placeholder="جستجو در فروشگاه‌ها..." 
          className="search-input"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select 
          className="filter-select"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        >
          <option value="">همه شهرها</option>
          <option value="تهران">تهران</option>
          <option value="مشهد">مشهد</option>
          <option value="اصفهان">اصفهان</option>
        </select>
      </div>

      <div className="grid grid-3">
        {data?.items.map((store) => (
          <Link to={`/stores/${store.id}`} key={store.id} className="store-card card">
            <h3>{store.name}</h3>
            <p className="store-description">{store.description || 'توضیحات موجود نیست'}</p>
            <div className="store-info">
              <span>📍 {store.city} {store.neighborhood ? `- ${store.neighborhood}` : ''}</span>
              <span>⭐ {store.rating?.toFixed(1) || 'جدید'} ({store.review_count || 0} نظر)</span>
            </div>
            <div className="store-footer">
              <span className={`badge ${store.is_verified ? 'verified' : ''}`}>
                {store.is_verified ? '✅ تأیید شده' : 'در انتظار تأیید'}
              </span>
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

export default StoresPage;
