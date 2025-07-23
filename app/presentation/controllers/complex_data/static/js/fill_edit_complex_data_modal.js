document.getElementById('editComplexDataModal')
  .addEventListener('show.bs.modal', function(event) {
    const trigger = event.relatedTarget;
    const modal   = this;

    // URL для отправки формы
    const updateUrl = modal.getAttribute('data-update-url');

    // Данные из атрибутов кнопки
    const dataId    = trigger.getAttribute('data-data-id');
    const name      = trigger.getAttribute('data-data-name') || '';
    const comment   = trigger.getAttribute('data-data-comment') || '';

    // Элементы формы
    const form     = modal.querySelector('#editComplexDataForm');
    const nameInput  = modal.querySelector('#complexDataName');
    const commentInput = modal.querySelector('#complexDataComment');
    const submitBtn   = modal.querySelector('#editComplexDataSubmit');

    // Кнопка «Добавить атрибут»
    const attrBtn = modal.querySelector('button[data-bs-target="#createAttributeAllModal"]');
    if (attrBtn) {
      attrBtn.setAttribute('data-data-id', dataId);
    }

    // Кнопка «Добавить цепочку»
    const chainBtn = modal.querySelector('button[data-bs-target="#createChainAllModal"]');
    if (chainBtn) {
      chainBtn.setAttribute('data-data-id', dataId);
    }

    // Устанавливаем action, значения полей и текст кнопки
    form.action        = updateUrl;
    nameInput.value    = name;
    commentInput.value = comment;
    submitBtn.textContent = 'Сохранить';
  });
