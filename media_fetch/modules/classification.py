import numpy as np
import pandas as pd
import nltk
import re
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import os

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import warnings  # Hide Warnings

warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)
# Show text full width
pd.set_option('display.max_colwidth', None)

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
train_path = os.path.join(project_dir, 'data', 'train.csv')
test_path = os.path.join(project_dir, 'data', 'test.csv')

train = pd.read_csv(train_path)
test = pd.read_csv(test_path)


def feature_adding(df):
    df['len'] = df.text.apply(lambda x: len(x))
    df['words'] = df.text.apply(lambda x: len(nltk.word_tokenize(x)))
    df['numbers'] = df.text.apply(lambda x: len(re.findall(r'\d+,*\d+|\d+', x)))
    df['sent'] = df.text.apply(lambda x: len(nltk.sent_tokenize(x)))
    df['hashtags'] = df.text.apply(lambda x: len(re.findall(r'#', x)))
    # extract hashtags
    df['tags'] = df.text.str.lower().apply(lambda x: " ".join([i for i in re.findall(r'#([A-Za-z]+)', x)]))
    df['mentions'] = df.text.apply(lambda x: len(re.findall(r'@', x)))
    # extract mentions
    df['mentionText'] = df.text.str.lower().apply(lambda x: " ".join([i for i in re.findall(r'@([A-Za-z0-9_.]+)', x)]))
    df['links'] = df.text.apply(lambda x: len(re.findall(r'http', x)))
    df['density'] = df.words / df.len
    # Punctuation count per tweet lenght
    df['punctuation'] = df.text.apply(lambda x: len(re.findall(r'[^A-Za-z0-9\s]', x)) / len(x))
    # Uppercase letters count per tweet lenght
    df['upper'] = df.text.apply(lambda x: len(re.findall(r'[A-Z]', x)) / len(x))
    # Scale
    scaler = MinMaxScaler()
    df[['len', 'words', 'numbers', 'sent', 'hashtags', 'mentions', 'links']] = scaler.fit_transform(
        df[['len', 'words', 'numbers', 'sent', 'hashtags', 'mentions', 'links']])
    return df


def process_tweet(df):
    # lower Case:
    df['tweet'] = df.text.apply(lambda x: x.lower())
    # Remove urls:
    df['tweet'] = df['tweet'].str.replace(r'http[^\s]+', " ")
    # Remove Punctuation
    df['tweet'] = df['tweet'].str.replace(r'[^A-Za-z0-9\s]', "")
    # Remove short words <=2 chars
    df['tweet'] = df['tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 2]))
    # remove stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    df['tweet'] = df['tweet'].apply(lambda x: " ".join(
        [i for i in nltk.word_tokenize(x) if i not in stopwords]))
    # Lemmatization
    lma = nltk.WordNetLemmatizer()
    df['tweet'] = df['tweet'].apply(lambda x: " ".join(
        [lma.lemmatize(i) for i in nltk.word_tokenize(x)]))
    # get dummy for keyword column
    df = pd.concat([df.drop('keyword', axis=1),
                    pd.get_dummies(df['keyword'], dummy_na=True)], axis=1)

    return df


def remove_repetitive(df):
    tfidf = TfidfVectorizer(min_df=1).fit_transform(df['tweet'])
    pairwise_similarity = tfidf * tfidf.T
    pairwise_similarity.setdiag(np.nan)
    similarTweets = df.iloc[list(set(pairwise_similarity.indices[pairwise_similarity.data >= 0.95]))]
    df.drop(similarTweets.index, axis=0, inplace=True)
    return df


def tfidf(df, isTrain):
    if isTrain:
        global vectTweet
        vectTweet = TfidfVectorizer(min_df=5, ngram_range=(1, 3)).fit(df['tweet'])
        global vectTags
        vectTags = TfidfVectorizer(min_df=2).fit(df['tags'])
        global vectMentions
        vectMentions = TfidfVectorizer(min_df=2).fit(df['mentionText'])

    dfVect = vectTweet.transform(df['tweet'])
    df_tags = vectTags.transform(df['tags'])
    df_mentions = vectMentions.transform(df['mentionText'])
    df = df.reset_index()
    df.drop('index', inplace=True, axis=1)
    df_all = pd.concat([df.drop(['tags', 'tweet', 'mentionText'], axis=1),
                        pd.DataFrame.sparse.from_spmatrix(df_tags),
                        pd.DataFrame.sparse.from_spmatrix(dfVect),
                        pd.DataFrame.sparse.from_spmatrix(df_mentions)], axis=1)
    return df_all


def pipeline(df, isTrain: bool):
    if isTrain:
        duplicatdDF = train[train.text.str.lower().duplicated()].sort_values(by='text')
        train.drop(duplicatdDF.index, axis=0, inplace=True)
    newDF = feature_adding(df)
    newDF = process_tweet(newDF)
    if isTrain:
        newDF = remove_repetitive(newDF)
    newDF = tfidf(newDF, isTrain)
    newDF.drop(['id', 'location', 'text'], axis=1, inplace=True)
    return newDF


def classify():
    newTrain = pipeline(train, True)

    testIDs = test.id
    newTest = pipeline(test, False)

    X_tr, X_te, y_tr, y_te = train_test_split(newTrain.drop('target', axis=1),
                                              newTrain['target'])
    X_tr.shape

    X_tr = X_tr.to_numpy()
    mnBayes = MultinomialNB(alpha=0.15).fit(X_tr, y_tr)
    X_te = X_te.to_numpy()
    print(mnBayes.score(X_tr, y_tr))
    print(mnBayes.score(X_te, y_te))

    svm = SVC(C=5, gamma=0.04).fit(scipy.sparse.csr_matrix(X_tr), y_tr)
    print(svm.score(X_tr, y_tr))
    print(svm.score(X_te, y_te))

    newTest.columns = newTest.columns.astype(str)
    test_predictions_nb = mnBayes.predict(newTest)
    test_predictions_svm = svm.predict(scipy.sparse.csr_matrix(newTest))

    test['target_nb'] = test_predictions_nb
    test['target_svm'] = test_predictions_svm

    result_nb = test[test['target_nb'] == 1]
    result_svm = test[test['target_svm'] == 1]

    result_nb.to_csv('nb_predictions_target_1.csv', index=False)
    result_svm.to_csv('svm_predictions_target_1.csv', index=False)

    print(f"NB模型预测为 target=1 的推文保存到 nb_predictions_target_1.csv，共 {len(result_nb)} 条")
    print(f"SVM模型预测为 target=1 的推文保存到 svm_predictions_target_1.csv，共 {len(result_svm)} 条")
