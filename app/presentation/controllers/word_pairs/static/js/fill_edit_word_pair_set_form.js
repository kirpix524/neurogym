document.getElementById('editWordPairSetModal')
  .addEventListener('show.bs.modal', function (event) {
    const btn        = event.relatedTarget;
    const modal      = this;
    const updateUrl  = modal.getAttribute('data-update-url');
    const setId      = btn.getAttribute('data-set-id');
    const name       = btn.getAttribute('data-name') || '';
    const comment    = btn.getAttribute('data-comment') || '';

    const form       = modal.querySelector('#wordPairSetForm');
    const idInput    = modal.querySelector('#setIdInput');
    const nameInput  = modal.querySelector('#setName');
    const commInput  = modal.querySelector('#setComment');
    const submitBtn  = modal.querySelector('#setSubmitBtn');

    form.action      = updateUrl;
    idInput.value    = setId;
    nameInput.value  = name;
    commInput.value  = comment;
    submitBtn.textContent = 'Сохранить';
  });