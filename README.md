coreference-baseline
====================

implemented system refer to "a machine learning approach for pronoun resolution in spoken document"

utterance segmentation: 
* use speaker turns;
* when overlapping, if time is continuous, merge the fragments (reduce 20% segments than without merging)

data generation:
* consider word token in pronoun list as candidates required resolution
* generate pair with all antecedent objects in the conversation

Feature:
* phrase-level: grammar function, depth in parsing tree 
  (from stanford parser, not use dependency feature yet)
* coreference-level:distance (words, objects, speaker_turns)

learning approach:
* weka J48 decision tree (not resampling for avoiding unbalance)

Initial result:
20%-30% object annotation include pronoun
150,000 training samples (<5% positive pairs), 50,000 test samples
=== Detailed Accuracy By Class ===

               TP Rate FP Rate Precision Recall F-Measure ROC Area Class
                 0.126 0.004 0.642 0.126 0.21 0.675 True
                 0.996 0.874 0.957 0.996 0.976 0.675 False
Weighted Avg. 0.954 0.831 0.941 0.954 0.938 0.675

=== Confusion Matrix ===

      a b <-- classified as
    940 6532 | a = True
    525 143876 | b = False

Feature importance based on Information Gain:
* ate_grammar > ana_grammar > object_dist > word_dist > speaker_turns 
>ate_dep>ana_dep

Detailed prediction result on test set:
* ErrorAnalysis/train10-test5-DT/raw_test.error
