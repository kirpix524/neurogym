document.getElementById('wordPairModal')
  .addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const modal = this;

    const createUrl = modal.getAttribute('data-create-url');
    const updateUrlTemplate = modal.getAttribute('data-update-url');

    const pairId = button.getAttribute('data-pair-id');
    const w1 = button.getAttribute('data-word1') || '';
    const w2 = button.getAttribute('data-word2') || '';

    const form = modal.querySelector('#wordPairForm');
    const titleEl = modal.querySelector('.modal-title');
    const submitBtn = modal.querySelector('#wordPairSubmitBtn');
    const pairIdInput = modal.querySelector('#pairIdInput');
    const word1Input = modal.querySelector('#word1');
    const word2Input = modal.querySelector('#word2');

    if (pairId) {
      titleEl.textContent = 'Редактировать пару';
      form.action = updateUrlTemplate.replace(/-1$/, pairId);
      submitBtn.textContent = 'Сохранить';
      pairIdInput.value = pairId;
      word1Input.value = w1;
      word2Input.value = w2;
    } else {
      titleEl.textContent = 'Новая пара слов';
      form.action = createUrl;
      submitBtn.textContent = 'Добавить';
      pairIdInput.value = '';
      word1Input.value = '';
      word2Input.value = '';
    }
  });
