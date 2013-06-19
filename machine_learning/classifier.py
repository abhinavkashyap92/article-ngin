import Orange


def get_classifier():
	articles = Orange.data.Table("training_set.tab")
	learner = Orange.classification.bayes.NaiveLearner()
	classifier_ = learner(articles)

	test_input = Orange.data.Table("input.tab")


	for eachInput in test_input:
		print classifier_(eachInput)

	

get_classifier()