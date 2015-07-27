from flask import Flask

from flask_restful import reqparse, Api, Resource

from lib.result import create_ga_screen_result
from lib.util import valid_date
import settings
from tasks.google_analitycs import GAScreenMaker

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('password', required=True)
parser.add_argument('start_date', type=valid_date, required=True)
parser.add_argument('end_date', type=valid_date, required=True)

class Task(Resource):
    def get(self, task_uid):
        celery_result = GAScreenMaker().AsyncResult(task_uid)
        result = None
        if celery_result.state == 'SUCCESS':
            result = create_ga_screen_result(task_uid)
        return {'uid': task_uid, 'state': celery_result.state, 'result': result}

class TaskList(Resource):
    def post(self):
        args = parser.parse_args()
        celery_task = GAScreenMaker()
        result = celery_task.delay(**args)
        return result.id, 201


api.add_resource(Task, '/tasks/<task_uid>')
api.add_resource(TaskList, '/tasks')

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
