import { useState } from 'react';
import './DashboardPage.css';

export default function ProviderDashboardPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'services' | 'orders' | 'reviews'>('overview');

  const stats = [
    { label: 'سفارشات فعال', value: '۰', icon: '📋', color: '#667eea' },
    { label: 'تکمیل‌شده', value: '۰', icon: '✅', color: '#10b981' },
    { label: 'درآمد این ماه', value: '۰ تومان', icon: '💰', color: '#f59e0b' },
    { label: 'امتیاز میانگین', value: '—', icon: '⭐', color: '#ef4444' },
  ];

  return (
    <div className="dashboard-page" dir="rtl">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>🔧 پنل ارائه‌دهنده خدمات</h1>
          <button className="btn-primary">+ افزودن خدمت جدید</button>
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
          {(['overview', 'services', 'orders', 'reviews'] as const).map((tab) => (
            <button
              key={tab}
              className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab === 'overview' && '📊 خلاصه'}
              {tab === 'services' && '🛠️ خدمات من'}
              {tab === 'orders' && '📦 سفارشات'}
              {tab === 'reviews' && '⭐ نظرات'}
            </button>
          ))}
        </div>

        <div className="tab-content">
          {activeTab === 'overview' && (
            <div className="empty-state">
              <span>📊</span>
              <h3>خلاصه فعالیت</h3>
              <p>پس از ثبت اولین خدمت، آمار و گزارشات اینجا نمایش داده می‌شوند.</p>
            </div>
          )}
          {activeTab === 'services' && (
            <div className="empty-state">
              <span>🛠️</span>
              <h3>هنوز خدمتی ثبت نکرده‌اید</h3>
              <p>با کلیک روی «افزودن خدمت جدید» اولین خدمت خود را معرفی کنید.</p>
              <button className="btn-primary" style={{marginTop:'16px'}}>+ افزودن خدمت</button>
            </div>
          )}
          {activeTab === 'orders' && (
            <div className="empty-state">
              <span>📦</span>
              <h3>سفارشی وجود ندارد</h3>
              <p>سفارشات دریافتی اینجا نمایش داده می‌شوند.</p>
            </div>
          )}
          {activeTab === 'reviews' && (
            <div className="empty-state">
              <span>⭐</span>
              <h3>هنوز نظری دریافت نکرده‌اید</h3>
              <p>نظرات مشتریان پس از تکمیل اولین سفارش اینجا نمایش داده می‌شوند.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
