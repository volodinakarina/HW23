import os
from typing import Optional, Iterable

from flask import abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def read_file_by_chunks(file: str) -> list:
    """
    File descriptor as a generator
    """
    with open(file, 'r', encoding='utf-8') as f:
        buffer = []
        for line in f.readlines():
            buffer.append(line.strip())
        if len(buffer) == 10:
            yield buffer
            buffer = []
        if buffer:
            yield buffer


def execute_query(file_name: str, cmd: str, value: str, data: Optional[Iterable[str]]) -> list[str]:
    """
    Execute command 'cmd' with parameter 'value'
    """
    if data is None:
        if not os.path.isfile(os.path.join(DATA_DIR, file_name)):
            abort(400)

        path = os.path.join(DATA_DIR, file_name)
        prep_data = []
        for chunk in read_file_by_chunks(path):
            prep_data += chunk
    else:
        prep_data = data

    func = CMD_TO_FUNC[cmd]
    try:
        return func(prep_data, value)
    except:
        abort(400)


def filter_data(data: list[str], value: str) -> list:
    """
    Filter data by content text in records
    """
    return list(filter(lambda text: value in text, data))


def map_data(data: list[str], value: str) -> list:
    """
    Filter data by a specific column
    """
    return list(map(lambda text: text.split(' ')[int(value)], data))


def unique_data(data: list[str], *args, **kwargs) -> list:
    """
    Filter by unique data
    """
    return list(set(data))


def sort_data(data: list[str], order: str) -> list:
    """
    Sort data in ascending/descending order
    """
    return sorted(data, reverse=True if order == 'desc' else False)


def limit_data(data: list[str], limit: str) -> list:
    """
    Limit the number of records
    """
    limit = int(limit)
    if limit < 0:
        limit = 0
    return data[:limit]


CMD_TO_FUNC = {
    'filter': filter_data,
    'map': map_data,
    'unique': unique_data,
    'sort': sort_data,
    'limit': limit_data,
}