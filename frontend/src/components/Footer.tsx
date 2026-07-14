import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer" dir="rtl">
      <div className="footer-container">
        <div className="footer-brand">
          <h2>نزدیک</h2>
          <p>پلتفرم یکپارچه خدمات و کالاهای محلی برای ایران</p>
          <div className="socials">
            <a href="#">📸</a>
            <a href="#">💬</a>
            <a href="#">📱</a>
          </div>
        </div>

        <div className="footer-links">
          <h3>دسترسی سریع</h3>
          <ul>
            <li><Link to="/services">خدمات</Link></li>
            <li><Link to="/stores">فروشگاه‌ها</Link></li>
            <li><Link to="/products">محصولات</Link></li>
            <li><Link to="/about">درباره ما</Link></li>
          </ul>
        </div>

        <div className="footer-links">
          <h3>حساب کاربری</h3>
          <ul>
            <li><Link to="/login">ورود به حساب</Link></li>
            <li><Link to="/register">ثبت‌نام</Link></li>
            <li><Link to="/orders">سفارشات من</Link></li>
            <li><Link to="/provider/dashboard">پنل ارائه‌دهنده</Link></li>
          </ul>
        </div>

        <div className="footer-links">
          <h3>تماس با ما</h3>
          <ul>
            <li>📧 info@nazdik.ir</li>
            <li>📞 ۰۲۱-۱۲۳۴۵۶۷۸</li>
            <li>📍 تهران، ایران</li>
            <li>⏰ ۲۴/۷ پاسخگویی</li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <span>© ۱۴۰۳ نزدیک — تمامی حقوق محفوظ است</span>
      </div>
    </footer>
  );
}
