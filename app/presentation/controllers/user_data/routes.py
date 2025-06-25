
from flask import render_template, redirect, url_for, flash, g
from . import bp

@bp.route('/', methods=['GET'])
def user_data():
    if g.current_user is None:
        flash('Пожалуйста, войдите в систему.', 'error')
        return redirect(url_for('login.show_login_form'))

    return render_template('user_data.html')