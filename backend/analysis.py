# reference: https://www.geeksforgeeks.org/python/python-sentiment-analysis-using-vader/
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_score(sentence):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = analyzer.polarity_scores(sentence)
    #for our purposes we only return the compound sentiment
    return sentiment_dict["compound"]


#test
if __name__ == "__main__":
    print("positive")
    print(sentiment_score("I had a great day today! It was fantastic"))
    print("negative")
    print(sentiment_score("I had a horrible day. I want to die"))
    print("neutral")
    print(sentiment_score("My day today was fairly average I would say. Didn't get up to much."))