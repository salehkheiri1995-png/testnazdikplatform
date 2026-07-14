import './AboutPage.css';

export default function AboutPage() {
  return (
    <div className="about-page" dir="rtl">
      {/* Hero */}
      <section className="about-hero">
        <div className="container">
          <h1>درباره نزدیک</h1>
          <p className="hero-subtitle">
            پلتفرم یکپارچه مارکت‌پلیس دوطرفه خدمات و کالاهای محلی برای ایران
          </p>
        </div>
      </section>

      {/* معرفی */}
      <section className="about-intro container">
        <div className="intro-text">
          <h2>ما چه هستیم؟</h2>
          <p>
            «نزدیک» یک پلتفرم یکپارچه است که هم خدمات محلی (نظافت، تعمیرات، آموزش و ...)
            و هم کالاهای فیزیکی (سوپرمارکت، پوشاک، الکترونیک و ...) را در یک اپلیکیشن واحد
            ارائه می‌دهد. هدف ما پیوند دادن مشتریان محلی با بهترین ارائه‌دهندگان و فروشندگان
            در نزدیکی آن‌هاست.
          </p>
        </div>
      </section>

      {/* ویژگی‌ها */}
      <section className="about-features">
        <div className="container">
          <h2>ویژگی‌های پلتفرم</h2>
          <div className="features-grid">

            <div className="feature-group">
              <div className="feature-icon">🛍️</div>
              <h3>برای مشتریان</h3>
              <ul>
                <li>✅ جستجو و کشف خدمات و محصولات محلی</li>
                <li>✅ سفارش آنلاین خدمات و کالاها</li>
                <li>✅ نظرات و امتیازدهی به ارائه‌دهندگان</li>
                <li>✅ پرداخت آنلاین و درگاه امن</li>
                <li>✅ پیگیری وضعیت سفارشات در لحظه</li>
                <li>✅ ذخیره آدرس‌های پرکاربرد</li>
              </ul>
            </div>

            <div className="feature-group">
              <div className="feature-icon">🔧</div>
              <h3>برای ارائه‌دهندگان خدمات</h3>
              <ul>
                <li>✅ ثبت و مدیریت خدمات با قیمت‌گذاری انعطاف‌پذیر</li>
                <li>✅ پنل مدیریت سفارشات و تقویم کاری</li>
                <li>✅ آمار و گزارش‌دهی درآمد</li>
                <li>✅ مدیریت نظرات و پاسخ به مشتریان</li>
                <li>✅ پروفایل حرفه‌ای با گالری تصاویر</li>
                <li>✅ تعریف محدوده جغرافیایی فعالیت</li>
              </ul>
            </div>

            <div className="feature-group">
              <div className="feature-icon">🏪</div>
              <h3>برای فروشندگان</h3>
              <ul>
                <li>✅ مدیریت فروشگاه و محصولات</li>
                <li>✅ مدیریت موجودی و قیمت‌گذاری</li>
                <li>✅ سیستم سفارش و پیگیری تحویل</li>
                <li>✅ گزارشات فروش و درآمد</li>
                <li>✅ تنظیم ساعات کاری و محدوده ارسال</li>
                <li>✅ مدیریت تخفیف‌ها و پیشنهادات ویژه</li>
              </ul>
            </div>

          </div>
        </div>
      </section>

      {/* آمار */}
      <section className="about-stats">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-number">۳</span>
              <span className="stat-label">شهر فعال</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">دو طرفه</span>
              <span className="stat-label">مارکت‌پلیس</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">۲۴/۷</span>
              <span className="stat-label">پشتیبانی</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">امن</span>
              <span className="stat-label">پرداخت آنلاین</span>
            </div>
          </div>
        </div>
      </section>

      {/* تماس */}
      <section className="about-contact container">
        <h2>تماس با ما</h2>
        <p>برای همکاری، پیشنهاد یا گزارش مشکل با ما در تماس باشید.</p>
        <div className="contact-info">
          <span>📧 info@nazdik.ir</span>
          <span>📞 ۰۲۱-۱۲۳۴۵۶۷۸</span>
          <span>📍 تهران، ایران</span>
        </div>
      </section>
    </div>
  );
}
