from flask import render_template, redirect, url_for, flash, g, request
from werkzeug import Response

from app.application.dtos.complex_data import CreateComplexDataDto
from app.application.dtos.folder import CreateFolderDto, UpdateFolderDto
from app.application.dtos.word_pair_set import CreateWordPairSetDto
from app.application.use_cases.complex_data.create_complex_data import CreateComplexDataUseCase
from app.application.use_cases.folders.create_folder import CreateFolderUseCase
from app.application.use_cases.word_pairs.create_word_pair_set import CreateWordPairSetUseCase
from app.application.use_cases.complex_data.delete_complex_data import DeleteComplexDataUseCase
from app.application.use_cases.folders.delete_folder import DeleteFolderUseCase
from app.application.use_cases.word_pairs.delete_word_pair_set import DeleteWordPairSetUseCase
from app.application.use_cases.folders.update_folder import UpdateFolderUseCase
from app.application.use_cases.user_data import DataService
from . import bp

create_folder_uc = CreateFolderUseCase()
delete_folder_uc = DeleteFolderUseCase()
update_folder_uc = UpdateFolderUseCase()
word_pair_uc = CreateWordPairSetUseCase()
complex_data_uc = CreateComplexDataUseCase()
delete_pairs_uc = DeleteWordPairSetUseCase()
delete_complex_data_uc = DeleteComplexDataUseCase()

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
        parent_up_id=parent_up_id,
        edit_folder=None
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
    try:
        create_folder_uc.execute(dto)
    except ValueError as err:
        flash(str(err), 'danger')
        return redirect(url_for('data.user_data', parent_id=parent_id))

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

@bp.route('/update_folder', methods=['POST'])
def update_folder() -> str | Response:
    folder_id = request.form.get('folder_id', type=int)
    parent_id = request.form.get('parent_id', type=int)
    name = request.form.get('folder_name', '').strip()
    comment = request.form.get('folder_comment', '').strip() or None

    if not name:
        flash('Название папки не может быть пустым.', 'danger')
        return redirect(url_for('data.user_data', parent_id=parent_id))

    dto = UpdateFolderDto(
        id=folder_id,
        name=name,
        comment=comment,
        owner_id=g.current_user.id,
        parent_id=parent_id
    )
    try:
        update_folder_uc.execute(dto)
        flash('Папка обновлена.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('data.user_data', parent_id=parent_id))

@bp.route('/create_data_item', methods=['POST'])
def create_data_item():
    name = request.form.get('data_name', '').strip()
    comment = request.form.get('data_comment', '').strip() or None
    data_type = request.form.get('data_type')
    parent_folder_id = request.form.get('parent_folder_id') or None
    parent_folder_id = int(parent_folder_id) if parent_folder_id else None

    if not name:
        flash('Название не может быть пустым.', 'danger')
        return redirect(url_for('data.user_data', parent_id=parent_folder_id))

    owner_id = g.current_user.id
    if data_type == 'word_pair_set':
        dto = CreateWordPairSetDto(name, comment, parent_folder_id, owner_id)
        word_pair_uc.execute(dto)
        flash('Набор пар слов создан.', 'success')
    elif data_type == 'complex_data':
        dto = CreateComplexDataDto(name, comment, parent_folder_id, owner_id)
        complex_data_uc.execute(dto)
        flash('Комплексные данные созданы.', 'success')
    else:
        flash('Неизвестный тип данных.', 'danger')

    return redirect(url_for('data.user_data', parent_id=parent_folder_id))

@bp.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_data_item(item_id: int) -> str | Response:
    parent_id = request.args.get('parent_id', type=int)
    item_type = request.args.get('item_type', type=str)
    try:
        if item_type == 'пары слов':
            delete_pairs_uc.execute(
                item_id=item_id,
                owner_id=g.current_user.id
            )
            flash('Набор пар слов удален.', 'success')
            return redirect(url_for('data.user_data', parent_id=parent_id))
        if item_type == 'комплексные данные':
            delete_complex_data_uc.execute(
                item_id=item_id,
                owner_id=g.current_user.id
            )
            flash('Комплексные данные удалены.', 'success')
            return redirect(url_for('data.user_data', parent_id=parent_id))
    except ValueError as err:
        flash(str(err), 'danger')
    return redirect(url_for('data.user_data', parent_id=parent_id))