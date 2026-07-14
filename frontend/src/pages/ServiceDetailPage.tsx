import { useParams, Link } from 'react-router-dom';
import { useService } from '../api/services';
import { formatPrice, formatDate } from '../utils/helpers';
import './ServiceDetailPage.css';

const ServiceDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const serviceId = Number(id);
  
  const { data: service, isLoading, error } = useService(serviceId);

  if (isLoading) {
    return <div className="loading">در حال بارگذاری...</div>;
  }

  if (error || !service) {
    return <div className="error">خدمت مورد نظر یافت نشد</div>;
  }

  return (
    <div className="service-detail-page">
      <div className="breadcrumb">
        <Link to="/">خانه</Link> / 
        <Link to="/services">خدمات</Link> / 
        <span>{service.title}</span>
      </div>

      <div className="service-detail">
        <div className="service-header">
          <div className="service-image-large">{service.image_url || '🛠️'}</div>
          <div className="service-info">
            <h1>{service.title}</h1>
            <div className="service-meta">
              <span className="rating">⭐ {service.rating?.toFixed(1) || 'جدید'}</span>
              <span>({service.review_count || 0} نظر)</span>
              <span>👁️ {service.view_count || 0} بازدید</span>
            </div>
            <div className="service-price">
              {service.discount_percent ? (
                <>
                  <span className="original-price">{formatPrice(service.price)}</span>
                  <span className="discount-badge">%{service.discount_percent} تخفیف</span>
                </>
              ) : null}
              <span className="final-price">{formatPrice(service.final_price || service.price)}</span>
            </div>
          </div>
        </div>

        {service.provider && (
          <div className="provider-section card">
            <h2>ارائه‌دهنده خدمت</h2>
            <div className="provider-info">
              <div className="provider-name">{service.provider.business_name}</div>
              <div className="provider-details">
                <span>📞 {service.provider.phone}</span>
                <span>📍 {service.provider.city} {service.provider.neighborhood}</span>
                {service.provider.is_verified && <span>✅ تأیید شده</span>}
              </div>
            </div>
          </div>
        )}

        <div className="service-description card">
          <h2>توضیحات خدمت</h2>
          <p>{service.description || 'توضیحات موجود نیست'}</p>
        </div>

        <div className="service-location card">
          <h2>موقعیت مکانی</h2>
          <p>📍 {service.city} {service.neighborhood ? `- ${service.neighborhood}` : ''}</p>
        </div>

        <div className="action-buttons">
          <button className="btn btn-primary btn-lg">سفارش این خدمت</button>
          <button className="btn btn-secondary btn-lg">تماس با ارائه‌دهنده</button>
        </div>
      </div>

      <div className="created-at">
        ثبت شده در: {formatDate(service.created_at)}
      </div>
    </div>
  );
};

export default ServiceDetailPage;
