from flask import Flask, request
from pydantic import ValidationError

from utils import execute_query
from models import BatchRequestsModel

app = Flask(__name__)


@app.route("/perform_query/", methods=['POST'])
def perform_query():
    data = request.json

    try:
        BatchRequestsModel(**data)
    except ValidationError:
        return app.response_class('Bad request!', status=400)

    result = None
    for query in data['queries']:
        result = execute_query(
            file_name=data['file_name'],
            cmd=query['cmd'],
            value=query['value'],
            data=result
        )

    return app.response_class('\n'.join(result), status=200)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
