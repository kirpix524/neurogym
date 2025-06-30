from flask import render_template, redirect, url_for, flash, g, request
from werkzeug import Response

from app.application.dtos.folder import CreateFolderDto
from app.application.use_cases.create_folder import CreateFolderUseCase
from app.application.use_cases.delete_folder import DeleteFolderUseCase
from app.application.use_cases.user_data import DataService
from . import bp

create_folder_uc = CreateFolderUseCase()
delete_folder_uc = DeleteFolderUseCase()

@bp.route('/', methods=['GET'])
def user_data():
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    # получаем из query-параметров id родительской папки (None для корня)
    parent_folder_id = request.args.get('parent_id', type=int)

    service = DataService()
    data_units = service.get_data_units(
        owner_id=g.current_user.id,
        parent_folder_id=parent_folder_id
    )
    # формируем «хлебные крошки»
    breadcrumbs = service.get_folder_path(
        owner_id=g.current_user.id,
        parent_folder_id=parent_folder_id
    )
    # ссылка «..» ведёт на уровень выше, если он есть
    parent_up_id = breadcrumbs[-2].id if len(breadcrumbs) > 1 else None

    return render_template(
        'user_data.html',
        data_units=data_units,
        breadcrumbs=breadcrumbs,
        parent_folder_id=parent_folder_id,
        parent_up_id=parent_up_id
    )

@bp.route('/create_folder', methods=['POST'])
def create_folder():
    name = request.form.get('folder_name', '').strip()
    comment = request.form.get('folder_comment', '').strip() or None
    parent_id = request.form.get('parent_id', type=int)

    if not name:
        flash('Название папки не может быть пустым.', 'danger')
        return redirect(url_for('data.user_data', parent_id=parent_id))

    dto = CreateFolderDto(
        name=name,
        comment=comment,
        owner_id=g.current_user.id,
        parent_id=parent_id
    )
    create_folder_uc.execute(dto)

    flash('Папка успешно создана.', 'success')
    return redirect(url_for('data.user_data', parent_id=parent_id))

@bp.route('/delete_folder/<int:folder_id>', methods=['POST'])
def delete_folder(folder_id: int) -> str | Response:
    parent_id = request.args.get('parent_id', type=int)
    try:
        delete_folder_uc.execute(
            folder_id=folder_id,
            owner_id=g.current_user.id
        )
        flash('Папка удалена.', 'success')
    except ValueError as err:
        flash(str(err), 'danger')
    return redirect(url_for('data.user_data', parent_id=parent_id))