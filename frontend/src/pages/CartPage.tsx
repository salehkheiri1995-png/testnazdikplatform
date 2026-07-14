import { Link } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { formatPrice } from '../utils/helpers';

const CartPage = () => {
  const { items, removeItem, updateQuantity, clearCart, getTotalPrice } = useCartStore();

  if (items.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div style={{ fontSize: '4rem' }}>🛒</div>
        <h2>سبد خرید خالی است</h2>
        <p style={{ color: '#666', marginBottom: '2rem' }}>محصولات یا خدمات مورد نظرتان را اضافه کنید</p>
        <Link to="/" className="btn btn-primary">بازگشت به خانه</Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto', padding: '0 1rem' }}>
      <h1 style={{ marginBottom: '1.5rem' }}>🛒 سبد خرید</h1>
      <div>
        {items.map(item => (
          <div key={item.id} className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem', padding: '1rem' }}>
            <div style={{ flex: 1 }}>
              <h3 style={{ margin: 0 }}>{item.name}</h3>
              <p style={{ color: '#e63946', fontWeight: 600, margin: '4px 0 0' }}>{formatPrice(item.price)}</p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <button className="btn btn-secondary" style={{ padding: '4px 12px' }}
                onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
              <span style={{ minWidth: 30, textAlign: 'center' }}>{item.quantity}</span>
              <button className="btn btn-secondary" style={{ padding: '4px 12px' }}
                onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
            </div>
            <button className="btn" style={{ background: '#fee2e2', color: '#e63946', padding: '6px 12px', border: 'none', borderRadius: 6, cursor: 'pointer' }}
              onClick={() => removeItem(item.id)}>حذف</button>
          </div>
        ))}
      </div>
      <div className="card" style={{ padding: '1.5rem', marginTop: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '1.1rem' }}>جمع کل:</span>
          <strong style={{ fontSize: '1.3rem', color: '#e63946' }}>{formatPrice(getTotalPrice())}</strong>
        </div>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button className="btn btn-primary" style={{ flex: 1 }}>ثبت سفارش</button>
          <button className="btn btn-secondary" onClick={clearCart}>پاک کردن</button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
