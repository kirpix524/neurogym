document.getElementById('complexElementModal')
  .addEventListener('show.bs.modal', function(event) {
    const btn                 = event.relatedTarget;
    const modal               = this;
    const createUrl           = modal.getAttribute('data-create-url');
    const updateUrlTemplate   = modal.getAttribute('data-update-url');
    const elementId           = btn.getAttribute('data-element-id');
    const elementName         = btn.getAttribute('data-element-name') || '';

    const form                = modal.querySelector('#complexElementForm');
    const titleEl             = modal.querySelector('.modal-title');
    const submitBtn           = modal.querySelector('#complexElementSubmitBtn');
    const elementIdInput      = modal.querySelector('#elementIdInput');
    const elementNameInput    = modal.querySelector('#elementName');

    if (elementId) {
      // редактирование
      titleEl.textContent         = 'Редактировать элемент';
      form.action                 = updateUrlTemplate.replace(/0$/, elementId);
      submitBtn.textContent       = 'Сохранить';
      elementIdInput.value        = elementId;
      elementNameInput.value      = elementName;
    } else {
      // создание нового
      titleEl.textContent         = 'Новый элемент цепочки';
      form.action                 = createUrl;
      submitBtn.textContent       = 'Добавить';
      elementIdInput.value        = '';
      elementNameInput.value      = '';
    }
  });