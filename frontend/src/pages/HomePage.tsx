import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <h1 className="hero-title">🎯 نزدیک</h1>
        <p className="hero-subtitle">پلتفرم خدمات و کالاهای محلی</p>
        <div className="hero-buttons">
          <Link to="/services" className="btn btn-primary btn-lg">مشاهده خدمات</Link>
          <Link to="/stores" className="btn btn-secondary btn-lg">فروشگاه‌ها</Link>
        </div>
      </section>

      <section className="features">
        <h2>چرا نزدیک؟</h2>
        <div className="grid grid-3">
          <div className="feature-card card">
            <div className="feature-icon">🏠</div>
            <h3>خدمات محلی</h3>
            <p>دسترسی به انواع خدمات محلی مانند نظافت، تعمیرات و آموزش</p>
          </div>
          <div className="feature-card card">
            <div className="feature-icon">🛒</div>
            <h3>خرید محلی</h3>
            <p>خرید کالاهای روزمره از فروشگاه‌های محله خودتان</p>
          </div>
          <div className="feature-card card">
            <div className="feature-icon">⭐</div>
            <h3>نظرات و امتیازها</h3>
            <p>انتخاب بهترین ارائه‌دهندگان با کمک نظرات کاربران</p>
          </div>
          <div className="feature-card card">
            <div className="feature-icon">💳</div>
            <h3>پرداخت آنلاین</h3>
            <p>پرداخت آسان و امن از طریق درگاه‌های بانکی معتبر</p>
          </div>
          <div className="feature-card card">
            <div className="feature-icon">📍</div>
            <h3>جستجوی مکانی</h3>
            <p>پیدا کردن نزدیک‌ترین ارائه‌دهندگان با استفاده از نقشه</p>
          </div>
          <div className="feature-card card">
            <div className="feature-icon">🔔</div>
            <h3>اعلان‌ها</h3>
            <p>مطلع شدن از وضعیت سفارشات و پیشنهادات ویژه</p>
          </div>
        </div>
      </section>

      <section className="cta">
        <div className="cta-content">
          <h2>آماده شروع هستید؟</h2>
          <p>همین حالا ثبت‌نام کنید و از خدمات نزدیک استفاده کنید</p>
          <button className="btn btn-primary btn-lg">ثبت‌نام رایگان</button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
