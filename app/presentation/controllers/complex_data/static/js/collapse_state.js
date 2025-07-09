(function(){
  const STORAGE_KEY = 'expandedChains';

  function readState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch {
      return [];
    }
  }
  function writeState(arr) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
    } catch {}
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Восстановим состояние при загрузке
    const expanded = readState();
    expanded.forEach(id => {
      const el = document.getElementById(`children-${id}`);
      if (el) {
        // Через Bootstrap API:
        new bootstrap.Collapse(el, { toggle: false }).show();
      }
    });

    // Слушаем клики по всем .children-toggle
    document.querySelectorAll('.children-toggle').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-element-id');
        const arr = readState();
        const idx = arr.indexOf(id);
        if (idx === -1) {
          // добавляем
          arr.push(id);
        } else {
          // убираем
          arr.splice(idx, 1);
        }
        writeState(arr);
      });
    });
  });
})();
