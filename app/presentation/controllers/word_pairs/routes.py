from flask import render_template, g, redirect, url_for, flash, Response, request

from app.application.dtos.word_pair import CreateWordPairDto
from app.application.use_cases.create_word_pair import CreateWordPairUseCase
from . import bp
from app.infrastructure.db.models.word_pairs import WordPairSetModel

create_pair_uc = CreateWordPairUseCase()

@bp.route('/<int:set_id>', methods=['GET'])
def view_word_pair_set(set_id):
    # Проверяем, что пользователь залогинен
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    # Ищем набор пар слов, принадлежащий текущему пользователю
    word_set = (
        WordPairSetModel.query
        .filter_by(id=set_id, owner_id=g.current_user.id)
        .first()
    )
    if word_set is None:
        flash('Набор пар слов не найден или доступ запрещён.', 'danger')
        return redirect(url_for('data.user_data'))

    # Строим список вложенных папок (некликабельный путь)
    folders_path = []
    folder = word_set.parent_folder
    while folder:
        folders_path.insert(0, folder)
        folder = folder.parent_folder

    return render_template(
        'word_pair_set.html',
        word_set=word_set,
        folders_path=folders_path
    )

@bp.route('/<int:set_id>/create_pair', methods=['POST'])
def create_pair(set_id: int) -> str | Response:
    # Получаем данные из формы
    word1 = request.form.get('word1', '').strip()
    word2 = request.form.get('word2', '').strip()
    owner_id = g.current_user.id

    # Формируем DTO
    dto = CreateWordPairDto(
        key=word1,
        value=word2,
        set_id=set_id
    )

    # Выполняем UseCase
    try:
        create_pair_uc.execute(dto)
        flash('Пара слов успешно добавлена.', 'success')
    except ValueError as err:
        flash(str(err), 'danger')

    # Перенаправляем обратно на страницу набора
    return redirect(url_for('word_pairs.view_word_pair_set', set_id=set_id))