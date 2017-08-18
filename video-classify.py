import math
import sys
import os
import cv2
import tensorflow as tf


video_path = sys.argv[1]


label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("output/label.txt")]
				   
with tf.gfile.FastGFile("output/output_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
	
with tf.Session() as sess:
	video_p = cv2.VideoCapture(video_path) 
	i = 1 
        success = True
	while video_p.isOpened(): 
                success,frame = video_p.read()
                cv2.imwrite("screens/" + str(i) + "frame.jpg" , frame)
		image_data = tf.gfile.FastGFile("screens/" + str(i)+ "frame.jpg", 'rb').read()
		i = i + 1
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
		predictions = sess.run(softmax_tensor, \
				 {'DecodeJpeg/contents:0': image_data})		
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
		for node_id in top_k:
			human_string = label_lines[node_id]
			score = predictions[0][node_id]
			print('%s (score = %.5f)' % (human_string, score))
		print ("\n\n")
		#cv2.imshow("image", frame)
		cv2.waitKey(1)

  	video_p.release()
	#cv2.destroyAllWindows()
