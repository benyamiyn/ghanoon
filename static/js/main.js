// ===========================================================
// مشاور صوت — main.js
// فعلاً فقط باز/بسته‌شدن دراپ‌داون پروفایل رو مدیریت می‌کنه.
// بعداً توابع لایک/کامنت AJAX هم همین‌جا اضافه می‌شن.
// ===========================================================

document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('profileToggle');
  const dropdown = document.getElementById('profileDropdown');

  if (!toggle || !dropdown) return; // یعنی کاربر لاگین نیست، این بخش اصلاً توی صفحه نیست

  toggle.addEventListener('click', function (e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });

  // کلیک بیرون از دراپ‌داون -> بسته بشه
  document.addEventListener('click', function (e) {
    if (!dropdown.contains(e.target) && e.target !== toggle) {
      dropdown.classList.remove('open');
    }
  });
});

// ===========================================================
// DJANGO: تابع کمکی برای خوندن CSRF Token از کوکی.
// وقتی بعداً لایک/کامنت رو با fetch بدون رفرش صفحه پیاده کردیم،
// این تابع لازم می‌شه.
// ===========================================================
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
