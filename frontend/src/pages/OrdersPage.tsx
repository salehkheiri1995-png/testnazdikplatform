import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import './OrdersPage.css';

interface Order {
  id: number;
  order_number: string;
  status: string;
  total_amount: number;
  order_type: string;
  created_at: string;
}

const statusMap: Record<string, { label: string; color: string }> = {
  pending:     { label: 'در انتظار', color: '#f59e0b' },
  confirmed:   { label: 'تأیید شده', color: '#3b82f6' },
  in_progress: { label: 'در حال انجام', color: '#8b5cf6' },
  completed:   { label: 'تکمیل شده', color: '#10b981' },
  cancelled:   { label: 'لغو شده', color: '#ef4444' },
  refunded:    { label: 'بازگشت وجه', color: '#6b7280' },
};

export default function OrdersPage() {
  const { isAuthenticated } = useAuthStore();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) { setLoading(false); return; }
    fetch('/api/v1/orders/')
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => setOrders(data.items || data))
      .catch(() => setOrders([]))
      .finally(() => setLoading(false));
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <div className="orders-page" dir="rtl">
        <div className="empty-orders">
          <span>🔒</span>
          <h2>ابتدا وارد شوید</h2>
          <Link to="/login" className="btn-primary">ورود به حساب</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="orders-page" dir="rtl">
      <div className="orders-container">
        <h1>📦 سفارشات من</h1>

        {loading ? (
          <div className="loading">در حال بارگذاری...</div>
        ) : orders.length === 0 ? (
          <div className="empty-orders">
            <span>📦</span>
            <h2>هنوز سفارشی ندارید</h2>
            <p>اولین سفارش خود را ثبت کنید!</p>
            <div style={{ display:'flex', gap:'12px', justifyContent:'center', marginTop:'16px' }}>
              <Link to="/services" className="btn-primary">خدمات</Link>
              <Link to="/stores" className="btn-outline">فروشگاه‌ها</Link>
            </div>
          </div>
        ) : (
          <div className="orders-list">
            {orders.map((order) => {
              const st = statusMap[order.status] || { label: order.status, color: '#888' };
              return (
                <div className="order-card" key={order.id}>
                  <div className="order-number">
                    <strong>#{order.order_number}</strong>
                    <span className="order-type">
                      {order.order_type === 'service' ? '🔧 خدمات' : '📦 کالا'}
                    </span>
                  </div>
                  <div className="order-date">
                    {new Date(order.created_at).toLocaleDateString('fa-IR')}
                  </div>
                  <div className="order-amount">
                    {order.total_amount.toLocaleString('fa-IR')} تومان
                  </div>
                  <span className="order-status" style={{ background: st.color + '22', color: st.color }}>
                    {st.label}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
