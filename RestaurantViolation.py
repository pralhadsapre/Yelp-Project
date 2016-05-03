import datetime as dt
from textblob import TextBlob

import TopicModeler as tm

class RestaurantViolation:
	def __init__(self, dataDict):
		self.dict = {}
		self.dict["restaurant_id"] = dataDict["restaurant_id"]
		self.dict["violations"] = []
		self.negativeCorpus = []

	# will be fed a row from the violations data set
	def addViolation(self, dataDict):
		tempDict = {}
		# print dt.datetime.strptime(dataDict["date"], '%Y-%m-%d').date().year
		tempDict["date"] = dt.datetime.strptime(dataDict["date"], '%Y-%m-%d').date().year
		tempDict["*"] = dataDict["*"]
		tempDict["**"] = dataDict["**"]
		tempDict["***"] = dataDict["***"]

		tempDict["count*"] = 1.0 if dataDict["*"] > 0 else 0.0
		tempDict["count**"] = 1.0 if dataDict["**"] > 0 else 0.0
		tempDict["count***"] = 1.0 if dataDict["***"] > 0 else 0.0
		
		isPresent = False
		for item in self.dict["violations"]:
			if item["date"] == tempDict["date"]:
				item["*"] += tempDict["*"]
				item["**"] += tempDict["**"]
				item["***"] += tempDict["***"]

				item["count*"] += tempDict["count*"]
				item["count**"] += tempDict["count**"]
				item["count***"] += tempDict["count***"]

				isPresent = True

		if not isPresent:
			self.dict["violations"].append(tempDict)

	# will be fed one review at a time and will figure out the overall sentiment in that year
	def addReview(self, reviewDict):
		polarity = reviewDict["sentiment"]

		tempDict = {}		
		tempDict["date"] = dt.datetime.strptime(reviewDict["date"], '%Y-%m-%d').date().year
		tempDict["negative"] = 0
		tempDict["positive"] = 0
		tempDict["neutral"] = 0
		tempDict["sentiment"] = polarity
		tempDict["count"] = 1
		tempDict["stars"] = reviewDict["stars"]

		if polarity < -0.05:
			tempDict["negative"] += 1
			for word in tm.getWordVector(reviewDict["text"]):
				self.negativeCorpus.append(word)

		elif polarity > 0.05:
			tempDict["positive"] += 1
		else:
			tempDict["neutral"] += 1

		isPresent = False
		for item in self.dict["violations"]:
			if item["date"] == tempDict["date"]:

				if "sentiment" not in item:
					item["negative"] = tempDict["negative"]
					item["positive"] = tempDict["positive"]
					item["neutral"] = tempDict["neutral"]
					item["sentiment"] = tempDict["sentiment"]
					item["stars"] = tempDict["stars"]
					item["count"] = tempDict["count"]					
				else:	
					item["negative"] += tempDict["negative"]
					item["positive"] += tempDict["positive"]
					item["neutral"] += tempDict["neutral"]
					item["sentiment"] += tempDict["sentiment"]
					item["stars"] += tempDict["stars"]
					item["count"] += tempDict["count"]			
				
				isPresent = True

		if not isPresent:
			self.dict["violations"].append(tempDict)         

	def setYelpIDs(self, yelpDataDict):
		self.dict["yelp_ID"] = []

		if yelpDataDict["yelp_id_0"]:
			self.dict["yelp_ID"].append(yelpDataDict["yelp_id_0"])

		if yelpDataDict["yelp_id_1"]:
			self.dict["yelp_ID"].append(yelpDataDict["yelp_id_1"])

		if yelpDataDict["yelp_id_2"]:
			self.dict["yelp_ID"].append(yelpDataDict["yelp_id_2"])

		if yelpDataDict["yelp_id_3"]:
			self.dict["yelp_ID"].append(yelpDataDict["yelp_id_3"])

	def getDictionary(self):
		for item in self.dict["violations"]:
			
			if "sentiment" in item:
				item["stars"] /= float(item["count"])
				item["sentiment"] /= item["count"]			
				item.pop("count")		

			if "count*" in item:
				item["*"] /= item["count*"] if item["count*"] > 0 else 1
				item["**"] /= item["count**"] if item["count**"] > 0 else 1
				item["***"] /= item["count***"] if item["count***"] > 0 else 1

				item.pop("count*")
				item.pop("count**")
				item.pop("count***")

		self.dict["checklist"] = []
		if len(self.negativeCorpus) > 0:
			self.dict["checklist"] = tm.getTopics(self.negativeCorpus)

		return self.dict

	def getYelpIDs(self):
		return self.dict["yelp_ID"]

