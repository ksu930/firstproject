from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('43.201.23.207', 27017, username="test", password="test")
db = client.dbsparta_plus_week2


@app.route('/')
def home():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    logs = list(db.logs.find({}, {"_id": False}))
    return render_template("home.html", logs=logs)



@app.route('/api/save_log', methods=['POST'])
def save_log():
    # 단어 저장하기
    title_receive = request.form['title_give']
    link_receive = request.form['link_give']
    comment_receive = request.form['comment_give']
    doc = {"title": title_receive, "link": link_receive, "comment": comment_receive}
    db.logs.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '저장완료'})


@app.route('/api/delete_log', methods=['POST'])
def delete_log():
    # 단어 삭제하기
    word_receive = request.form['word_give']
    db.words.delete_one({"word": word_receive})
    db.examples.delete_many({"word": word_receive})
    return jsonify({'result': 'success', 'msg': f'word "{word_receive}" deleted'})

@app.route('/api/get_comment', methods=['GET'])
def get_exs():
    word_receive = request.args.get("word_give")
    result = list(db.examples.find({"word": word_receive}, {'_id': 0}))
    print(word_receive, len(result))

    return jsonify({'result': 'success', 'examples': result})


@app.route('/api/save_comment', methods=['POST'])
def save_ex():
    word_receive = request.form['word_give']
    example_receive = request.form['example_give']
    doc = {"word": word_receive, "example": example_receive}
    db.examples.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'example "{example_receive}" saved'})


@app.route('/api/delete_comment', methods=['POST'])
def delete_ex():
    word_receive = request.form['word_give']
    number_receive = int(request.form["number_give"])
    example = list(db.examples.find({"word": word_receive}))[number_receive]["example"]
    print(word_receive, example)
    db.examples.delete_one({"word": word_receive, "example": example})
    return jsonify({'result': 'success', 'msg': f'example #{number_receive} of "{word_receive}" deleted'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
