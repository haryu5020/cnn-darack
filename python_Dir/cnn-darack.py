import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data

tf.reset_default_graph()

x = tf.placeholder(tf.float32, [None, 784])
x_image = tf.reshape(x, [-1, 28, 28, 1])

W_conv1 = tf.Variable(tf.truncated_normal([5, 5, 1, 32],stddev=0.1))
h_conv1 = tf.nn.conv2d(x_image, W_conv1, strides=[1,1,1,1], padding='SAME')
b_conv1 = tf.Variable(tf.constant(0.1, shape=[32]))
h_conv1_cutoff = tf.nn.relu(h_conv1 + b_conv1)
h_pool1 = tf.nn.max_pool(h_conv1_cutoff,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

W_conv2 = tf.Variable(tf.truncated_normal([5, 5, 32, 64],stddev=0.1))
h_conv2 = tf.nn.conv2d(h_pool1, W_conv2, strides=[1,1,1,1], padding='SAME')
b_conv2 = tf.Variable(tf.constant(0.1, shape=[64]))
h_conv2_cutoff = tf.nn.relu(h_conv2 + b_conv2)
h_pool2 = tf.nn.max_pool(h_conv2_cutoff, ksize=[1,2,2,1], strides=[1,2,2,1], padding = 'SAME')

h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])

W2 = tf.Variable(tf.truncated_normal([7*7*64, 1024]))
b2 = tf.Variable(tf.constant(0.1, shape = [1024]))
hidden2 = tf.nn.relu(tf.matmul(h_pool2_flat,W2)+b2)

keep_prob = tf.placeholder(tf.float32)
hidden2_drop = tf.nn.dropout(hidden2, keep_prob)


w0 = tf.Variable(tf.zeros([1024, 10]))
b0 = tf.Variable(tf.zeros([10]))
k = tf.matmul(hidden2_drop, w0) + b0
p = tf.nn.softmax(k)


# prepare session
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
saver.restore(sess, '/Users/SungHyunJun/cnn_session')

print('reload has been done')

from PIL import Image

img_list = []

img = Image.open('/Users/SungHyunJun/Documents/Workspace/cnn-darack/uploads/save.png')
img_temp = img.resize((28, 28))

img_arr = np.array(img_temp.convert('L'),dtype=int)

for i in range(0,28) :
    for j in range(0,28) :
        if np.any(img_arr[i, j] == 255):
            img_list.append(0)
        elif np.any(img_arr[i, j] == 0):
            img_list.append(1)

p_val = sess.run(p, feed_dict={x:[img_list], keep_prob:1.0})
pred = p_val[0]
img_temp.show()
print(pred.argmax())


# In[ ]:
'''
conv1_vals, cutoff1_vals = sess.run(
    [h_conv1, h_conv1_cutoff], feed_dict={x:[img_list], keep_prob:1.0})

fig = plt.figure(figsize=(16,4))

for f in range(32):
    subplot = fig.add_subplot(4, 16, f+1)
    subplot.set_xticks([])
    subplot.set_yticks([])
    subplot.imshow(conv1_vals[0,:,:,f],
                   cmap=plt.cm.gray_r, interpolation='nearest') 
plt.show()


# In[ ]:

fig = plt.figure(figsize=(16,4))

for f in range(32):
    subplot = fig.add_subplot(4, 16, f+1)
    subplot.set_xticks([])
    subplot.set_yticks([])
    subplot.imshow(cutoff1_vals[0,:,:,f],
                   cmap=plt.cm.gray_r, interpolation='nearest') 
    
plt.show()


# In[ ]:



'''

