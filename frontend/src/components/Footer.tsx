import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>🎯 نزدیک</h3>
          <p>پلتفرم خدمات و کالاهای محلی</p>
        </div>
        <div className="footer-section">
          <h4>لینک‌های سریع</h4>
          <ul>
            <li><a href="/about">درباره ما</a></li>
            <li><a href="/contact">تماس با ما</a></li>
            <li><a href="/terms">شرایط استفاده</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>تماس</h4>
          <p>support@nazdik.ir</p>
          <p>021-12345678</p>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2026 نزدیک. تمامی حقوق محفوظ است.</p>
      </div>
    </footer>
  );
};

export default Footer;
