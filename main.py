import os
import pyttsx3
import subprocess as sub
import speech_recognition as speech
import webbrowser
import requests, json
from datetime import datetime
import wolframalpha
import re
import random


def body():

	engine.say(greet())
	engine.runAndWait()

	while(True):
		r = speech.Recognizer()

		mic = speech.Microphone(device_index=1)

		f = open('log.txt', 'a')

		tmp_text = ''
		with mic as source:
		    print('[*] Speak anything...')
		    audio = r.listen(source)
		    try:
		    	tmp_text = r.recognize_google(audio)
		    	content = f.write(f"[+] {datetime.now()}  :  {tmp_text}\n")
		    except Exception as e:
		       pass


		text = str.lower(tmp_text.split(' ')[-1])

		engine.say(f'You said {text}.')
		engine.runAndWait()

		map_command = {
			'talk' : 100,
			'shutdown' : 0,											# this no is the process id assigned by us
			'powershell' : 1,
			'dialer' : 1,
			'dvdplay' : 1,
			'calculator' : 11,
			'edge' : 1,
			'bluetooth' : 1,
			'panel' : 1,
			'explorer' : 1,
			'prompt' : 1,
			'camera' : 1,
			'calendar' : 1,
			'notepad' : 1,
			'youtube' : 20,
			'google' : 30,
			'joke' : 26,
			'weather' : 27,
			'stop'  : 28,
			'find'	: 50,
		}

		try:
			try:
				choice = str(map_command[text])
			except Exception:
				choice = '10'

			if(choice == '0'):
				engine.say('Shutting the system down')
				engine.runAndWait()
				os.system("shutdown /s /t 1")

			if(choice == '1'):
				sub.Popen(text)

			if(choice == '11'):
				sub.Popen(['calc'])

			if(choice >= '10'):
				open_application(text)

			if(choice == '20'):
				engine.say("what shall i search")
				engine.runAndWait()
				tmp_text = ''
				with mic as source:
					print('[*] Speak anything...')
					audio = r.listen(source)
					try:
						tmp_text = r.recognize_google(audio)
						content = f.write(f'\t------[+] {tmp_text}\n')
						webbrowser.open(f'https://youtube.com/results?search_query={tmp_text}')
					except Exception:
						print("OOps exception, I hate it aaaggh...!")
					engine.say(f"searching {tmp_text}")
					engine.runAndWait()

			if(choice == '30'):
				engine.say("what shall i search")
				engine.runAndWait()
				tmp_text = ''
				with mic as source:
					print('[*] Speak anything...')
					audio = r.listen(source)
					try:
						tmp_text = r.recognize_google(audio)
						content = f.write(f'\t------[+] {tmp_text}\n')
						webbrowser.open(f'https://google.com/search?q={tmp_text}')
					except Exception:
						print("OOps exception, I hate it aaaggh...!")
					engine.say(f"searching {tmp_text}")
					engine.runAndWait()

			if(choice == '26'):
				engine.say(jokes())
				engine.runAndWait()

			if(choice == '27'):
				api_key = "c9771bc882017675a824ebe550759482"
				base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
				print("City name : ")
				city_name = ''
				with mic as source:
					print('[*] Speak anything...')
					audio = r.listen(source)
					try:
						city_name = r.recognize_google(audio)
						content = f.write(f"[+] {datetime.now()}  :  {tmp_text}\n")
					except Exception:
						pass
				complete_url = base_url + "appid =" + api_key + "&q =" + city_name
				response = requests.get(complete_url)
				x = response.json()

				if x["cod"] != "404":
					y = x["main"]
					current_temperature = y["temp"]
					current_pressure = y["pressure"]
					current_humidiy = y["humidity"]
					z = x["weather"]
					weather_description = z[0]["description"]
					print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))

				else:
					engine.say(" City Not Found ")

			if(choice == '28'):
				engine.say('Oooops you stooooped me... Anyways thank you.')
				engine.runAndWait()
				exit(0)

			if(choice == '100'):
				engine.say("Hey, the day is nice. How are you?")
				engine.runAndWait()
				while(True):
					question = ''
					with mic as source:
						print('[*] Speak anything...')
						audio = r.listen(source)
						try:
							question = r.recognize_google(audio)
							content = f.write(f'\t------[+] {tmp_text}\n')
							app_id = "U3AT8K-HA922U7HKX"
							client = wolframalpha.Client(app_id)
					  
							res = client.query(question)
							answer = next(res.results).text
					  
							print(answer)
							engine.say(answer)
							engine.runAndWait()
						except Exception as e:
							pass

			if(choice == '50'):
				print('\nThis is a beta feature. May not work properly...\n')
				prg = input('Enter file name: \n')
				pathtrav(prg)

		except Exception as e:
			engine.say(f'Cannot express your intentions in action...')
			engine.runAndWait()


def pathtrav(prg):

	for root, sub, files in os.walk('C:\\Program Files\\'):
		for each in files:
			if re.findall(prg, each):
				print("Found!!! {prg}")
				content = f.write(f"[+] {datetime.now()}  :  Found {each}\n")
				os.chdir(root)
				print(os.getcwd() + '/' + each)
	

def open_application(to_search):
    to_search = to_search+".exe"
    found = False

    if found == False:
        for root, sub, files in os.walk("C:\\Program Files\\"):
            for each in files:
                if(str.lower(each) == to_search):
                    os.chdir(root)
                    os.popen(each)
                    found = True
                    print("[+] Found!!!")
                    exit(0)
    if(not found):
        print("[-] Not found dear...")


def jokes():
	f = open('joke.txt', 'r')
	content = f.read()
	jokes = content.split('\n')
	to_say = random.choice(jokes)
	return to_say


def greet():
	return "Heeeyah... This is Ray. How may I be of any help?"


engine = pyttsx3.init()

engine.setProperty('voice', "english")
engine.setProperty('rate', 170)
engine.setProperty('volume', 1)

if __name__ == "__main__":
	body()