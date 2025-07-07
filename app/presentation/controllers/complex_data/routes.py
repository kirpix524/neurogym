from flask import render_template, g, redirect, url_for, flash, Response
from . import bp
from app.common_utils import get_folder_path
from app.application.use_cases.complex_data.complex_data_data_service import ComplexDataService

@bp.route('/<int:data_id>', methods=['GET'])
def view_complex_data(data_id: int) -> str | Response:
    # Только для авторизованных
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    # Загружаем комплексные данные и их элементы
    try:
        complex_data = ComplexDataService().get_complex_data(
            owner_id=g.current_user.id,
            data_id=data_id
        )
    except ValueError as err:
        flash(str(err), 'danger')
        return redirect(url_for('data.user_data'))

    # Хлебные крошки по папке
    folders_path = get_folder_path(complex_data.folder_id)

    return render_template(
        'complex_data.html',
        complex_data=complex_data,
        folders_path=folders_path
    )
