import { useState } from 'react';
import { Link } from 'react-router-dom';
import './ServicesPage.css';

const ServicesPage = () => {
  const [services] = useState([
    { id: 1, title: 'نظافت منزل', provider: 'شرکت نظافتی ABC', price: '500,000', rating: 4.8, image: '🏠' },
    { id: 2, title: 'تعمیر یخچال', provider: 'تعمیرگاه الکترونیک', price: '300,000', rating: 4.5, image: '🔧' },
    { id: 3, title: 'آموزش زبان انگلیسی', provider: 'استاد محمدی', price: '400,000', rating: 4.9, image: '📚' },
    { id: 4, title: 'حمل اثاثیه', provider: 'باربری سریع', price: '800,000', rating: 4.6, image: '🚚' },
    { id: 5, title: 'آرایشگری', provider: 'سالن زیبایی نگار', price: '250,000', rating: 4.7, image: '💇' },
    { id: 6, title: 'تعمیر کولر', provider: 'سرویس تهویه', price: '350,000', rating: 4.4, image: '❄️' },
  ]);

  return (
    <div className="services-page">
      <div className="page-header">
        <h1>خدمات محلی</h1>
        <p>بهترین خدمات را در محله خود پیدا کنید</p>
      </div>

      <div className="filters">
        <input type="text" placeholder="جستجو در خدمات..." className="search-input" />
        <select className="filter-select">
          <option>همه دسته‌بندی‌ها</option>
          <option>نظافت</option>
          <option>تعمیرات</option>
          <option>آموزش</option>
        </select>
      </div>

      <div className="grid grid-3">
        {services.map((service) => (
          <Link to={`/services/${service.id}`} key={service.id} className="service-card card">
            <div className="service-image">{service.image}</div>
            <h3>{service.title}</h3>
            <p className="provider-name">{service.provider}</p>
            <div className="service-footer">
              <div className="rating">⭐ {service.rating}</div>
              <div className="price">{service.price} تومان</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ServicesPage;
