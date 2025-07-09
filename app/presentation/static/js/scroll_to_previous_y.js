(function() {
  // Вешаемся на отправку любых форм
  document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.tagName !== 'FORM') return;

    const y = Math.floor(window.scrollY);

    try {
      const actionUrl = new URL(form.action, window.location.origin);
      actionUrl.searchParams.set('scroll', y);
      form.action = actionUrl.toString();
    } catch (err) {
      console.error('  [scroll script] URL parse error:', err);
    }

    // остановка в точке для ручного дебага
    // debugger;
  }, true);

  // При загрузке страницы
  window.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    const scroll = params.get('scroll');
    if (scroll !== null) {
      const target = parseInt(scroll, 10);
      window.scrollTo(0, target);
    }

    // очищаем URL и логируем
    const cleanUrl = window.location.pathname + window.location.hash;
    history.replaceState(null, '', cleanUrl);
  });
})();
