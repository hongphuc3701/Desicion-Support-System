from flask import Flask,render_template,request
import pickle
import numpy as np

popular = pickle.load(open('popular.pkl','rb'))
toprated1 = pickle.load(open('toprated1.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           read=list(popular['Book-Rating'].values),
                           rating=list(popular['avg_rating'].values)
                           )

@app.route('/toprated')    
def topratedbook():
    return render_template('toprated.html',
                           book_name= list(toprated1['Book-Title'].values),
                           author=list(toprated1['Book-Author'].values),
                           image=list(toprated1['Image-URL-M'].values),
                           read=list(toprated1['Book-Rating'].values),
                           rating=list(toprated1['avg_rating'].values),
                           score=list(toprated1['score'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)