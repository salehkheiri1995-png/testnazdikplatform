import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useCartStore } from '../store/cartStore';
import './Header.css';

export default function Header() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const items = useCartStore((s) => s.items);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header" dir="rtl">
      <div className="header-container">
        <Link to="/" className="logo">نزدیک</Link>

        <nav className="nav">
          <Link to="/services">خدمات</Link>
          <Link to="/stores">فروشگاه‌ها</Link>
          <Link to="/products">محصولات</Link>
          <Link to="/about">درباره ما</Link>
        </nav>

        <div className="header-actions">
          <Link to="/cart" className="cart-btn">
            🛒
            {items.length > 0 && <span className="cart-badge">{items.length}</span>}
          </Link>

          {isAuthenticated ? (
            <div className="user-menu">
              <Link to="/profile" className="user-btn">
                👤 {user?.full_name?.split(' ')[0]}
              </Link>
              <Link to="/orders" className="nav-link">سفارشات</Link>
              <button onClick={handleLogout} className="logout-btn">خروج</button>
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="btn-outline">ورود</Link>
              <Link to="/register" className="btn-primary">ثبت‌نام</Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
