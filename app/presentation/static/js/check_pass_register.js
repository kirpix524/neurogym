(function() {
  const form = document.getElementById('registerForm');
  const pwd = form.querySelector('#password');
  const confirm = form.querySelector('#password_confirm');

  // При отправке формы проверяем пароли
  form.addEventListener('submit', function(event) {
    if (pwd.value !== confirm.value) {
      confirm.classList.add('is-invalid');
      event.preventDefault();
      event.stopPropagation();
    }
  });

  // Сбрасываем ошибку при вводе нового значения
  confirm.addEventListener('input', function() {
    if (confirm.classList.contains('is-invalid')) {
      confirm.classList.remove('is-invalid');
    }
  });
})();