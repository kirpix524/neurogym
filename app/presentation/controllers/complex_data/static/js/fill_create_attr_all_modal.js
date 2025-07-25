document.getElementById('createAttributeAllModal')
  .addEventListener('show.bs.modal', function(event) {
    const button = event.relatedTarget;
    const modal = this;

    // ID текущей цепочки из кнопки-источника
    const dataId = button.getAttribute('data-data-id');

    // Шаблон URL с placeholder-ом
    const template = modal.getAttribute('data-create-url-template');

    // Подставляем реальный ID вместо 0
    const action = template.replace(/\/0\//, `/${dataId}/`);

    // Устанавливаем action формы
    const form = modal.querySelector('#createAttributeAllForm');
    form.action = action;
  });