from flask import Flask,render_template,request
import pickle
import numpy as np

popular = pickle.load(open('popular.pkl','rb'))
toprated1 = pickle.load(open('toprated1.pkl','rb'))
foryou = pickle.load(open('user_item.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))


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


@app.route('/foryou')
def foryou_ui():
    return render_template('foryou.html')

@app.route('/foryou_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(foryou[index])), key=lambda x: x[1], reverse=True)[1:10]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('foryou.html',data=data)
@app.route('/sameap')
def sameap_ui():
    return render_template('sameap.html')

@app.route('/sameap_books',methods=['POST'])


def get_books():
    name = request.form.get('user_input')
    d = data_processed[data_processed['Book-Title'] == name]
    au = d['Book-Author'].unique()

    data = data_processed[data_processed['Book-Title'] != name]

    if au[0] in list(data['Book-Author'].unique()):
        k2 = data[data['Book-Author'] == au[0]]
    k2 = k2.sort_values(by=['Book-Rating']).drop_duplicates(subset=['Book-Title'])
    k3 = k2.head(10)
    k3 = k3.merge(rating_avg_round,on='Book-Title')
    
    pu = d['Publisher'].unique()

    if pu[0] in list(data['Publisher'].unique()):
        k4 = data[data['Publisher'] == pu[0]]
    k4 = k4.sort_values(by=['Book-Rating']).drop_duplicates(subset=['Book-Title'])
    k5 = k4.head(10)
    k5 = k5.merge(rating_avg_round,on='Book-Title')
    
        
    return render_template('sameap.html',
                           book_name_k3= list(k3['Book-Title'].values),
                           image_k3=list(k3['Image-URL-M'].values),
                           read_k3=list(k3['Book-Rating'].values),
                           rating_k3=list(k3['avg_rating'].values),
                           author=list(k3['Book-Author'].values),
                           publisher=list(k5['Publisher'].values),
                           book_name_k5= list(k5['Book-Title'].values),
                           image_k5=list(k5['Image-URL-M'].values),
                           read_k5=list(k5['Book-Rating'].values),
                           rating_k5=list(k5['avg_rating'].values),
                           authork5=list(k5['Book-Author'].values)
                           )

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    
