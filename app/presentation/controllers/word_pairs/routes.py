from flask import render_template, g, redirect, url_for, flash
from . import bp
from app.infrastructure.db.models.word_pairs import WordPairSetModel

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