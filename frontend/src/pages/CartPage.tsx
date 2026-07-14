import { Link } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import './CartPage.css';

export default function CartPage() {
  const { items, removeItem, updateQuantity, clearCart, getTotalPrice } = useCartStore();

  if (items.length === 0) {
    return (
      <div className="cart-page" dir="rtl">
        <div className="empty-cart">
          <span>🛒</span>
          <h2>سبد خرید شما خالی است</h2>
          <p>محصولات مورد نظر خود را از فروشگاه‌ها انتخاب کنید</p>
          <Link to="/stores" className="btn-primary">رفتن به فروشگاه‌ها</Link>
        </div>
      </div>
    );
  }

  const total = getTotalPrice();

  return (
    <div className="cart-page" dir="rtl">
      <div className="cart-container">
        <div className="cart-header">
          <h1>🛒 سبد خرید</h1>
          <button className="clear-btn" onClick={clearCart}>خالی کردن سبد</button>
        </div>

        <div className="cart-layout">
          <div className="cart-items">
            {items.map((item) => (
              <div className="cart-item" key={item.id}>
                <div className="item-image">
                  {item.image_url
                    ? <img src={item.image_url} alt={item.name} />
                    : <span>📦</span>
                  }
                </div>
                <div className="item-info">
                  <h3>{item.name}</h3>
                  <p className="item-price">{item.price.toLocaleString('fa-IR')} تومان</p>
                </div>
                <div className="item-qty">
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>−</button>
                  <span>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                </div>
                <div className="item-total">
                  {(item.price * item.quantity).toLocaleString('fa-IR')} تومان
                </div>
                <button className="remove-btn" onClick={() => removeItem(item.id)}>×</button>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <h2>خلاصه سفارش</h2>
            <div className="summary-row">
              <span>جمع کالاها:</span>
              <span>{items.reduce((s, i) => s + i.quantity, 0)} عدد</span>
            </div>
            <div className="summary-row">
              <span>جمع کل:</span>
              <span>{total.toLocaleString('fa-IR')} تومان</span>
            </div>
            <div className="summary-row delivery">
              <span>هزینه ارسال:</span>
              <span>توسط فروشنده تعیین می‌شود</span>
            </div>
            <div className="summary-total">
              <span>جمع قابل پرداخت:</span>
              <strong>{total.toLocaleString('fa-IR')} تومان</strong>
            </div>
            <button className="checkout-btn">درگاه پرداخت</button>
            <Link to="/stores" className="continue-btn">ادامه خرید</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
