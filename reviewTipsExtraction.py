import sys
import pymongo
import TopicModeler as tm

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
    tipsSet = []
    
    # find query will give us all the rows
  
    # businesses_results = db.businesses.find()
    # businesses_results.count()
    # for item in range(1000):        
    #    query = {"business_id" : unicode(businesses_results[item]["business_id"])}                
        
    count = 1       
    query = {"sentiment" : { "$lt" : -0.05 }}
    for review in db.reviewsSentiment.find(query):                                    
        reviewsSet.append(review["text"])
        sys.stdout.write("\r" + "%d reviews processed" % count)
        sys.stdout.flush()
        count += 1
        # if count == 10:
        #     break
    
    print "\nReviews processing done!"    
    tm.buildTopicModel(reviewsSet)

    # count = 1  
    # for tip in db.tips.find():
    #     tipsSet.append(tip["text"])
    #     sys.stdout.write("\r" + "%d tips processed" % count)
    #     sys.stdout.flush()
    #     count += 1
    #     # if count == 10000:
    #         # break

    # print "\nTips processing done!"
    # tm.analyzeSentiment(reviewsSet)
            
    # print "Reviews %d" % db.reviews.find(query).count()
    # print "Tips %d" % db.tips.find(query).count()   
    c.close()        
    
    # print "Topic modelling the reviews ... "
    # tm.buildTopicModel(reviewsSet)
    
    # print "Topic modelling the tips ... "
    # tm.buildTopicModel(tipsSet)
        
if __name__ == "__main__":
    main()            
               