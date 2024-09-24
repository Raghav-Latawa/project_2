from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import nltk
from nltk.corpus import stopwords
import pandas as pd

nltk.download('stopwords')
stopwords = stopwords.words('english')
candidates = ['bernie', 'sanders', 'elizabeth', 'warren', 'pete', 'mayor', 'joe', 'biden', 'kamala', 'harris', 'buttigieg']
stopwords.extend(candidates)
tokenizer = RegexpTokenizer(r'\w+')

allTweetsdf = pd.read_csv("/home/kapil/PycharmProjects/Political-Opinion-Mining/Candidate_AND_Every_Other_Topic_Query_Tweets/all_candidates_tweets.csv")

p_stemmer = PorterStemmer()

doc_set = []
for i in range(0, allTweetsdf.shape[0]):
  

    doc_set.append(allTweetsdf.iloc[i]['text'])


texts = []

for i in doc_set:

    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

  
    stopped_tokens = [i for i in tokens if not i in stopwords]


    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    texts.append(stemmed_tokens)


dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]


ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word = dictionary, passes=20)

print(ldamodel.print_topics(num_topics=2, num_words=4))

print(ldamodel.print_topics(num_topics=3, num_words=3))
