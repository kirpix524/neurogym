document.getElementById('createAttributeAllModal')
  .addEventListener('show.bs.modal', function(event) {
    console.log('[attr-modal] show.bs.modal triggered, relatedTarget=', event.relatedTarget);
    const button = event.relatedTarget;
    const modal = this;

    // ID текущей цепочки из кнопки-источника
    const dataId = button.getAttribute('data-data-id');
    console.log('[attr-modal] data-data-id =', dataId);

    // Шаблон URL с placeholder-ом
    const template = modal.getAttribute('data-create-url-template');

    // Подставляем реальный ID вместо 0
    const action = template.replace(/\/0\//, `/${dataId}/`);

    // Устанавливаем action формы
    const form = modal.querySelector('#createAttributeAllForm');
    form.action = action;

    // ← сюда добавляем лог перед отправкой
    form.addEventListener('submit', function(e) {
      console.log('[attr-modal] submitting form to:', this.action);
    });
  });