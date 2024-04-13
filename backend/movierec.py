import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

def ModelTraining():
    credits = pd.read_csv('credits.csv')
    movies = pd.read_csv('movies.csv')
    
    movies = movies.merge(credits, on = 'title')
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace = True)
    
    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    def convert3(obj):
        L = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter !=3:
                L.append(i['name'])
                counter += 1
            else: 
                break
        return L

    movies['cast'] = movies['cast'].apply(convert)
    def director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L
    
    movies['crew'] = movies['crew'].apply(director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(' ', '') for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(' ', '') for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(' ', '') for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(' ', '') for i in x])
    
    movies['tags'] = movies['overview'] + movies['genres'] + movies['cast'] + movies['crew'] + movies['keywords']
    
    global new 
    new = movies[['movie_id', 'title', 'tags']]
    new['tags'] = new['tags'].apply(lambda x: ' '.join(x))
    new['tags'] = new['tags'].apply(lambda x : x.lower())
    
    cv = CountVectorizer(max_features = 5000, stop_words = 'english')
    vectors = cv.fit_transform(new['tags']).toarray()
    
    ps = PorterStemmer()
    
    def stem(text):
        y = []
        for i in text.split():
            y.append(ps.stem(i))
        return " ".join(y)
    
    new['tags'] = new['tags'].apply(stem)
    
    global similarity
    similarity = cosine_similarity(vectors)
    sorted(list(enumerate(similarity[0])), reverse = True, key = lambda x: x[1])[1:6]
    
def RecoModel(InputMovie):
    movies = []
    def recommend(movie):
        if len(new[new['title'] == movie]) == 0:
            return None
        movie_index = new[new['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]

        for i in movies_list:
            movies.append(new.iloc[i[0]].title)
            
    recommend(str(InputMovie))
    return movies