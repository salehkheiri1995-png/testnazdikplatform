import { useState } from 'react';
import './DashboardPage.css';

export default function SellerDashboardPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'products' | 'orders' | 'reports'>('overview');

  const stats = [
    { label: 'محصولات فعال', value: '۰', icon: '📦', color: '#667eea' },
    { label: 'سفارشات امروز', value: '۰', icon: '🛒', color: '#10b981' },
    { label: 'فروش این ماه', value: '۰ تومان', icon: '💰', color: '#f59e0b' },
    { label: 'موجودی کم', value: '۰', icon: '⚠️', color: '#ef4444' },
  ];

  return (
    <div className="dashboard-page" dir="rtl">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>🏪 پنل فروشنده</h1>
          <button className="btn-primary">+ افزودن محصول جدید</button>
        </div>

        {/* Stats */}
        <div className="stats-grid">
          {stats.map((s) => (
            <div className="stat-card" key={s.label} style={{ borderTop: `4px solid ${s.color}` }}>
              <span className="stat-icon">{s.icon}</span>
              <span className="stat-value">{s.value}</span>
              <span className="stat-label">{s.label}</span>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="tabs">
          {(['overview', 'products', 'orders', 'reports'] as const).map((tab) => (
            <button
              key={tab}
              className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab === 'overview' && '📊 خلاصه'}
              {tab === 'products' && '📦 محصولات'}
              {tab === 'orders' && '🛒 سفارشات'}
              {tab === 'reports' && '📈 گزارشات فروش'}
            </button>
          ))}
        </div>

        <div className="tab-content">
          {activeTab === 'overview' && (
            <div className="empty-state">
              <span>📊</span>
              <h3>خلاصه فروشگاه</h3>
              <p>پس از ثبت اولین محصول، آمار و گزارشات فروش اینجا نمایش داده می‌شوند.</p>
            </div>
          )}
          {activeTab === 'products' && (
            <div className="empty-state">
              <span>📦</span>
              <h3>هنوز محصولی اضافه نکرده‌اید</h3>
              <p>با کلیک روی «افزودن محصول جدید» اولین کالای خود را ثبت کنید.</p>
              <button className="btn-primary" style={{marginTop:'16px'}}>+ افزودن محصول</button>
            </div>
          )}
          {activeTab === 'orders' && (
            <div className="empty-state">
              <span>🛒</span>
              <h3>سفارشی وجود ندارد</h3>
              <p>سفارشات دریافتی فروشگاه شما اینجا نمایش داده می‌شوند.</p>
            </div>
          )}
          {activeTab === 'reports' && (
            <div className="empty-state">
              <span>📈</span>
              <h3>گزارشات فروش</h3>
              <p>آمار فروش، درآمد و عملکرد محصولات پس از اولین فروش اینجا نمایش داده می‌شوند.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
