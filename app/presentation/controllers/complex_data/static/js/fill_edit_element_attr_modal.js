document.getElementById('editElementAttrModal')
  .addEventListener('show.bs.modal', function(event) {
    const button = event.relatedTarget;
    const modal = this;

    // Шаблон URL обновления из data-атрибута модалки
    const updateUrlTemplate = modal.getAttribute('data-update-url');

    // Получаем ID и текущее значение из кнопки
    const attrId = button.getAttribute('data-attr-id');
    const attrContent = button.getAttribute('data-attr-content') || '';
    const attrName = button.getAttribute('data-attr-name') || '';

    // Находим элементы формы
    const form = modal.querySelector('#editElementAttrForm');
    const idInput = modal.querySelector('#editAttrIdInput');
    const contentInput = modal.querySelector('#editAttrContent');
    const attrNameLabel = modal.querySelector('#editElementAttrModalLabel');

    // Задаем action формы заменой последнего числа (0) на реальный ID атрибута
    form.action = updateUrlTemplate.replace(/0$/, attrId);

    // Заполняем поля
    idInput.value = attrId;
    contentInput.value = attrContent;
    attrNameLabel.textContent = 'Редактировать атрибут ' + attrName;
  });
