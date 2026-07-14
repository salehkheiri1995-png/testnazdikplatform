/**
 * فرمت‌کننده قیمت به تومان با جداکننده هزار
 */
export const formatPrice = (price: number): string => {
  if (price === undefined || price === null) return '—';
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان';
};

/**
 * فرمت‌کننده تاریخ ISO به شمسی
 */
export const formatDate = (dateStr: string): string => {
  if (!dateStr) return '—';
  try {
    return new Date(dateStr).toLocaleDateString('fa-IR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch {
    return dateStr;
  }
};
