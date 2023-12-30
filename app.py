from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from utils.models import Task, init_app, db
from utils.utilities import calculate_duration, validate_date_time

app = Flask(__name__)
init_app(app=app)

# search_criteria = ["taskID", "sprint", "employeeName", "startDate", "endDate", "duration", "remark"]
search_criteria = {
    "Task ID": "taskID",
    "Sprint": "sprint",
    "Employee Name": "employeeName",
    "Start Date": "startDate",
    "End Date": "endDate",
    "Remark": "remark"
}

@app.route('/')
def index():
    tasks = Task.query.all()
    if tasks:
        return render_template('home.html', tasks=tasks, search_criteria=search_criteria.keys())
    else:
        return redirect(url_for('add_task'))


@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'GET':
        return render_template('add_task.html')
    else:
        try:
            validate_date_time(start_date=request.form['startDate'], end_date=request.form['endDate'])
            days, minutes = calculate_duration(start_date_str=request.form['startDate'], end_date_str=request.form['endDate'])
            
            duration = f"{days} days and {minutes} minutes"
            # TODO: add validation for task id.
            task_data = {
                'taskID': request.form['taskID'],
                'sprint': request.form['sprint'],
                'employeeName': request.form['employeeName'],
                'startDate': request.form['startDate'],
                'endDate': request.form['endDate'],
                'remark': request.form['remark'],
            }
            # Adding duration to task_data
            task_data['duration'] = duration

            new_task = Task(**task_data)
            db.session.add(new_task)
            db.session.commit()
        except Exception as e:
            flash(f'error: {e} while adding data', 'error')
        else:
            flash('Task added.', 'success')
            return redirect(url_for('index'))


@app.route('/edit_task/<string:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return render_template('error.html', message='Task not found'), 404
    try:
        if request.method == 'POST':
            validate_date_time(start_date=request.form['startDate'], end_date=request.form['endDate'])
            days, minutes = calculate_duration(start_date_str=request.form['startDate'], end_date_str=request.form['endDate'])
            
            duration = f"{days} days and {minutes} minutes"

            # Update task details based on the form data
            task.sprint = request.form['sprint']
            task.employeeName = request.form['employeeName']
            task.startDate = request.form['startDate']
            task.endDate = request.form['endDate']
            task.remark = request.form['remark']
            task.duration = duration

            db.session.commit()
            flash(f'{task_id} updated successfully', 'success')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'error: {e} while updating {task_id}', 'error')

    return render_template('edit_task.html', task=task)


@app.route('/delete_task/<string:task_id>', methods=['POST'])
def delete_task(task_id):
    task_details = Task.query.get(task_id)
    
    if task_details is None:
        return render_template('error.html', message=f'Details not found for id: {task_id}')
    else:
        db.session.delete(task_details)
        db.session.commit()
        flash(f'Task {task_id} has been deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/confirm_clear', methods=['GET', 'POST'])
def confirm_clear():
    return render_template('confirm_clear.html')


@app.route('/clear_tasks', methods=['GET', 'POST'])
def clear_tasks():
    try:
        # Clear all tasks from the database
        Task.query.delete()
        db.session.commit()
        flash('All tasks have been cleared.', 'success')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db.session.rollback()
        flash('Error occurred while clearing tasks.', 'error')

    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    try:
        search_query = request.form.get('search_query').lower()
        selected_criteria = search_criteria.get(request.form.get('search_criteria'))

        if selected_criteria is None:
            return render_template('error.html', message=f"invalid search criteria {request.form.get('search_criteria')}")
        
        tasks = Task.query.all()
        # Perform search based on the selected criteria
        results = [task for task in tasks if str(getattr(task, selected_criteria)).lower() == search_query]


        return render_template('home.html', tasks=results, search_criteria=search_criteria, selected_criteria=selected_criteria,
                               search_query=search_query, search=True)
    except Exception as e:
        print(f'Error during search: {str(e)}', 'error')


@app.route('/export', methods=['GET', 'POST'])
def export():
    return jsonify("export data feature coming soon...")

if __name__ == '__main__':
    app.run(debug=True)
