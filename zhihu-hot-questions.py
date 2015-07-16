#coding: utf-8
from flask import Blueprint, request, redirect, render_template, url_for
from flask import Flask
from flask.ext.paginate import Pagination
from flask_bootstrap import Bootstrap
import datetime
import pymongo

db = pymongo.MongoClient('localhost', 27017).scrapy
app = Flask(__name__)
Bootstrap(app)


days_ago = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")

@app.route('/test')
def test():
    return render_template('base.html')


@app.route('/')
def show():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    questions_all = db.zhihu.find({'created': {"$gt": days_ago}}).sort('answer_count', -1)


    pagination = Pagination(page=page, total=questions_all.count(), search=search, record_name='questions')
    pagination.per_page = 30

    links = str(pagination.links).replace('<div class="pagination"><ul>', '<div><ul class="pagination">')

    questions = questions_all[(page-1)*pagination.per_page:page*pagination.per_page]
    return render_template('base.html', questions=questions, pagination=pagination, links=links)


@app.route('/all')
def show_all():
    # row_list = []
    # template = u"<html><head><title>知乎热门问题</title></head><body><table><tr><th>问题</th><th>关注人数</th><th>回答数</th><th>时间</th></tr>%s</table></body></html>"
    # row = u"<tr><td><a href='{url}' target=_bland>{question}</a></td><td>{follow_count}</td><td>{answer_count}</td><td>{created}</td></tr>"
    # for item in db.zhihu.find().sort('created', -1):
    #     row_list.append(row.format(url=item['url'], question=item['question'], follow_count=item['follow_count'],
    #                                answer_count=item['answer_count'], created=item['created']))
    #
    # return template % ''.join(row_list)


    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    questions_all = db.zhihu.find().sort('created', -1)


    pagination = Pagination(page=page, total=questions_all.count(), search=search, record_name='questions')
    pagination.per_page = 30

    links = str(pagination.links).replace('<div class="pagination"><ul>', '<div><ul class="pagination">')

    questions = questions_all[(page-1)*pagination.per_page:page*pagination.per_page]
    return render_template('base.html', questions=questions, pagination=pagination, links=links)


if __name__ == '__main__':
    app.run(debug=True)
