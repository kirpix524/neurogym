from flask import render_template, request, redirect, url_for, flash, g, Response

from app.application.dtos.complex_data import CreateComplexElementDto, UpdateComplexElementDto, DeleteComplexElementDto
from app.application.use_cases.complex_data.create_complex_element import CreateComplexElementUseCase
from app.application.use_cases.complex_data.delete_complex_element import DeleteComplexElementUseCase
from app.application.use_cases.complex_data.update_complex_element import UpdateComplexElementUseCase
from . import bp
from app.common_utils import get_folder_path
from app.application.use_cases.complex_data.complex_data_data_service import ComplexDataService

create_element_uc = CreateComplexElementUseCase()
update_element_uc = UpdateComplexElementUseCase()
delete_element_uc = DeleteComplexElementUseCase()

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

@bp.route('/<int:data_id>/update_element/<int:element_id>', methods=['POST'])
def update_element(data_id: int, element_id: int) -> str | Response:
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    name = request.form.get('element_name', '').strip()
    if not name:
        flash('Название элемента не может быть пустым.', 'danger')
        return redirect(url_for('complex_data.view_complex_data', data_id=data_id))

    dto = UpdateComplexElementDto(
        id=element_id,
        name=name,
        content='',
        comment='',
        data_id=data_id,
        owner_id=g.current_user.id
    )
    try:
        update_element_uc.execute(dto)
        flash('Элемент цепочки обновлён.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('complex_data.view_complex_data', data_id=data_id))

@bp.route('/<int:data_id>/delete_element/<int:element_id>', methods=['POST'])
def delete_element(data_id: int, element_id: int) -> str | Response:
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    dto = DeleteComplexElementDto(
        id=element_id,
        data_id=data_id,
        owner_id=g.current_user.id
    )
    try:
        delete_element_uc.execute(dto)
        flash('Элемент цепочки удалён.', 'success')
    except ValueError as err:
        flash(str(err), 'danger')

    return redirect(url_for('complex_data.view_complex_data', data_id=data_id))