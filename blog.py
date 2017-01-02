#coding:utf-8
import sys
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash,jsonify
import MySQLdb.cursors
import markdown,hashlib,time,functools


reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.debug = True
app.secret_key = "super secret key"

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='blog', charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
conn.ping(True)

class BizException(Exception):
        def __init__(self, msg):
            super(BizException, self).__init__(msg)


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


def require_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if "user" not in session or session["user"] is None:
            if request.method == 'GET':
                return redirect(url_for('render_login'))
            else:
                return exception(BizException('未登录'))
        return func(*args, **kw)
    return wrapper


@app.context_processor
def inject_file_hash():
    return dict(file_hash=hashlib.md5(str(time.time())).hexdigest())


@app.route('/login')
def render_login():
    return render_template("login.html")


@app.route('/')
def render_home():
    return render_template("home.html")


@app.route('/article/detail/<int:article_id>')
def render_article(article_id):
    try:
        cursor = conn.cursor()
        cursor.execute('update tbl_article set pv = coalesce(pv, 0) + 1 where id =' + str(article_id))
        conn.commit()
        sql = '''
            select t1.*,t2.real_name as author
            from tbl_article t1
            left join tbl_user t2
            on t1.cid = t2.id
            where t1.id = %s
        '''
        cursor.execute(sql, [article_id])
        article = cursor.fetchone()
        return render_template("article_detail.html", article=article)
    except Exception as e:
        return exception(e)


@app.route('/article/new')
@require_login
def render_article_new():
    return render_template('article_edit.html', article={})


@app.route('/article/list')
def render_article_list():
    cursor = conn.cursor()
    cursor.execute('select * from tbl_article where stat = 0')
    articles = cursor.fetchall()
    return render_template('article_list.html')


@app.route('/article/api/get_article_list', methods=['GET','POST'])
def api_get_article_list():
    try:
        start = request.json['start']
        length = request.json['length']
        cursor = conn.cursor()
        where_cond = 'where stat = 0'
        if 'user' in session and session['user'] is not None:
            where_cond = ''
        sql = '''
        select t1.*,t2.real_name as author
        from tbl_article t1
        left join tbl_user t2
        on t1.cid = t2.id
        %s
        limit %d,%d
        ''' % (where_cond, start, length)
        cursor.execute(sql)
        article_list = cursor.fetchall()
        for article in article_list:
            article['ctime'] = article['ctime'].strftime('%y/%m/%d')

        return success(article_list)
    except Exception as e:
        return exception(e)



@app.route('/article/edit/<int:article_id>')
@require_login
def render_article_edit(article_id):
    cursor = conn.cursor()
    cursor.execute("select * from tbl_article where id = %s" % article_id)
    article = cursor.fetchone()
    return render_template("article_edit.html", article=article)


@app.route('/article/api/get_article', methods=['GET', 'POST'])
def api_get_article():
    article_id = request.json['article_id']
    cursor = conn.cursor()
    cursor.execute("select * from tbl_article where id = %s" % article_id)
    article = cursor.fetchone()
    return jsonify({
        'status': 'OK',
        'article': article
    })


@app.route('/article/api/add_article', methods=['POST'])
@require_login
def api_add_article():
    try:
        title = request.json['title']
        content = request.json['content']
        html = request.json['html']
        stat = request.json['stat']
        if title is None or len(title) == 0:
            raise BizException("标题不能为空！")
        # The format string is not really a normal Python format string. You must always use %s for all fields
        sql = "insert into tbl_article(title, content, html, stat, cid, uid,  ctime, utime) VALUES(%s, %s, %s, %s, %s, %s,  %s, %s)"

        cursor = conn.cursor()
        user_id = session['user']['id']
        # print sql % (title, content, html, '0', user_id, user_id, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(sql, [title, content, html, stat, user_id, user_id, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')])
        conn.commit()
        id = cursor.lastrowid
        return success(id)
    except BizException as e:
        return exception(e)
    except Exception, e:
        return exception(e)


@app.route('/article/api/update_article', methods=['POST'])
@require_login
def api_update_article():
    try:
        article_id = request.json['article_id']
        title = request.json['title']
        content = request.json['content']
        html = request.json['html']
        stat = request.json['stat']

        if title is None or len(title) == 0:
            raise BizException("标题不能为空！")
        # The format string is not really a normal Python format string. You must always use %s for all fields
        sql = "update tbl_article set title=%s, content=%s, html=%s, stat=%s, uid=%s, utime=%s where id = %s"
        cursor = conn.cursor()
        user_id = session['user']['id']
        cursor.execute(sql, [title, content, html, stat, user_id, time.strftime('%Y-%m-%d %H:%M:%S'), article_id])
        conn.commit()
        return success(article_id)
    except BizException as e:
        return exception(e)
    except Exception, e:
        return exception(e)


@app.route('/user/api/login', methods=['GET', 'POST'])
def user_api_login():
    login_name = request.json['login_name']
    password = request.json['password']
    cursor = conn.cursor()
    cursor.execute("select * from tbl_user where login_name = '%s';" % login_name)
    user = cursor.fetchone()
    password = hashlib.md5(password).hexdigest()
    if user is not None or password == user['password']:
        session["user"] = user
        return jsonify({
            'status': 'OK'
        })
    else:
        return jsonify({
            'status': 'ERROR',
            'message': '密码错误，请重试！'
        })


if __name__ == '__main__':
    app.run()