import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div dir="rtl" style={{
      minHeight: '70vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '40px'
    }}>
      <div style={{ fontSize: '5rem', marginBottom: '16px' }}>🔍</div>
      <h1 style={{ fontSize: '4rem', color: '#667eea', margin: '0 0 8px' }}>404</h1>
      <h2 style={{ fontSize: '1.4rem', color: '#444', marginBottom: '12px' }}>صفحه پیدا نشد!</h2>
      <p style={{ color: '#888', marginBottom: '28px' }}>صفحه‌ای که دنبالش می‌گردید وجود ندارد یا حذف شده است.</p>
      <Link to="/" style={{
        background: '#667eea', color: 'white', padding: '12px 28px',
        borderRadius: '10px', textDecoration: 'none', fontSize: '1rem'
      }}>بازگشت به خانه</Link>
    </div>
  );
}
