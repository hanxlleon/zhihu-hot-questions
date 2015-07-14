#coding: utf-8
from flask import Flask

app = Flask(__name__)


from flask import Flask
# from flask.ext.mongoengine import MongoEngine
import pymongo



db = pymongo.MongoClient('localhost', 27017).scrapy


@app.route('/')
def hello_world():
    row_list = []
    template = u"<html><head><title>知乎热门问题</title></head><body><table><tr><th>问题</th><th>关注人数</th><th>回答数</th></tr>%s</table></body></html>"
    row = u"<tr><td><a href='{url}' target=_bland>{question}</a></td><td>{follow_count}</td><td>{answer_count}</td></tr>"
    for item in db.zhihu.find().sort('follow_count', -1):
        row_list.append(row.format(url=item['url'], question=item['question'], follow_count=item['follow_count'],
                                   answer_count=item['answer_count']))

    return template % ''.join(row_list)


if __name__ == '__main__':
    app.run()
