from flask import Blueprint,render_template,request
from common.exception import BizException
from common.result import success,exception
import urllib


tool = Blueprint('tool', __name__)
@tool.route('/tool/list')
def render_tool_list():
    return render_template('tool/list.html')


@tool.route('/tool/url_endec')
def render_url_decode():
    return render_template('tool/url_endec.html')


@tool.route('/api/tool/url_decode', methods=['GET','POST'])
def api_url_decode():
    try:
        input = request.json['input']
        output = urllib.unquote(input)
        return success(output)
    except Exception as e:
        return exception(e)


@tool.route('/api/tool/url_encode', methods=['GET', 'POST'])
def api_url_encode():
    try:
        input = request.json['input']
        output = urllib.quote(input)
        return success(output)
    except Exception as e:
        return exception(e)
