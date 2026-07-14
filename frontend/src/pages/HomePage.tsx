import { Link } from 'react-router-dom';
import './HomePage.css';

const categories = [
  { icon: '🧹', label: 'نظافت', to: '/services' },
  { icon: '🔧', label: 'تعمیرات', to: '/services' },
  { icon: '📚', label: 'آموزش', to: '/services' },
  { icon: '🚗', label: 'حملونقل', to: '/services' },
  { icon: '🏪', label: 'سوپرمارکت', to: '/stores' },
  { icon: '👗', label: 'پوشاک', to: '/stores' },
  { icon: '📱', label: 'الکترونیک', to: '/products' },
  { icon: '🍔', label: 'غذا', to: '/stores' },
];

const features = [
  { icon: '📍', label: 'محلی و سریع', desc: 'دسترسی به خدمات و کالاها در نزدیکی شما', c1:'#6366f1',c2:'#818cf8' },
  { icon: '⭐', label: 'ارائه‌دهندگان تأییدشده', desc: 'تمام ارائه‌دهندگان توسط تیم نزدیک بررسی شده‌اند', c1:'#f59e0b',c2:'#fbbf24' },
  { icon: '💳', label: 'پرداخت امن', desc: 'پرداخت آنلاین امن با درگاه‌های بانکی معتبر', c1:'#10b981',c2:'#34d399' },
  { icon: '📦', label: 'پیگیری سفارش', desc: 'وضعیت سفارش را در لحظه مشاهده کنید', c1:'#f43f5e',c2:'#fb7185' },
];

export default function HomePage() {
  return (
    <div className="home-page" dir="rtl">

      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-bg" />
        <div className="hero-grid" />
        <div className="hero-content">
          <div className="hero-tag">
            <span />
            پلتفرم شماره یک ایران
          </div>
          <h1>
            هر چیزی که نیاز داری،<br />
            <em>نزدیک</em> پیداش کن!
          </h1>
          <p className="hero-desc">
            خدمات محلی، کالاهای فیزیکی و فروشگاه‌های اطرافت — همه چیز در یک اپلیکیشن
          </p>
          <div className="hero-search">
            <input type="text" placeholder="دنبال چه میگردید؟  نظافت، پیتزا، تعمیرات ..." />
            <button className="search-btn">🔍 جستجو</button>
          </div>
          <div className="hero-buttons">
            <Link to="/services" className="btn-hero-primary">مشاهده خدمات</Link>
            <Link to="/stores" className="btn-hero-secondary">فروشگاه‌ها</Link>
          </div>
          <div className="hero-stats">
            <div className="hero-stat"><span className="stat-num">۱۰۰+</span><span className="stat-lbl">ارائه‌دهنده</span></div>
            <div className="hero-stat"><span className="stat-num">۵۰+</span><span className="stat-lbl">فروشگاه</span></div>
            <div className="hero-stat"><span className="stat-num">۳ شهر</span><span className="stat-lbl">پوشش</span></div>
          </div>
        </div>

        <div className="hero-visual">
          {['🧹','🔧','📚','🏪','🚗','📱','👗','🍔','⭐'].map((e,i) => (
            <div className="hero-visual-item" key={i}>{e}</div>
          ))}
        </div>
      </section>

      {/* ── Categories ── */}
      <section className="section-wrap dark">
        <div className="section-inner">
          <div className="section-head">
            <h2>دسته‌بندی‌ها</h2>
            <p>خدمت یا کالای مورد نظر خود را بیابید</p>
          </div>
          <div className="cats-grid">
            {categories.map((c) => (
              <Link to={c.to} key={c.label} className="cat-card">
                <span className="cat-icon">{c.icon}</span>
                <span>{c.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="section-wrap">
        <div className="section-inner">
          <div className="section-head">
            <h2>چرا نزدیک؟</h2>
            <p>مزیت‌هایی که ما ارائه می‌دهیم</p>
          </div>
          <div className="features-grid">
            {features.map((f) => (
              <div className="feature-box" key={f.label}
                style={{ '--c1': f.c1, '--c2': f.c2 } as React.CSSProperties}>
                <div className="feature-icon-wrap" style={{ background: `linear-gradient(135deg,${f.c1},${f.c2})` }}>
                  {f.icon}
                </div>
                <h3>{f.label}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Two Sides ── */}
      <section className="section-wrap dark">
        <div className="section-inner">
          <div className="section-head">
            <h2>برای همه</h2>
            <p>هم مشتریان و هم ارائه‌دهندگان</p>
          </div>
          <div className="sides-grid">
            <div className="side-box customer">
              <h3>🛍️ مشتریان</h3>
              <ul className="side-list">
                <li>جستجو و سفارش آسان</li>
                <li>نظرات و امتیازدهی واقعی</li>
                <li>پیگیری لحظه‌به‌لحظه سفارش</li>
                <li>ذخیره آدرس و تاریخچه</li>
              </ul>
              <Link to="/register" className="btn-customer">ثبت‌نام رایگان</Link>
            </div>
            <div className="side-box provider">
              <h3>🔧 ارائه‌دهندگان و فروشندگان</h3>
              <ul className="side-list">
                <li>پنل مدیریت حرفه‌ای</li>
                <li>دریافت سفارشات در لحظه</li>
                <li>آمار و گزارش درآمد</li>
                <li>معرفی رایگان به هزاران مشتری</li>
              </ul>
              <Link to="/register" className="btn-provider">همکاری با ما</Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="cta-wrap">
        <h2>امروز شروع کنید!</h2>
        <p>همین حالا ثبت‌نام کنید و از خدمات نزدیک بهره‌مند شوید</p>
        <div className="cta-buttons">
          <Link to="/register" className="btn-cta-main">ثبت‌نام رایگان</Link>
          <Link to="/about" className="btn-cta-sec">بیشتر بدان</Link>
        </div>
      </section>

    </div>
  );
}
