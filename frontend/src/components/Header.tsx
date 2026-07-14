import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useCartStore } from '../store/cartStore';
import { getUserFromStorage } from '../api/auth';
import './Header.css';

const Header = () => {
  const navigate = useNavigate();
  const user = getUserFromStorage();
  const cartItemCount = useCartStore((state) => state.getItemCount());
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <div className="container header-content">
        <Link to="/" className="logo">
          🎯 نزدیک
        </Link>

        <nav className="nav">
          <Link to="/services" className="nav-link">خدمات</Link>
          <Link to="/stores" className="nav-link">فروشگاه‌ها</Link>
          <Link to="/products" className="nav-link">محصولات</Link>
        </nav>

        <div className="header-actions">
          {user ? (
            <>
              <Link to="/cart" className="cart-icon">
                🛒
                {cartItemCount > 0 && (
                  <span className="cart-badge">{cartItemCount}</span>
                )}
              </Link>
              <Link to="/orders" className="nav-link">سفارش‌های من</Link>
              <span className="user-name">👤 {user.full_name}</span>
              <button onClick={handleLogout} className="btn btn-secondary">خروج</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary">ورود</Link>
              <Link to="/register" className="btn btn-primary">ثبت‌نام</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
