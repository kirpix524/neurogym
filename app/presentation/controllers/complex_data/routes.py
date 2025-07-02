from flask import render_template, g, redirect, url_for, flash
from . import bp
from app.infrastructure.db.models.complex_data import ComplexDataModel

@bp.route('/<int:data_id>', methods=['GET'])
def view_complex_data(data_id: int):
    # 1. Только для залогиненных
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    # 2. Ищем комплексные данные у текущего пользователя
    complex_data = (
        ComplexDataModel.query
        .filter_by(id=data_id, owner_id=g.current_user.id)
        .first()
    )
    if complex_data is None:
        flash('Комплексные данные не найдены или доступ запрещён.', 'danger')
        return redirect(url_for('data.user_data'))

    # 3. Собираем путь (breadcrumb) до папки
    folders_path = []
    folder = complex_data.folder
    while folder:
        folders_path.insert(0, folder)
        folder = folder.parent_folder

    return render_template(
        'complex_data.html',
        complex_data=complex_data,
        folders_path=folders_path
    )
