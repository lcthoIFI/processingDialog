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
import matplotlib.pyplot as plt
import numpy as np

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
    # vectorizer = CountVectorizer()
    # counts = vectorizer.fit_transform(corpus)
    # transformer = TfidfTransformer()
    # tfidf = transformer.fit_transform(counts)
    #
    # svd = TruncatedSVD(40)
    # normalizer = Normalizer(copy=False)
    # lsa = make_pipeline(svd, normalizer)
    #
    # X = lsa.fit_transform(tfidf)
    # testValue = X[0]
    # #print("done in %fs" % (time() - t0))
    #
    # explained_variance = svd.explained_variance_ratio_.sum()
    # print("Explained variance of the SVD step: {}%".format(
    #     int(explained_variance * 100)))
    #
    # # Do action clustering
    # n_cluster = 3
    # # km = MiniBatchKMeans(n_clusters= n_cluster, init='k-means++', n_init=1,
    # #                      init_size=1000, batch_size=1000, )
    #
    # km = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1)
    # km.fit(X)
    #print(km)
    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(corpus)

    dictPaire = {}
    c = 0
    for k, v in distdt.items():
        dictPaire[k] = X[c]
        c = c +1
    ## recalcule
    #print(corpus[0])
    feature_names = vectorizer.get_feature_names()
    # doc = 0
    # feature_index = X[doc, :].nonzero()[1]
    # tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])
    # for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
    #     print(w, s)
    true_k = 3
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    clus = {i: X[np.where(model.labels_ == i)] for i in range(model.n_clusters)}
    #print(clus)
    ##### lỗi combine các dict
    dictT = {}
    for k,v in clus.items():
        dictb = {}
        for item in range(len(v.toarray())):
            for k1,v1 in dictPaire.items():
                if v1.toarray() == item:
                    dictb[k1] = distdt.get(k1)
        dictT[k] = dictb


    ################################
    listt = []
    # for k, v in clus.items():
    #     listc = []
    #     #print('- - ---  Group ' + str(k) +' --- - - ' )
    #     for id in range(len(v.toarray())):
    #
    #         feature_index = X[id, :].nonzero()[1]
    #         tfidf_scores = zip(feature_index, [X[id, x] for x in feature_index])
    #         sentence = ' '
    #         for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
    #             #print(w, s)
    #             sentence = sentence + w + ' '
    #         #print('\n')
    #         listc.append(sentence)
    #     listt.append(listc)
    # for item in listt[1]:
    #     print(item)
    #     print('\n')
    ############################################

    #Plot the results
    # for i in set(model.labels_):
    #     index = model.labels_ == i
    #     plt.plot(X[index, 0], X[index, 1], 'o')
    # plt.show()


    # if opts.n_components:
   # original_space_centroids = svd.inverse_transform(km.cluster_centers_)
    #original_space_centroids = svd.inverse_transform(km.n_clusters)
   # order_centroids = original_space_centroids.argsort()[:, ::-1]
    # else:
    #order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    # terms = vectorizer.get_feature_names()
    #
    # for k, v in clus.items():
    #     original_space = svd.inverse_transform(v)
    #     order_cen = original_space.argsort()[:, ::-1]
    #     for id in range(len(order_cen)):
    #         for ids in order_cen[id]:
    #             print(' %s' % terms[ids], end='')
    #         print('\n')
    #     print('\n')
    #     print('\n')
    # for i in range(3):
    #     print("Cluster %d:" % i, end='')
    #     for ind in order_centroids[i]:
    #         print(' %s' % terms[ind], end='')
    #     print()

if __name__ == "__main__":
    ## Do action extract
    extract()