import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { login } from '../api/auth';

const LoginPage = () => {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setUser } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login({ phone, password });
      setUser(res.user, res.access_token);
      navigate('/');
    } catch {
      setError('شماره تلفن یا رمز عبور اشتباه است');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '4rem auto', padding: '2rem' }}>
      <div className="card">
        <h1 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>ورود به حساب</h1>
        {error && <div className="error" style={{ marginBottom: '1rem', padding: '0.75rem', borderRadius: 8 }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>شماره تلفن</label>
            <input
              type="tel"
              value={phone}
              onChange={e => setPhone(e.target.value)}
              placeholder="09120000000"
              className="search-input"
              style={{ width: '100%' }}
              required
            />
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>رمز عبور</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="رمز عبور"
              className="search-input"
              style={{ width: '100%' }}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'در حال ورود...' : 'ورود'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          حساب ندارید؟ <Link to="/register" style={{ color: '#3a86ff' }}>ثبت‌نام کنید</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
