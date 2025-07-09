(function(){
  const PARAM = 'scroll';

  console.log('[scroll] initializing scroll persistence script');

  // Перехватываем сабмит форм
  document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.tagName !== 'FORM') return;
    const y = Math.floor(window.scrollY);
    console.log('[scroll] form submit detected, scrollY =', y, 'original action =', form.action);
    try {
      const u = new URL(form.action, window.location.origin);
      u.searchParams.set(PARAM, y);
      console.log('[scroll] rewriting action to', u.toString());
      form.action = u.toString();
    } catch (err) {
      console.error('[scroll] error rewriting form action:', err);
    }
  }, true);

  // Вспомогалка: возвращает Promise, который резолвится, когда один collapse показан
  function waitForShown(el) {
    return new Promise(resolve => {
      el.addEventListener('shown.bs.collapse', () => resolve(), { once: true });
    });
  }

  function restore() {
    console.log('[scroll] restore() called, search =', window.location.search);
    const params = new URLSearchParams(window.location.search);
    const v = params.get(PARAM);
    console.log('[scroll] scroll param =', v);
    if (v !== null) {
      const y = parseInt(v, 10);
      console.log('[scroll] will scroll to', y, 'after collapse');

      // собираем все контейнеры, которые должны быть показаны
      const toShow = Array.from(document.querySelectorAll('.children-toggle'))
        .map(btn => btn.getAttribute('data-element-id'))
        .filter(id => id && localStorage.getItem('expandedChains'))
        .filter(id => JSON.parse(localStorage.getItem('expandedChains') || '[]').includes(id))
        .map(id => document.getElementById(`children-${id}`))
        .filter(el => el);

      if (toShow.length) {
        // ждём пока все развёрнутся
        Promise.all(toShow.map(el => waitForShown(el)))
          .then(() => {
            console.log('[scroll] all collapse shown, now scrolling');
            window.scrollTo(0, y);
            // чистим URL
            const clean = window.location.pathname + window.location.hash;
            history.replaceState(null, '', clean);
          });
      } else {
        // если ничего не разворачивается — просто скроллим
        window.scrollTo(0, y);
        const clean = window.location.pathname + window.location.hash;
        history.replaceState(null, '', clean);
      }
    }
  }

  // при полной загрузке страницы и при возврате из bfcache
  window.addEventListener('load',  restore);
  window.addEventListener('pageshow', restore);

})();
