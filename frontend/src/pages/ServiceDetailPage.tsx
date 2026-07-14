import { useParams } from 'react-router-dom';
import './ServiceDetailPage.css';

const ServiceDetailPage = () => {
  const { id } = useParams();

  return (
    <div className="detail-page">
      <div className="detail-header">
        <div className="detail-icon">🏠</div>
        <div>
          <h1>نظافت منزل</h1>
          <p className="provider">شرکت نظافتی ABC</p>
          <div className="rating-detail">⭐ 4.8 (127 نظر)</div>
        </div>
      </div>

      <div className="detail-grid">
        <div className="detail-main">
          <section className="card">
            <h2>توضیحات خدمت</h2>
            <p>ارائه خدمات نظافت حرفه‌ای منزل شامل تمیز کردن کف، شیشه‌ها، آشپزخانه و سرویس‌های بهداشتی. تیم ما با استفاده از بهترین تجهیزات و مواد شوینده، منزل شما را به‌طور کامل تمیز و ضدعفونی می‌کند.</p>
          </section>

          <section className="card">
            <h2>ویژگی‌ها</h2>
            <ul className="features-list">
              <li>✅ تیم حرفه‌ای و با تجربه</li>
              <li>✅ استفاده از مواد شوینده استاندارد</li>
              <li>✅ بیمه مسئولیت</li>
              <li>✅ گارانتی رضایت</li>
            </ul>
          </section>
        </div>

        <div className="detail-sidebar">
          <div className="card price-card">
            <div className="price-value">500,000 تومان</div>
            <p className="price-note">قیمت تقریبی - بسته به وسعت منزل متغیر است</p>
            <button className="btn btn-primary btn-block">درخواست خدمت</button>
          </div>

          <div className="card">
            <h3>اطلاعات تماس</h3>
            <p>📞 021-12345678</p>
            <p>📍 تهران، منطقه 3</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceDetailPage;
