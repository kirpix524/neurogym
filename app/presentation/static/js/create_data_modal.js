document.addEventListener('DOMContentLoaded', function() {
  var modal = document.getElementById('createDataModal');
  if (!modal) return;
  modal.addEventListener('show.bs.modal', function (e) {
    var trigger = e.relatedTarget;
    var type = trigger.getAttribute('data-type');
    var parentId = trigger.getAttribute('data-parent-id');
    var title = type === 'word_pair_set'
                ? 'Создать набор пар слов'
                : 'Создать комплексные данные';
    var nameLabel = type === 'word_pair_set'
                ? 'Имя набора пар слов'
                : 'Имя комплексных данных';
    document.getElementById('createDataModalLabel').textContent = title;
    document.getElementById('dataNameLabel').textContent = nameLabel;
    document.getElementById('dataTypeInput').value = type;
    document.getElementById('dataParentInput').value = parentId;
  });
});
