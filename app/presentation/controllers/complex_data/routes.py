from flask import render_template, request, redirect, url_for, flash, g, Response

from app.application.dtos.complex_data import CreateComplexElementDto, UpdateComplexElementDto, DeleteComplexElementDto, \
    CreateAttributeForAllDto, UpdateElementAttributeDto, CreateChainForAllDto, UpdateComplexDataDto
from app.application.use_cases.complex_data.create_complex_attribute_for_all import CreateAttributeForAllUseCase
from app.application.use_cases.complex_data.create_complex_data_for_all import CreateComplexDataForAllUseCase
from app.application.use_cases.complex_data.create_complex_element import CreateComplexElementUseCase
from app.application.use_cases.complex_data.delete_complex_element import DeleteComplexElementUseCase
from app.application.use_cases.complex_data.update_complex_attrubute import UpdateElementAttributeUseCase
from app.application.use_cases.complex_data.update_complex_data import UpdateComplexDataUseCase
from app.application.use_cases.complex_data.update_complex_element import UpdateComplexElementUseCase
from app.infrastructure.db.models.complex_data import ComplexDataModel, ComplexElementModel
from . import bp
from app.common_utils import get_folder_path, find_root_data
from app.application.use_cases.complex_data.complex_data_data_service import ComplexDataService

update_complex_data_uc = UpdateComplexDataUseCase()
create_element_uc = CreateComplexElementUseCase()
update_element_uc = UpdateComplexElementUseCase()
delete_element_uc = DeleteComplexElementUseCase()
create_attr_all_uc = CreateAttributeForAllUseCase()
update_attr_uc = UpdateElementAttributeUseCase()
create_complex_data_all_uc = CreateComplexDataForAllUseCase()

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

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll') # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data',data_id=root_data.id, scroll = scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))

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

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll')  # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id, scroll=scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))

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

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll')  # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id, scroll=scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))

@bp.route('/<int:data_id>/create_attribute_all', methods=['POST'])
def create_attribute_all(data_id: int):
    if g.current_user is None:
        flash('Войдите в систему', 'error')
        return redirect(url_for('login.show_login_form'))

    name = request.form.get('attribute_name', '').strip()
    if not name:
        flash('Имя атрибута не может быть пустым', 'danger')
        return redirect(url_for('complex_data.view_complex_data', data_id=data_id))

    dto = CreateAttributeForAllDto(
        data_id=data_id,
        name=name,
        owner_id=g.current_user.id
    )
    try:
        create_attr_all_uc.execute(dto)
        flash('Атрибут создан для всех элементов', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll')  # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id, scroll=scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))

@bp.route('/<int:data_id>/update_element_attr/<int:attr_id>', methods=['POST'])
def update_element_attr(data_id: int, attr_id: int):
    if g.current_user is None:
        flash('Войдите в систему', 'error')
        return redirect(url_for('login.show_login_form'))

    content = request.form.get('content', '').strip()
    dto = UpdateElementAttributeDto(
        id=attr_id,
        data_id=data_id,
        content=content,
        owner_id=g.current_user.id
    )
    try:
        update_attr_uc.execute(dto)
        flash('Значение атрибута сохранено', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll')  # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id, scroll=scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))

@bp.route('/<int:data_id>/create_chain_all', methods=['POST'])
def create_chain_all(data_id: int) -> str | Response:
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    name = request.form.get('chain_name', '').strip()
    comment = request.form.get('chain_comment', '').strip() or None

    if not name:
        flash('Название цепочки не может быть пустым.', 'danger')
        return redirect(url_for('complex_data.view_complex_data', data_id=data_id))

    dto = CreateChainForAllDto(
        data_id=data_id,
        name=name,
        comment=comment,
        owner_id=g.current_user.id
    )
    try:
        create_complex_data_all_uc.execute(dto)
        flash('Подчинённые цепочки созданы для всех элементов.', 'success')
    except ValueError as err:
        flash(str(err), 'danger')

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll')  # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id, scroll=scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))

@bp.route('/<int:data_id>/update_complex_data', methods=['POST'])
def update_complex_data(data_id: int) -> str | Response:
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    name = request.form.get('data_name', '').strip()
    comment = request.form.get('data_comment', '').strip() or None

    if not name:
        flash('Название не может быть пустым.', 'danger')
        return redirect(url_for('complex_data.view_complex_data', data_id=data_id))

    dto = UpdateComplexDataDto(
        id=data_id,
        name=name,
        comment=comment,
        owner_id=g.current_user.id
    )
    try:
        update_complex_data_uc.execute(dto)
        flash('Комплексные данные обновлены.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    root_data = find_root_data(data_id)

    scroll = request.args.get('scroll')  # если он есть — передаем в redirect, иначе просто редирект
    if scroll is not None:
        return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id, scroll=scroll))
    return redirect(url_for('complex_data.view_complex_data', data_id=root_data.id))