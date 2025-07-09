document.getElementById('complexElementModal')
  .addEventListener('show.bs.modal', function(event) {
    const button    = event.relatedTarget;
    const modal     = this;

    // Для создания:
    const createUrl = button.getAttribute('data-create-url');

    // Для редактирования (как было раньше)
    const updateUrlTemplate = modal.getAttribute('data-update-url');

    // Проверяем, есть ли data-element-id
    const elementId = button.getAttribute('data-element-id');
    const elementName = button.getAttribute('data-element-name') || '';

    // Элементы формы
    const form            = modal.querySelector('#complexElementForm');
    const titleEl         = modal.querySelector('.modal-title');
    const submitBtn       = modal.querySelector('#complexElementSubmitBtn');
    const elementIdInput  = modal.querySelector('#elementIdInput');
    const nameInput       = modal.querySelector('#elementName');

    if (elementId) {
      // Редактируем существующий
      titleEl.textContent   = 'Редактировать элемент';
      form.action           = updateUrlTemplate.replace(/0$/, elementId);
      submitBtn.textContent = 'Сохранить';
      elementIdInput.value  = elementId;
      nameInput.value       = elementName;
    } else {
      // Создаем новый в нужной цепочке
      titleEl.textContent   = 'Новый элемент цепочки';
      form.action           = createUrl;      // берём созданный URL
      submitBtn.textContent = 'Добавить';
      elementIdInput.value  = '';
      nameInput.value       = '';
    }
  });
