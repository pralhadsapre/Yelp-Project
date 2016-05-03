import sys
import pymongo

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from textblob import TextBlob

def main():
    try:
        c = MongoClient('localhost', 27017)
    except ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e

    # getting a handle to the database
    db = c["projectDB"]
    print "Database connected successfully"

    sentimentDict = {}

    count = 1
    review_cursor = db.reviews.find()
    for one_review in review_cursor:
    	# if "sentiment" not in one_review:
    	if True:
    		
    		one_review["sentiment"] = TextBlob(one_review["text"]).sentiment.polarity
    		sentimentDict[one_review["review_id"]] = one_review

    	count += 1
    	sys.stdout.write("\r" + "%d reviews processed" % count)
    	sys.stdout.flush()

    print ""
    count = 1
    for key_val in sentimentDict:    	
    	db.reviewsSentiment.insert(sentimentDict[key_val])

    	sys.stdout.write("\r" + "%d reviews inserted" % count)
    	sys.stdout.flush()
    	count += 1

    print ""
    print "Reviewing sentiments done!"

    c.close()

if __name__ == "__main__":
    main()     