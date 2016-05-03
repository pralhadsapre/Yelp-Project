import sys
import pymongo
import TopicModeler as tm
import pickle

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def main():
    try:
        c = MongoClient('localhost', 27017)
    except ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e
        
    # getting a handle to the database
    db = c["projectDB"]            
    print "Businesses database connected successfully"
    
    reviewsSet = []

    count = 1       
    query = {"sentiment" : { "$lt" : -0.05 }}
    for review in db.reviewsSentiment.find(query):                                            
        if count > 1000:
            reviewsSet.append(review["text"])
            sys.stdout.write("\r" + "%d reviews processed" % count)
            sys.stdout.flush()

        if count > 1100:
            break

        count += 1
    
    print ""
    print "Reviews processing done!"   

    # topics = ["Food in general",
    #             "Service Speed & Delivery",
    #             "Bar & Liquor",
    #             "Cafe Menu & Service",
    #             "Staff's Attitude",
    #             "Meat Menu & Kitchen Hygiene",
    #             "Fast Food Items",
    #             "Seafood Menu Items",
    #             "Ambiance & Hospitality",
    #             "Dinner & Drinks"]
    # pickle.dump(topics, open("trained-model-topics",'w'))
    # topics = []

    topics = pickle.load(file("trained-model-topics"))
    ldaModel = pickle.load(file("trained-negative-model"))
    ldaDictionary = pickle.load(file("model-dictionary"))

    print "Dictionary and Trained Model loaded!"
    # print ldaModel.show_topics(num_topics=10, num_words=10, formatted=False)
    for item in reviewsSet:
        topics_found = []
        models = ldaModel[ldaDictionary.doc2bow(tm.getWordVector(item))]
        models = sorted(models, key=lambda k: k[1], reverse = True)
        # print models
        # if len(models) == 2:
        #     print "-"*5 + str(topics[models[0][0]]) + "-"*5 + str(topics[models[1][0]]) + "-"*5
        #     print item
        for single_topic in models:
            topics_found.append(topics[single_topic[0]])
            if len(topics_found) > 2:
                break

        print "-"*5 + str(topics_found) + "-"*5
        print item

    c.close()
        
if __name__ == "__main__":
    main()            
               