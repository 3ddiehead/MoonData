import datetime
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#CREATE FASTER SEARCH ALGORITHM DEPENDING ON LATITUDE + THE ~±28° RANGE OF THE MOON + THE ROUGH LENGTH OF TIME BETWEEN CROSSES DEPENDING ON ALTITUDE.
#IN COSTA RICA AT 9.9°/-85.5°, IT IS ROUGHLY 17 DAYS BELOW and 11 DAYS ABOVE

#DISPLAY WHETHER THE MOON IS CROSSING OVER N->S or S->N FOR ~±28° LATITUDE REGIONS

#ADD OPTIONS FOR LOCATION OF THE HIGHEST ALTITUDE BY DATE AND TIME / CURRENT

#COLLECT INFORMATION ON THE SPEED OF ALTITUDE RISING AND LOWERING

file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)

#Begin an instance of Chrome without a visible window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

#Set the default to the day before the current date and time
dt = datetime.datetime.now() + datetime.timedelta(days=-1)

#Collect variables from user
longitude = input("What is the longitude of the location in decimal? ")
latitude = input("What is the latitude of the location? ")
peaks = int(input("How many peaks would you like to read in advance? "))

#Times, altitudes, and illumination percentage of closest approaches by the moon
TAIs = []

#Variables to store the TAI from the the current and previous url query
is_rising = False
this_TAI = ['NA','NA','NA']
last_TAI = ['NA','NA','NA']

#Loop until 10 culmination dates are found
while len(TAIs) < peaks:
	
	#Generate the URL for mooncalc.org with latitude, longitude, day, and time
	dtlist = dt.strftime("%Y-%m-%d-%H-%M").split("-")
	dtstr = f"{dtlist[0]}.{dtlist[1]}.{dtlist[2]}/{dtlist[3]}:{dtlist[4]}"
	url = f"https://mooncalc.org/#/{latitude},{longitude},10/{dtstr}/1/0"

	#Pull webpage data
	driver.get(url)

	#Function to check if times have loaded into the culmination element
	def values_loaded(driver):
		try:
			element_text = driver.find_element(By.ID, "clickSunpeak").text
			return (":" in element_text) or ("undef" in element_text)
		except (NoSuchElementException, StaleElementReferenceException):
			return False

	#Use WebDriverWait to wait for values to appear in the elements
	WebDriverWait(driver, 10).until(values_loaded)

	#Get page source
	page_content = driver.page_source

	#Soupify
	soup = BeautifulSoup(page_content, 'html.parser')

	#Get text data from specific webpage elements
	culminTime = soup.find(attrs={"id":"clickSunpeak"}).text
	altitude = soup.find(attrs={"id":"sunhoehe"}).text
	distance_E2M = soup.find(attrs={"id":"time-span twilight dawn-time"})
	illumination = soup.find(attrs={"title":"Identification of the Moon Phase / Visibility (Illumination)"})

	#Fix the culmination time in the URL so that the highest altitude for a day is checked
	if culminTime == "undef":
		delta = datetime.timedelta(days=1)
		dt = dt + delta
		continue
	elif culminTime[0:5] != dt.strftime("%H:%M"):
		HM = culminTime.split(":")
		print(HM)
		dt = dt.replace(hour=int(HM[0]), minute=int(HM[1]))
		continue

	this_TAI = [dt,altitude]

	#Set the last_TAI in the first round when there's nothing to be compared yet
	if last_TAI[0] == "NA":
		last_TAI = this_TAI
		continue

	if float(this_TAI[1][:-1]) > float(last_TAI[1][:-1]):
		is_rising = True
	else:
		if is_rising:
			TAIs.append(last_TAI)
		is_rising = False

	last_TAI = this_TAI
	delta = datetime.timedelta(days=1)
	dt = dt + delta

driver.close()

for item in TAIs:
	print(item[0].strftime("%Y.%m.%d at %H:%M,"), "Alt:", item[1])