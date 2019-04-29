import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class InstaComents(object):
	"""InstaComents class
	Class created to login and coment multiple times to a instagram photo
	selenium and chromedriver is required

	selenium: pip install selenium
	chromedriver: http://chromedriver.chromium.org/downloads

	How to use:
	insta = InstaComents('C:\\your_path\\chromedrive.exe')
	insta.following()
	insta.go_coment(link_photo="photo_url", quantity_coments=3, quantity_user_for_coment=6, like_photo=False, follow_photo_user=False)
	"""

	def __init__(self, chromedriver_path: str, instagram_login_home_page='https://www.instagram.com/accounts/login/?source=auth_switcher'):
		# Open Chrome Drive
		self.driver = webdriver.Chrome(chromedriver_path)

		# Get Instagram Login Page
		self.driver.get(instagram_login_home_page)

		# Wait 1000s until login
		WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a/span')))

		# Awnser no in instagram notification
		try: 
			self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()

		except NoSuchElementException:
			pass

		finally:
			self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a/span').click()

	def following(self):
		# Wait following button
		WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span')))

		# Set the self.following (list with following users)
		setattr(self, 'following', self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'))
		self.following.click()
		self.following = int(self.following.text)  # Now self.following is the quantity of following. Instead of HTML element

		# Wait 60s for appear the following list
		WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/ul/div/li[1]')))

		# Append users to self.users_list
		setattr(self, 'users_list', list())  # set users_list as an attribute
		for c in range(1, self.following + 1):  # c(counter) to the amount of following
			try:
				# Try to take each following user
				line = self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/ul/div/li[{c}]')

			except NoSuchElementException:
				try:
					# Wait 60s for appear the next following user (sometimes, scrolling down is too fast that the element doesn't appear. So, wait)
					WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/div/div[2]/ul/div/li[{c}]')))

				except TimeoutException:
					break

				else:
					# After wait, take the element
					line = self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/ul/div/li[{c}]')

			except TimeoutException:
				break

			finally:
				# Scroll down <div>
				self.driver.execute_script("arguments[0].scrollIntoView();", line)
				try:
					self.users_list.append(line.text.split()[0])

				except IndexError:
					# Some users won't be abel to take. 
					pass

	def go_coment(self, link_photo, quantity_coments, quantity_user_for_coment, like_photo=False, follow_photo_user=False):
		# Get link_photo
		self.driver.get(str(link_photo))

		# Wait 15s for load the page
		WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button/span')))

		# if like_photo
		if bool(like_photo):
			like_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button/span')
			if like_button.get_attribute('aria-label').lower() == 'like' or like_button.get_attribute('aria-label').lower() == 'curtir':
				like_button.click()

		# if follow_photo_user
		if bool(follow_photo_user):
			try:
				self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[2]/button').click()
				time.sleep(1)
				self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
			except NoSuchElementException:
				pass

		# Comenta
		random.shuffle(self.users_list)
		for c in range(quantity_coments):
			try:
				self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea').click()

			except:
				self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea').click()

			finally:
				coment_field = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
				coment_field.click()

			coment_field.send_keys(f'@{" @".join(random.choices(self.users_list, k=quantity_user_for_coment))}')
			coment_field.send_keys(Keys.ENTER)
			time.sleep(3)
