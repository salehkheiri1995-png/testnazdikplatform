import { Link } from 'react-router-dom';
import './HomePage.css';

const categories = [
  { icon: '🧹', label: 'نظافت', to: '/services' },
  { icon: '🔧', label: 'تعمیرات', to: '/services' },
  { icon: '📚', label: 'آموزش', to: '/services' },
  { icon: '🚗', label: 'حمل و نقل', to: '/services' },
  { icon: '🏪', label: 'سوپرمارکت', to: '/stores' },
  { icon: '👗', label: 'پوشاک', to: '/stores' },
  { icon: '📱', label: 'الکترونیک', to: '/products' },
  { icon: '🍔', label: 'غذا', to: '/stores' },
];

const HomePage = () => {
  return (
    <div className="home-page" dir="rtl">

      {/* Hero */}
      <section className="hero">
        <div className="hero-content">
          <h1>هر چیزی که نیاز داری، <br /><span>نزدیک</span> پیداش کن!</h1>
          <p>خدمات محلی، کالاهای فیزیکی و فروشگاه‌های اطرافتان اینجاست</p>
          <div className="hero-search">
            <input type="text" placeholder="دنبال چه میگردید؟ (نظافت، پیتزا، ...)" />
            <button>🔍 جستجو</button>
          </div>
          <div className="hero-buttons">
            <Link to="/services" className="btn btn-primary">مشاهده خدمات</Link>
            <Link to="/stores" className="btn btn-outline">فروشگاه‌ها</Link>
          </div>
        </div>
        <div className="hero-image">🏙️</div>
      </section>

      {/* Categories */}
      <section className="categories">
        <div className="section-container">
          <h2>دسته‌بندی‌ها</h2>
          <div className="categories-grid">
            {categories.map((c) => (
              <Link to={c.to} key={c.label} className="category-card">
                <span className="cat-icon">{c.icon}</span>
                <span>{c.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* چرا نزدیک */}
      <section className="features">
        <div className="section-container">
          <h2>چرا نزدیک؟</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📍</div>
              <h3>محلی و سریع</h3>
              <p>دسترسی به انواع خدمات و کالاها در نزدیکی شما</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⭐</div>
              <h3>ارائه‌دهندگان تأییدشده</h3>
              <p>تمام ارائه‌دهندگان توسط تیم نزدیک بررسی و تأیید شده‌اند</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💳</div>
              <h3>پرداخت امن</h3>
              <p>پرداخت آنلاین و درگاه بانکی امن و سریع</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📦</div>
              <h3>پیگیری سفارش</h3>
              <p>وضعیت سفارش را در لحظه مشاهده کنید</p>
            </div>
          </div>
        </div>
      </section>

      {/* دو طرفه */}
      <section className="two-sides">
        <div className="section-container">
          <h2>برای همه</h2>
          <div className="sides-grid">
            <div className="side-card customers">
              <h3>🛍️ مشتریان</h3>
              <ul>
                <li>جستجو و سفارش آسان</li>
                <li>نظرات و امتیازدهی واقعی</li>
                <li>پیگیری لحظه‌به‌لحظه</li>
                <li>ذخیره آدرس و تاریخچه</li>
              </ul>
              <Link to="/register" className="btn btn-primary">ثبت‌نام رایگان</Link>
            </div>
            <div className="side-card providers">
              <h3>🔧 ارائه‌دهندگان و فروشندگان</h3>
              <ul>
                <li>پنل مدیریت حرفه‌ای</li>
                <li>دریافت سفارشات در لحظه</li>
                <li>آمار و گزارش درآمد</li>
                <li>معرفی رایگان به هزاران مشتری</li>
              </ul>
              <Link to="/register" className="btn btn-outline">همکاری با ما</Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <div className="cta-content">
          <h2>امروز شروع کنید!</h2>
          <p>همین حالا ثبت‌نام کنید و از خدمات نزدیک بهره‌مند شوید</p>
          <Link to="/register" className="btn btn-white">ثبت‌نام رایگان</Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
