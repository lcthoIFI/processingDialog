#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from proces_dialog import *
from sklearn.cluster import KMeans, MiniBatchKMeans

def getDictDt():
    readDtList = getListData()
    lisdt = correctSentenceQA(readDtList)
    return extract_respons_sentenses(lisdt)

def extract():
    distdt= getDictDt()
    corpus = []
    ### get all value in dictionary
    for k,v in distdt.items():
        corpus.append(v)

    ##  count vector
    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(corpus)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(counts)

    svd = TruncatedSVD(40)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    X = lsa.fit_transform(tfidf)

    #print("done in %fs" % (time() - t0))

    explained_variance = svd.explained_variance_ratio_.sum()
    print("Explained variance of the SVD step: {}%".format(
        int(explained_variance * 100)))

    # Do action clustering
    n_cluster = 3
    # km = MiniBatchKMeans(n_clusters= n_cluster, init='k-means++', n_init=1,
    #                      init_size=1000, batch_size=1000, )

    km = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1)
    km.fit(X)
    #print(km)

    # if opts.n_components:
    original_space_centroids = svd.inverse_transform(km.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    # else:
    #order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(3):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i]:
            print(' %s' % terms[ind], end='')
        print()

if __name__ == "__main__":
    ## Do action extract
    extract()