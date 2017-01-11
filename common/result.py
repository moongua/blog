from exception import BizException
from flask import jsonify
def success(data):
    return jsonify({
        'status': 'OK',
        'msg': '',
        'data': data
    })


def exception(arg):
    if isinstance(arg, basestring): #compatible with unicode
        return jsonify({
            'status': 'ERROR',
            'msg': arg,
            'data': None
        })
    if isinstance(arg, BizException):
        return jsonify({
            'status': 'BIZ_ERROR',
            'msg': arg.message,
            'data': None
        })
    if isinstance(arg, Exception):
        return jsonify({
            'status': 'ERROR',
            'msg': arg.message,
            'data': None
        })
