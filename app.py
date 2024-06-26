from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd


popular_books= pd.read_pickle('popular_books.pkl')
book_pivot= pd.read_pickle('book_pivot.pkl')
books= pd.read_pickle('books.pkl')
similarity_score= pd.read_pickle('similarity_score.pkl')


app = Flask(__name__)

@app.route('/top_books')
def index():
    return render_template('index.html',
                           book_names= list(popular_books['title'].values),
                           authors=list(popular_books['author'].values),
                           votes=list(popular_books['num_ratings'].values),
                           ratings=list(popular_books['avg_ratings'].values),
                           images=list(popular_books['image'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=["post"])
def recommend():
    user_input= request.form.get("user_input")
    book_index = np.where(book_pivot.index == user_input)[0][0]
    suggested_items = sorted(list(enumerate(similarity_score[book_index])), key=lambda x: x[1], reverse=True)[1:5]
    book_list = list(books["title"].values)

    data = []
    for i in suggested_items:
        item = []
        temp = books[books["title"] == book_pivot.index[i[0]]]
        item.extend(temp.drop_duplicates("title")['title'].values)
        item.extend(temp.drop_duplicates("title")['author'].values)
        item.extend(temp.drop_duplicates("title")['image'].values)

        data.append(item)
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)