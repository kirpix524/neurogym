  document.getElementById('createFolderModal')
  .addEventListener('show.bs.modal', function (event) {
    const button      = event.relatedTarget;
    const folderId    = button.getAttribute('data-folder-id');
    const parentId    = button.getAttribute('data-parent-id')     || '';
    const name        = button.getAttribute('data-folder-name')   || '';
    const comment     = button.getAttribute('data-folder-comment')|| '';

    const modal       = this;
    const titleEl     = modal.querySelector('.modal-title');
    const form        = modal.querySelector('#folderForm');
    const idInput     = modal.querySelector('#folderIdInput');
    const parentInput = modal.querySelector('#parentIdInput');
    const nameInput   = modal.querySelector('#folderName');
    const commentInput= modal.querySelector('#folderComment');
    const submitBtn   = modal.querySelector('#folderSubmitBtn');

    // читаем URL из data-атрибутов модалки
    const createUrl   = modal.getAttribute('data-create-url');
    const updateUrl   = modal.getAttribute('data-update-url');

    if (folderId) {
      titleEl.textContent    = 'Редактировать папку';
      form.action            = updateUrl;
      idInput.value          = folderId;
      submitBtn.textContent  = 'Сохранить';
    } else {
      titleEl.textContent    = 'Создать новую папку';
      form.action            = createUrl;
      idInput.value          = '';
      submitBtn.textContent  = 'Создать';
    }

    parentInput.value  = parentId;
    nameInput.value    = name;
    commentInput.value = comment;
  });