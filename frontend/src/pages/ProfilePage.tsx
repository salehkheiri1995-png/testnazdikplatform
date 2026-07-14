import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import type { RootState } from '../store';
import './ProfilePage.css';

export default function ProfilePage() {
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);

  if (!isAuthenticated || !user) {
    return (
      <div className="profile-page" dir="rtl">
        <div className="not-auth">
          <span>🔒</span>
          <h2>ابتدا وارد شوید</h2>
          <Link to="/login" className="btn-primary">ورود به حساب</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page" dir="rtl">
      <div className="profile-container">
        <h1>پروفایل کاربری</h1>

        <div className="profile-card">
          <div className="avatar">
            {user.full_name?.charAt(0) || '👤'}
          </div>
          <div className="profile-info">
            <h2>{user.full_name}</h2>
            <p className="phone">📱 {user.phone}</p>
            {user.is_admin && <span className="badge admin">ادمین</span>}
          </div>
        </div>

        <div className="profile-menu">
          <Link to="/orders" className="menu-item">
            <span className="menu-icon">📦</span>
            <div>
              <h3>سفارشات من</h3>
              <p>مشاهده و پیگیری سفارشات</p>
            </div>
            <span className="arrow">←</span>
          </Link>

          <Link to="/provider/dashboard" className="menu-item">
            <span className="menu-icon">🔧</span>
            <div>
              <h3>پنل ارائه‌دهنده خدمات</h3>
              <p>مدیریت خدمات، سفارشات و درآمد</p>
            </div>
            <span className="arrow">←</span>
          </Link>

          <Link to="/seller/dashboard" className="menu-item">
            <span className="menu-icon">🏪</span>
            <div>
              <h3>پنل فروشنده</h3>
              <p>مدیریت فروشگاه، محصولات و سفارشات</p>
            </div>
            <span className="arrow">←</span>
          </Link>

          <Link to="/about" className="menu-item">
            <span className="menu-icon">ℹ️</span>
            <div>
              <h3>درباره نزدیک</h3>
              <p>آشنایی با پلتفرم و ویژگی‌ها</p>
            </div>
            <span className="arrow">←</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
