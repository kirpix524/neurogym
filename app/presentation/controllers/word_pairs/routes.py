from flask import render_template, g, redirect, url_for, flash, Response, request

from app.application.dtos.word_pair import CreateWordPairDto
from app.application.use_cases.create_word_pair import CreateWordPairUseCase
from app.application.use_cases.delete_word_pair import DeleteWordPairUseCase
from app.application.use_cases.word_pairs import WordPairDataService
from app.common_utils import get_folder_path
from . import bp
from app.infrastructure.db.models.word_pairs import WordPairSetModel

create_pair_uc = CreateWordPairUseCase()
delete_pair_uc = DeleteWordPairUseCase()


@bp.route('/<int:set_id>', methods=['GET'])
def view_word_pair_set(set_id: int) -> str | Response:
    # Требуем аутентификации
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    service = WordPairDataService()
    # Получаем сам набор
    word_set = service.get_word_pair_set(
        owner_id=g.current_user.id,
        set_id=set_id
    )
    # Список пар в наборе
    pairs = service.get_word_pairs(
        owner_id=g.current_user.id,
        set_id=set_id
    )
    # «Хлебные крошки» по папкам
    folders_path = get_folder_path(word_set.parent_folder)

    return render_template(
        'word_pair_set.html',
        word_set=word_set,
        pairs=pairs,
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

@bp.route('/<int:set_id>/delete_pair/<int:pair_id>', methods=['POST'])
def delete_pair(set_id: int, pair_id: int) -> str | Response:
    """
    Удаляет слово из набора и возвращает на страницу просмотра набора.
    """
    try:
        delete_pair_uc.execute(pair_id=pair_id, set_id=set_id)
        flash('Пара слов удалена.', 'success')
    except ValueError as err:
        flash(str(err), 'danger')
    return redirect(url_for('word_pairs.view_word_pair_set', set_id=set_id))