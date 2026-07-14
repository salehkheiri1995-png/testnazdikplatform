import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <h1>🎯 نزدیک</h1>
        </Link>
        <nav className="nav">
          <Link to="/" className="nav-link">خانه</Link>
          <Link to="/services" className="nav-link">خدمات</Link>
          <Link to="/stores" className="nav-link">فروشگاه‌ها</Link>
        </nav>
        <div className="header-actions">
          <button className="btn btn-primary">ورود / ثبت‌نام</button>
        </div>
      </div>
    </header>
  );
};

export default Header;
