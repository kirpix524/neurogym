from flask import render_template, request, redirect, url_for, flash, g, Response

from app.application.dtos.complex_data import CreateComplexElementDto
from app.application.use_cases.complex_data.create_complex_element import CreateComplexElementUseCase
from . import bp
from app.common_utils import get_folder_path
from app.application.use_cases.complex_data.complex_data_data_service import ComplexDataService

create_element_uc = CreateComplexElementUseCase()

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

@bp.route('/<int:data_id>/create_element', methods=['POST'])
def create_element(data_id: int) -> str | Response:
    # Только для авторизованных
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    name = request.form.get('element_name', '').strip()
    if not name:
        flash('Название элемента не может быть пустым.', 'danger')
        return redirect(url_for('complex_data.view_complex_data', data_id=data_id))

    dto = CreateComplexElementDto(
        name=name,
        data_id=data_id,
        content='',
        comment='',
        owner_id=g.current_user.id
    )
    try:
        create_element_uc.execute(dto)
        flash('Элемент цепочки добавлен.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('complex_data.view_complex_data', data_id=data_id))