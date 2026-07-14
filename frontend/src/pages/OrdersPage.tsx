import { Link } from 'react-router-dom';
import { getUserFromStorage } from '../api/auth';

const OrdersPage = () => {
  const user = getUserFromStorage();

  if (!user) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div style={{ fontSize: '4rem' }}>🔒</div>
        <h2>برای مشاهده سفارش‌ها وارد شوید</h2>
        <Link to="/login" className="btn btn-primary" style={{ marginTop: '1rem', display: 'inline-block' }}>ورود به حساب</Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto', padding: '0 1rem' }}>
      <h1 style={{ marginBottom: '1.5rem' }}>📦 سفارش‌های من</h1>
      <div style={{ textAlign: 'center', padding: '3rem', color: '#666' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📭</div>
        <p>هنوز سفارشی ثبت نکرده‌اید</p>
        <Link to="/services" className="btn btn-primary" style={{ marginTop: '1rem', display: 'inline-block' }}>مشاهده خدمات</Link>
      </div>
    </div>
  );
};

export default OrdersPage;
