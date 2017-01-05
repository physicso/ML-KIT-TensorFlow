import mnist_input_data
import tensorflow as tf

mnist = mnist_input_data.read_data_sets("MNIST_data/", one_hot=True)

# Create the model
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 10])
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy)

# Train
training_iteration = 10000
batch_size = 100
display_step = 50
with tf.Session() as sess:
	sess.run(tf.initialize_all_variables())
	for iter in range(training_iteration):
		batch_xs, batch_ys = mnist.train.next_batch(batch_size)
		train_step.run({x: batch_xs, y_: batch_ys})
		if iter % display_step == 0:
			print "Epoch:", '%04d' % (iter + 1), "accuracy =", "{:.9f}".format(
				sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys}))
	print "Test Accuracy: " + "{:.9f}".format(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
