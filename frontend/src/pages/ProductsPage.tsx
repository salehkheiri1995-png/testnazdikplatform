import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useProducts } from '../api/products';
import { formatPrice } from '../utils/helpers';

const ProductsPage = () => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');

  const { data, isLoading, error } = useProducts({
    page,
    page_size: 12,
    search: search || undefined,
  });

  if (isLoading) return <div className="loading">در حال بارگذاری...</div>;
  if (error) return <div className="error">خطا در بارگذاری محصولات</div>;

  return (
    <div className="stores-page">
      <div className="page-header">
        <h1>محصولات</h1>
        <p>محصولات فروشگاه‌های محلی</p>
      </div>

      <div className="filters">
        <input
          type="text"
          placeholder="جستجو در محصولات..."
          className="search-input"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="grid grid-3">
        {data?.items.map((product) => (
          <div key={product.id} className="card">
            <h3>{product.name}</h3>
            <p style={{ color: '#666', fontSize: '0.9rem' }}>{product.description}</p>
            <div className="product-price" style={{ marginTop: '0.5rem' }}>
              {product.discount_percent ? (
                <span style={{ textDecoration: 'line-through', color: '#999', marginLeft: '8px' }}>
                  {formatPrice(product.price)}
                </span>
              ) : null}
              <strong style={{ color: '#e63946' }}>{formatPrice(product.final_price || product.price)}</strong>
            </div>
            {product.stock_quantity !== undefined && (
              <p style={{ fontSize: '0.85rem', color: product.stock_quantity > 0 ? 'green' : 'red' }}>
                {product.stock_quantity > 0 ? `موجود: ${product.stock_quantity} عدد` : 'ناموجود'}
              </p>
            )}
          </div>
        ))}
      </div>

      {data && data.total_pages > 1 && (
        <div className="pagination">
          <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn btn-secondary">قبلی</button>
          <span>صفحه {page} از {data.total_pages}</span>
          <button onClick={() => setPage(p => Math.min(data.total_pages, p + 1))} disabled={page === data.total_pages} className="btn btn-secondary">بعدی</button>
        </div>
      )}
    </div>
  );
};

export default ProductsPage;
