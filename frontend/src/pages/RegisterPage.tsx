import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { register } from '../api/auth';

const RegisterPage = () => {
  const [fullName, setFullName] = useState('');
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
      const res = await register({ full_name: fullName, phone, password });
      setUser(res.user, res.access_token);
      navigate('/');
    } catch {
      setError('خطا در ثبت‌نام. شاید این شماره قبلاً ثبت شده باشد.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '4rem auto', padding: '2rem' }}>
      <div className="card">
        <h1 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>ثبت‌نام</h1>
        {error && <div className="error" style={{ marginBottom: '1rem', padding: '0.75rem', borderRadius: 8 }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>نام کامل</label>
            <input type="text" value={fullName} onChange={e => setFullName(e.target.value)}
              placeholder="علی محمدی" className="search-input" style={{ width: '100%' }} required />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>شماره تلفن</label>
            <input type="tel" value={phone} onChange={e => setPhone(e.target.value)}
              placeholder="09120000000" className="search-input" style={{ width: '100%' }} required />
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>رمز عبور</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)}
              placeholder="حداقل ۸ کاراکتر" className="search-input" style={{ width: '100%' }} required minLength={8} />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'در حال ثبت‌نام...' : 'ثبت‌نام'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '1rem' }}>
          حساب دارید؟ <Link to="/login" style={{ color: '#3a86ff' }}>وارد شوید</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
