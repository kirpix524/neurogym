from datetime import datetime

from flask import render_template, redirect, url_for, flash, g, request
from app.application.dtos.folder import CreateFolderDto
from app.application.use_cases.create_folder import CreateFolderUseCase
from app.application.use_cases.user_data import DataService
from . import bp

create_folder_uc = CreateFolderUseCase()

@bp.route('/', methods=['GET'])
def user_data():
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    service = DataService()
    data_units = service.get_data_units(
        owner_id=g.current_user.id,
        parent_folder_id=None
    )
    return render_template('user_data.html', data_units=data_units)

@bp.route('/create_folder', methods=['POST'])
def create_folder():
    name = request.form.get('folder_name', '').strip()
    comment = request.form.get('folder_comment', '').strip() or None

    if not name:
        flash('Название папки не может быть пустым.', 'danger')
        return redirect(url_for('data.user_data'))

    dto = CreateFolderDto(name=name, comment=comment, owner_id=g.current_user.id)
    create_folder_uc.execute(dto)

    flash('Папка успешно создана.', 'success')
    return redirect(url_for('data.user_data'))