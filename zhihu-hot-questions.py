#coding: utf-8
from flask import request, render_template
from flask import Flask
from flask.ext.paginate import Pagination
from flask_bootstrap import Bootstrap

import datetime
import pymongo
from bson import ObjectId

db = pymongo.MongoClient('localhost', 27017).scrapy
app = Flask(__name__)
Bootstrap(app)


#热门问题显示为最近5天的问题
days_ago = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")


#过滤器，将搜索的关键词渲染为黄色北京
@app.template_filter('render_keyword')
def render_keyword(text, key_words):
    text = text.replace(key_words, '<b style="color:black;background-color:#ffff66">'+key_words+'</b>')
    return text

# filters.FILTERS['render_keyword'] = render_keyword


@app.route('/', methods=['GET', 'POST'])
def show():
    all_pages = request.args.get('all_pages', '')

    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    questions_all = []
    key_words = ''
    # 搜索关键字
    if request.method == 'POST':
        key_words = request.form.get('key_word')
        if key_words:
            indexs = db.index.find_one({key_words: {'$exists': True}})
            if indexs:
                ids = [ObjectId(id) for id in indexs[key_words].keys()]
                questions_all = db.zhihu.find({'_id': {"$in": ids}}).sort('answer_count', -1)
    if not questions_all:
        if all_pages:
            questions_all = db.zhihu.find().sort('answer_count', -1)
        else:
            questions_all = db.zhihu.find({'created': {"$gt": days_ago}}).sort('answer_count', -1)
            #如果最近几天没有数据（没有爬数据），则显示前50条数据
            if not questions_all.count():
                questions_all = db.zhihu.find().sort('created', -1).limit(50)

    pagination = Pagination(page=page, total=questions_all.count(True), search=search, record_name='questions')
    pagination.per_page = 30  #每页30个条目

    #pagination插件有问题，这里参考boostrap分页的写法
    links = str(pagination.links).replace('<div class="pagination"><ul>', '<div><ul class="pagination">')

    questions = questions_all[(page-1)*pagination.per_page:page*pagination.per_page]
    return render_template('base.html', questions=questions, pagination=pagination, links=links, key_words=key_words)


if __name__ == '__main__':
    app.run(debug=True)
