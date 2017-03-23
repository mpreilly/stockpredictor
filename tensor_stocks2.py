import tensorflow as tf
import numpy as np

NUM_FEATURES = 10
NUM_CLASSES = 2

def readToLines(file, skip1row1col):
    with open(file) as f:
        lines = f.read().splitlines()
    splitLines = []

    # adds the list of each stock's stats within the list of lines
    if skip1row1col:
        for i, line in enumerate(lines):
            if i != 0:  # Skips first row
                splitLines += [line.split(',')[1:]] # Skips stock symbols
    else:
        for i, line in enumerate(lines):
            splitLines += [line.split(',')]

    return splitLines

def makeFeatureArray(file):
    splitLines = readToLines(file, True)
    # features is an array with a row for each stock, and all 10 features for each one
    features = np.zeros([len(splitLines), NUM_FEATURES])

    for i, line in enumerate(splitLines):

        for j, item in enumerate(line):
            features[i, j] = item

    return features

def makeLabelArray(file):
    splitLines = readToLines(file, False)
    #labels is an array with a row for each stock, and two columns to label each (one-hot)
    labels = np.zeros([len(splitLines), NUM_CLASSES])

    negCounter = 0
    print splitLines
    # one-hot encoding: puts 1 in first col if class 1, second col if class 2
    for i, line in enumerate(splitLines):
        if float(line[0]) > 0:
            labels[i, 0] = 1
        else:
            labels[i, 1] = 1

    return labels



inputs = tf.placeholder(tf.float32, [None, NUM_FEATURES])

W = tf.Variable(tf.zeros([NUM_FEATURES, NUM_CLASSES]))
b = tf.Variable(tf.zeros([NUM_CLASSES]))

#predicted labels:
output = tf.nn.softmax(tf.matmul(inputs,W) + b)

#correct labels
true_labels = tf.placeholder(tf.float32, [None, NUM_CLASSES])

# loss function: cross entropy
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    labels=true_labels, logits=output))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

train_features = makeFeatureArray('data/training_1day_data.csv')
train_labels = makeLabelArray('data/training_1day_nextdaychanges.csv')
# Train
for _ in range(1000):
    sess.run(train_step, feed_dict={inputs:train_features, true_labels:train_labels})

# Boolean array of whether it made the correct predictions
correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(true_labels, 1))

#cast booleans to floats and take mean
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

test_features = makeFeatureArray('data/testing_1day_data.csv')
test_labels = makeLabelArray('data/testing_1day_nextdaychanges.csv')
# run session on test data to calculate accuracy, print
print(sess.run(accuracy, feed_dict={inputs:test_features, true_labels:test_labels}))

amd = [5.42,-2.17,12774357,0.70,2.66,-14.10,34.16,7.11,0.9202037351443124]
amdArray = np.zeros([1, NUM_FEATURES])
for i, item in enumerate(amd):
    amdArray[0, i] = item
print(sess.run(output, feed_dict={inputs:amdArray}))
