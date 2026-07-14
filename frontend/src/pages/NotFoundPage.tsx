import { Link } from 'react-router-dom';

const NotFoundPage = () => (
  <div style={{ textAlign: 'center', padding: '6rem 2rem' }}>
    <div style={{ fontSize: '6rem' }}>🔍</div>
    <h1 style={{ fontSize: '3rem', color: '#e63946' }}>404</h1>
    <h2>صفحه‌ای پیدا نشد</h2>
    <p style={{ color: '#666', marginBottom: '2rem' }}>صفحه‌ای که دنبالش می‌گردید وجود ندارد</p>
    <Link to="/" className="btn btn-primary">بازگشت به خانه</Link>
  </div>
);

export default NotFoundPage;
