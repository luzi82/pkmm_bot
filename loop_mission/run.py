import subprocess
import PIL.Image
import io
import os
import os.path
import numpy
import time
import argparse
import datetime
import sys
import random
import traceback
import re

#ADB = '/home/luzi82/Android/Sdk/platform-tools/adb'
#ADB = '/Users/jenkins/Library/Android/sdk/platform-tools/adb'

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("adb", type=str)
	parser.add_argument("tcpip_addr", type=str)
	parser.add_argument("solo_multi", type=str)
	parser.add_argument("battle_select_0", type=str)
	parser.add_argument("battle_select_1", type=str)
	parser.add_argument("battle_select_2", type=str)
	arg = parser.parse_args()

	image_type_to_data_dict = {}

	image_sample_list_list = os.listdir('image_sample_list_list')
	for image_sample_list_name in image_sample_list_list:
		image_sample_list = []
		image_sample_list_path = os.path.join('image_sample_list_list',image_sample_list_name)
		if not os.path.isdir(image_sample_list_path): continue
		image_sample_name_list = os.listdir(image_sample_list_path)
		for image_sample_name in image_sample_name_list:
			if not image_sample_name.endswith('.png'): continue
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

	last_act_time = time.time()
	fail_count = 0
	while True:
		print('HBRBLHOVFW datetime={datetime} fail_count={fail_count}'.format(datetime=datetime.datetime.now(),fail_count=fail_count))
		now_act_time = time.time()
		if fail_count >= 10:
			break
		try:
			print('ITOFBVBERF')
			process = subprocess.Popen([arg.adb,'-s',arg.tcpip_addr,'exec-out','screencap','-p'], stdout=subprocess.PIPE)
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
				if now_act_time - last_act_time > 600:
					print('OAAYAXQPPX kill app')
					subprocess.Popen([arg.adb,'shell','am','force-stop','com.dena.a12026418'], stdout=subprocess.PIPE).communicate(timeout=10)
					time.sleep(10)
					print('VUIQGQOKBL start app')
					subprocess.Popen([arg.adb,'shell','am','start','-n','com.dena.a12026418/com.dena.kenya.Kenya'], stdout=subprocess.PIPE).communicate(timeout=10)
					last_act_time = now_act_time
				continue
	
			#print(list(image_type_to_diff_dict.items()))
			image_type = filter(lambda i:i[1]==min_diff, image_type_to_diff_dict.items())
			image_type = list(image_type)[0][0]
			print(image_type)
			
			image_type = image_type.split('.')
			image_type = image_type[0]
			
			xy = None
			
			if image_type == 'battle_select_solo_0' or image_type == 'battle_select_multi_0':
				if image_type == 'battle_select_solo_0' and arg.solo_multi == 'm':
					xy = (1080,320)
				elif image_type == 'battle_select_multi_0' and arg.solo_multi == 's':
					xy = (360,320)
				elif arg.battle_select_0 == '0':
					xy = (720,650)
				elif arg.battle_select_0 == '1':
					xy = (720,950)
				elif arg.battle_select_0 == '2':
					xy = (720,1250)
				elif arg.battle_select_0 == '3':
					xy = (720,1550)
			elif image_type == 'battle_select_solo_1' or image_type == 'battle_select_multi_1':
				if arg.battle_select_1 == '0':
					xy = (720,700)
				elif arg.battle_select_1 == '1':
					xy = (720,1100)
				elif arg.battle_select_1 == '2':
					xy = (720,1500)
				elif arg.battle_select_1 == '3':
					xy = (720,1900)
				else:
					bs1s = arg.battle_select_1.split(',')
					xy = []
					while len(bs1s)>2:
						xy.append('u')
						bs1s.pop(0)
					xy.append(int(bs1s[0]))
					xy.append(int(bs1s[1]))
			elif image_type == 'battle_select_multi_1c':
				if arg.battle_select_1 == '0':
					xy = (720,440)
				elif arg.battle_select_1 == '1':
					xy = (720,840)
				elif arg.battle_select_1 == '2':
					xy = (720,1240)
				elif arg.battle_select_1 == '3':
					xy = (720,1640)
			elif image_type == 'battle_select_solo_2' or image_type == 'battle_select_multi_2':
				if arg.battle_select_2 == '0':
					xy = (720,700) # very hard
				elif arg.battle_select_2 == '1':
					xy = (720,1150) # hard
				elif arg.battle_select_2 == '2':
					xy = (720,1600) # normal
				else:
					g = re.fullmatch('(\\d+),(\\d+)',arg.battle_select_2)
					x = int(g.group(1))
					y = int(g.group(2))
					xy = (x,y)
			elif image_type == 'battle_select_multi_2_high':
				if arg.battle_select_2 == '0':
					xy = (720,500) # very hard
				elif arg.battle_select_2 == '1':
					xy = (720,950) # hard
				elif arg.battle_select_2 == '2':
					xy = (720,1400) # normal
			elif image_type == 'battle_select_multi_2x':
				if arg.battle_select_2 == '0':
					xy = (720,1000) # very hard
				elif arg.battle_select_2 == '1':
					xy = (720,1450) # hard
				elif arg.battle_select_2 == '2':
					xy = (720,1900) # normal
			elif image_type == 'battle_select_multii_2':
				if arg.battle_select_2 == '0':
					xy = (720,500) # very hard
				elif arg.battle_select_2 == '1':
					xy = (720,950) # hard
				elif arg.battle_select_2 == '2':
					xy = (720,1400) # normal
			elif image_type == 'battle_select_multi_3':
				xy = (360,1280)
			elif image_type == 'battle_pre':
				xy = (720,2450)
			elif image_type == 'battle_end_0_level_up':
				xy = (720,1280)
			elif image_type == 'battle_end_1':
				xy = (720,1280)
			elif image_type == 'battle_end_2':
				xy = (720,2450)
			elif image_type == 'battle_end_2r':
				xy = (1080,2450)
			elif image_type == 'battle_end_3':
				xy = (720,2450)
			elif image_type == 'battle_end_3r':
				xy = (1080,2450)
			elif image_type == 'battle_bad_network':
				xy = (1000,1700)
			elif image_type == 'error':
				xy = (720,2000)
			elif image_type == 'error_entry':
				xy = (720,1700)
			elif image_type == 'error_entry_ny':
				xy = (540,1700) # no when no group
				#xy = (900,1700) # yes when no group
			elif image_type == 'title':
				xy = (720,1280)
			elif image_type == 'menu':
				xy = (720,2450)
			elif image_type == 'news':
				xy = (1330,2330)
			elif image_type == 'new_mission':
				xy = (720,2000)
			
			while len(xy)>2:
				subprocess.Popen([arg.adb,'-s',arg.tcpip_addr,'shell','input','swipe','720','2200','720','200'], stdout=subprocess.PIPE).communicate(timeout=10)
				time.sleep(1)
				xy.pop(0)
			xy = tuple(i+random.randint(-5,5) for i in xy)
			subprocess.Popen([arg.adb,'-s',arg.tcpip_addr,'shell','input','tap',str(xy[0]),str(xy[1])], stdout=subprocess.PIPE).communicate(timeout=10)
			
			last_act_time = now_act_time
			
			time.sleep(4)
		except KeyboardInterrupt as e:
			break
		except OSError as e:
			print(sys.exc_info()[0])
			traceback.print_exception(*sys.exc_info())
			try:
				subprocess.Popen([arg.adb,'disconnect'], stdout=subprocess.PIPE).communicate(timeout=10)
				time.sleep(1)
				subprocess.Popen([arg.adb,'connect',arg.tcpip_addr], stdout=subprocess.PIPE).communicate(timeout=10)
			except:
				pass
			time.sleep(10)
			fail_count += 1
		except:
			print(sys.exc_info()[0])
			traceback.print_exception(*sys.exc_info())
			time.sleep(10)
			fail_count += 1
