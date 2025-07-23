document.getElementById('createChainAllModal')
  .addEventListener('show.bs.modal', function(event) {
    const button = event.relatedTarget;
    const modal  = this;

    // Получаем ID текущей цепочки из кнопки-источника
    const dataId = button.getAttribute('data-data-id');

    // Находим форму и её исходный action (с плейсхолдером 0)
    const form     = modal.querySelector('form');
    const template = form.getAttribute('action');

    // Подставляем реальный ID вместо "/0/"
    const newAction = template.replace(/\/0\//, `/${dataId}/`);
    form.action = newAction;
  });