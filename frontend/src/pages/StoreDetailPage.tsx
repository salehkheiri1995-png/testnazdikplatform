import { useParams, Link } from 'react-router-dom';
import { useStore } from '../api/stores';
import { useProducts } from '../api/products';
import { formatPrice, formatDate } from '../utils/helpers';
import './StoreDetailPage.css';

const StoreDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const storeId = Number(id);
  
  const { data: store, isLoading: storeLoading, error: storeError } = useStore(storeId);
  const { data: products, isLoading: productsLoading } = useProducts({ page: 1, page_size: 20 });

  if (storeLoading) {
    return <div className="loading">در حال بارگذاری...</div>;
  }

  if (storeError || !store) {
    return <div className="error">فروشگاه مورد نظر یافت نشد</div>;
  }

  const storeProducts = products?.items.filter(p => p.store_id === storeId) || [];

  return (
    <div className="store-detail-page">
      <div className="breadcrumb">
        <Link to="/">خانه</Link> / 
        <Link to="/stores">فروشگاه‌ها</Link> / 
        <span>{store.name}</span>
      </div>

      <div className="store-detail">
        <div className="store-header">
          <h1>{store.name}</h1>
          <div className="store-meta">
            <span className="rating">⭐ {store.rating?.toFixed(1) || 'جدید'}</span>
            <span>({store.review_count || 0} نظر)</span>
            <span className={`badge ${store.is_verified ? 'verified' : ''}`}>
              {store.is_verified ? '✅ تأیید شده' : 'در انتظار تأیید'}
            </span>
          </div>
        </div>

        <div className="store-info-section card">
          <h2>اطلاعات فروشگاه</h2>
          <p>📞 {store.phone}</p>
          <p>📍 {store.city} {store.neighborhood ? `- ${store.neighborhood}` : ''}</p>
          {store.address && <p>🏠 {store.address}</p>}
        </div>

        <div className="store-description card">
          <h2>توضیحات</h2>
          <p>{store.description || 'توضیحات موجود نیست'}</p>
        </div>

        <div className="products-section">
          <h2>محصولات این فروشگاه</h2>
          {productsLoading ? (
            <div className="loading">در حال بارگذاری محصولات...</div>
          ) : storeProducts.length > 0 ? (
            <div className="grid grid-3">
              {storeProducts.map((product) => (
                <Link to={`/products/${product.id}`} key={product.id} className="product-card card">
                  <h3>{product.name}</h3>
                  <div className="product-price">
                    {product.discount_percent ? (
                      <>
                        <span className="original-price">{formatPrice(product.price)}</span>
                        <span className="discount-badge">%{product.discount_percent}</span>
                      </>
                    ) : null}
                    <span className="final-price">{formatPrice(product.final_price || product.price)}</span>
                  </div>
                  <div className="product-meta">
                    <span>⭐ {product.rating?.toFixed(1) || 'جدید'}</span>
                    {product.stock_quantity !== undefined && (
                      <span>{product.stock_quantity > 0 ? `موجود: ${product.stock_quantity}` : 'ناموجود'}</span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <p>محصولی برای این فروشگاه ثبت نشده است.</p>
          )}
        </div>

        <div className="action-buttons">
          <button className="btn btn-primary btn-lg">تماس با فروشگاه</button>
        </div>
      </div>

      <div className="created-at">
        ثبت شده در: {formatDate(store.created_at)}
      </div>
    </div>
  );
};

export default StoreDetailPage;
