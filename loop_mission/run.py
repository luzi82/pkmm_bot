import subprocess
import PIL.Image
import io
import os
import numpy
import time
import argparse
import datetime
import sys

ADB = '/home/luzi82/Android/Sdk/platform-tools/adb'

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("battle_select_2", type=int)
	arg = parser.parse_args()

	image_type_to_data_dict = {}

	image_sample_list_list = os.listdir('image_sample_list_list')
	for image_sample_list_name in image_sample_list_list:
		image_sample_list = []
		image_sample_list_path = os.path.join('image_sample_list_list',image_sample_list_name)
		image_sample_name_list = os.listdir(image_sample_list_path)
		for image_sample_name in image_sample_name_list:
			image_sample_path = os.path.join(image_sample_list_path,image_sample_name)
			image_sample = PIL.Image.open(image_sample_path)
			image_sample = image_sample.convert('RGB')
			image_sample = numpy.array(image_sample)
			image_sample_list.append(image_sample)
		image_sample_list = numpy.array(image_sample_list)
		
		image_data = numpy.transpose(image_sample_list, (1,2,3,0))

		image_min = numpy.min(image_data, axis=3).astype(int)
		#print(image_min.shape)
		image_max = numpy.max(image_data, axis=3).astype(int)
		#print(image_max.shape)
		#print(image_data.shape)
		image_type_to_data_dict[image_sample_list_name] = {
			'min': image_min,
			'max': image_max,
		}
		
		image_sample_list = None
		image_data = None

	fail_count = 0
	while True:
		print('HBRBLHOVFW datetime={datetime} fail_count={fail_count}'.format(datetime=datetime.datetime.now(),fail_count=fail_count))
		if fail_count >= 10:
			break
		try:
			print('ITOFBVBERF')
			process = subprocess.Popen([ADB,'exec-out','screencap','-p'], stdout=subprocess.PIPE)
			stdout, stderr = process.communicate(timeout=10)
			print('VRTYSJJQRZ')
			bytes_in = io.BytesIO(stdout)
			img = PIL.Image.open(bytes_in)
			img = img.convert('RGB')
			img = img.resize((90,160),PIL.Image.BILINEAR)
			#print(img.size)
			img = numpy.array(img).astype(int)
			#print('img')
			#print(img)
			
			fail_count = 0
			
			image_type_to_diff_dict = {}
			for image_type, image_type_data in image_type_to_data_dict.items():
				#print(image_type)
				image_min = image_type_data['min']
				image_max = image_type_data['max']
				#print('image_min')
				#print(image_min)
				diff_min = image_min - img
				diff_max = img - image_max
				#print('diff_min')
				#print(diff_min)
				diff = numpy.maximum(diff_min, diff_max)
				diff = numpy.maximum(diff, 0)
				#print(diff.shape)
				diff = numpy.average(diff)
				image_type_to_diff_dict[image_type] = diff
	
			min_diff = min(image_type_to_diff_dict.values())
			if min_diff > 10:
				print('None {0}'.format(min_diff))
				continue
	
			#print(list(image_type_to_diff_dict.items()))
			image_type = filter(lambda i:i[1]==min_diff, image_type_to_diff_dict.items())
			image_type = list(image_type)[0][0]
			print(image_type)
			
			xy = None
			
			if image_type == 'battle_select_2':
				if arg.battle_select_2 == 0:
					xy = (720,700) # very hard
				elif arg.battle_select_2 == 1:
					xy = (720,1150) # hard
				elif arg.battle_select_2 == 2:
					xy = (720,1600) # normal
			elif image_type == 'battle_pre':
				xy = (720,2450)
			elif image_type == 'battle_end_0_level_up':
				xy = (720,1280)
			elif image_type == 'battle_end_1':
				xy = (720,1280)
			elif image_type == 'battle_end_2':
				xy = (720,2450)
			
			subprocess.Popen([ADB,'shell','input','tap',str(xy[0]),str(xy[1])], stdout=subprocess.PIPE).communicate(timeout=10)
			
			time.sleep(5)
		except KeyboardInterrupt as e:
			break
		except:
			print(sys.exc_info()[0])
			fail_count += 1
