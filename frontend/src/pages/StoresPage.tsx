import { useState } from 'react';
import { Link } from 'react-router-dom';
import './StoresPage.css';

const StoresPage = () => {
  const [stores] = useState([
    { id: 1, name: 'سوپرمارکت شبانه‌روزی', category: 'مواد غذایی', rating: 4.7, image: '🛒' },
    { id: 2, name: 'پوشاک مدرن', category: 'پوشاک', rating: 4.5, image: '👔' },
    { id: 3, name: 'میوه فروشی تازه', category: 'میوه و سبزیجات', rating: 4.9, image: '🍎' },
    { id: 4, name: 'فروشگاه لوازم خانگی', category: 'لوازم خانگی', rating: 4.6, image: '🏠' },
    { id: 5, name: 'نانوایی سنتی', category: 'نان و شیرینی', rating: 4.8, image: '🍞' },
    { id: 6, name: 'داروخانه 24 ساعته', category: 'دارو و بهداشت', rating: 4.7, image: '💊' },
  ]);

  return (
    <div className="stores-page">
      <div className="page-header">
        <h1>فروشگاه‌های محلی</h1>
        <p>خرید از فروشگاه‌های محله خود</p>
      </div>

      <div className="filters">
        <input type="text" placeholder="جستجو در فروشگاه‌ها..." className="search-input" />
        <select className="filter-select">
          <option>همه دسته‌بندی‌ها</option>
          <option>مواد غذایی</option>
          <option>پوشاک</option>
          <option>لوازم خانگی</option>
        </select>
      </div>

      <div className="grid grid-2">
        {stores.map((store) => (
          <Link to={`/stores/${store.id}`} key={store.id} className="store-card card">
            <div className="store-image">{store.image}</div>
            <div className="store-info">
              <h3>{store.name}</h3>
              <p className="category">{store.category}</p>
              <div className="rating">⭐ {store.rating}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default StoresPage;
