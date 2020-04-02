from flask import Blueprint, jsonify, request
from . import db_session, jobs

blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/jobs')
def get_all_jobs():
    session = db_session.create_session()
    all_jobs = session.query(jobs.Jobs).all()
    return jsonify(
        {
            "jobs":
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                    for item in all_jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_one_job(job_id):
    session = db_session.create_session()
    one_job = session.query(jobs.Jobs).get(job_id)
    if not one_job:
        return jsonify({"error": "Not found"})
    else:
        return jsonify(
            {
                "job": one_job.to_dict(only=(
                    'id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
            }
        )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'work_size', 'job', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    a = session.query(jobs.Jobs.id).all()
    print(a)
    if not request.json['id'] in session.query(jobs.Jobs.id).all()[0]:
        job = jobs.Jobs(
            id=request.json['id'],
            start_date=request.json['start_date'],
            end_date=request.json['end_date'],
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'Id already exists'})
