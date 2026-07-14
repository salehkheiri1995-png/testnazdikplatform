import { useParams } from 'react-router-dom';
import './StoreDetailPage.css';

const StoreDetailPage = () => {
  const { id } = useParams();

  const products = [
    { id: 1, name: 'شیر کم‌چرب', price: '28,000', image: '🥛' },
    { id: 2, name: 'نان بربری', price: '5,000', image: '🍞' },
    { id: 3, name: 'پنیر لیقوان', price: '45,000', image: '🧀' },
    { id: 4, name: 'ماست کم‌چرب', price: '18,000', image: '🥣' },
  ];

  return (
    <div className="detail-page">
      <div className="detail-header">
        <div className="detail-icon">🛒</div>
        <div>
          <h1>سوپرمارکت شبانه‌روزی</h1>
          <p className="category">مواد غذایی</p>
          <div className="rating-detail">⭐ 4.7 (89 نظر)</div>
        </div>
      </div>

      <section className="card">
        <h2>درباره فروشگاه</h2>
        <p>سوپرمارکت شبانه‌روزی با بیش از 10 سال سابقه، ارائه‌دهنده انواع مواد غذایی تازه و با کیفیت است. ما 24 ساعته در خدمت شما هستیم.</p>
      </section>

      <section className="card">
        <h2>محصولات</h2>
        <div className="products-grid">
          {products.map((product) => (
            <div key={product.id} className="product-card">
              <div className="product-image">{product.image}</div>
              <h4>{product.name}</h4>
              <div className="product-price">{product.price} تومان</div>
              <button className="btn btn-primary btn-sm">افزودن به سبد</button>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h3>اطلاعات تماس</h3>
        <p>📞 021-87654321</p>
        <p>📍 تهران، خیابان ولیعصر</p>
        <p>🕐 24 ساعته</p>
      </section>
    </div>
  );
};

export default StoreDetailPage;
