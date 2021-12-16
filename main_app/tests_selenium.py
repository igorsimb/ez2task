import os

from django.test import TestCase
import pytest
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
load_dotenv()

class TestDemoUserFunctionality(StaticLiveServerTestCase):

    # setUp and tearDown methods to open/close Chrome for each individual test (slower)

    # def setUp(self):
    #     # change these to test different users
    #     login_keys = 'demo@user.com'
    #     # login_keys = 'my@gmail.com'
    #     password_keys = 'testing321'
    #
    #     self.browser = webdriver.Chrome('chromedriver.exe')
    #     self.browser.get('http://localhost:8000')
    #     login = self.browser.find_element(By.NAME, 'username')
    #     password = self.browser.find_element(By.NAME, 'password')
    #     submit = self.browser.find_element(By.ID, 'login_button')
    #     login.send_keys(login_keys)
    #     password.send_keys(password_keys)
    #     submit.click()
    #
    # def tearDown(self):
    #     self.browser.quit()

    # setUpClass and tearDownClass classes to open Chrome once and run all tests (faster)
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

        # change these to test different users
        login_keys = str(os.getenv('LOGIN_DEMO_KEYS'))
        password_keys = str(os.getenv('PASSWORD_DEMO_KEYS'))

        # cls.browser = webdriver.Chrome('chromedriver.exe')
        cls.browser.get('http://localhost:8000')
        login = cls.browser.find_element(By.NAME, 'username')
        password = cls.browser.find_element(By.NAME, 'password')
        submit = cls.browser.find_element(By.ID, 'login_button')
        # login.send_keys(login_keys)
        # password.send_keys(password_keys)

        for letter in login_keys:
            login.send_keys(letter)
            sleep(0.1)

        for letter in password_keys:
            password.send_keys(letter)
            sleep(0.05)

        submit.click()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        super().tearDownClass()

    def test_main_page_demo_user_alert(self):
        print('***"Demo accounts" notification...***')
        sleep(1)
        self.assertIn('(demo accounts have limited functionality)', self.browser.page_source)

    def test_task_create_button_is_disabled(self):
        self.browser.get('http://localhost:8000/create/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'task_create_button').is_enabled()
        print('***Task Create button disabled test...***')
        self.assertFalse(button)

    def test_user_create_button_is_disabled(self):
        self.browser.get('http://localhost:8000/user-create/')
        sleep(4)
        button = self.browser.find_element_by_id('user_create_button').is_enabled()
        print('***User Create button disabled test...***')
        self.assertFalse(button)

    def test_project_create_button_is_disabled(self):
        self.browser.get('http://localhost:8000/category/create/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'category_create_button').is_enabled()
        print('***Category Create button disabled test...***')
        self.assertFalse(button)

    def test_user_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000')
        self.browser.find_element_by_id('user_name_link').click()
        sleep(1)
        self.browser.find_element_by_id('user_settings_link').click()
        sleep(1)
        button = self.browser.find_element_by_id('user_update_submit_button').is_enabled()
        print('***User Update button disabled test...***')
        self.assertFalse(button)

    def test_user_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000')
        self.browser.find_element(By.ID, 'user_name_link').click()
        sleep(1)
        self.browser.find_element(By.ID, 'user_settings_link').click()
        sleep(1)
        self.browser.find_element(By.ID, 'update_company_info_link').click()
        sleep(3)
        button = self.browser.find_element(By.ID, 'company_update_submit_button').is_enabled()
        print('***Company Update button disabled test...***')
        self.assertFalse(button)

    def test_password_reset_button_is_disabled(self):
        self.browser.get('http://localhost:8000/password-reset/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'password_reset_submit_button').is_enabled()
        print('***Category Create button disabled test...***')
        self.assertFalse(button)

    def test_comment_button_is_disabled(self):
        self.browser.get('http://localhost:8000/detail/3/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'comment_submit_button').is_enabled()
        print('***Comment button disabled test...***')
        self.assertFalse(button)

    def test_task_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000/password-reset/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'password_reset_submit_button').is_enabled()
        print('***Category Create button disabled test...***')
        self.assertFalse(button)

    def test_task_delete_button_is_disabled(self):
        self.browser.get('http://localhost:8000/detail/3/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'task_delete_submit_button').is_enabled()
        print('***Task Delete button disabled test...***')
        self.assertIn('btn btn-sm btn-danger mt-3 disabled', self.browser.page_source)

    def test_task_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000/detail/3/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'task_update_submit_button').is_enabled()
        print('***Task Update button disabled test...***')
        self.assertFalse(button)

    def test_user_delete_button_is_disabled(self):
        self.browser.get('http://localhost:8000/manage_users/')
        sleep(1)
        print('***User Delete button disabled test...***')
        self.assertIn("m-0 p-0 btn d-inline disabled", self.browser.page_source)

    def test_category_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000/category/update/1/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'category_update_submit_button').is_enabled()
        print('***Category Update button disabled test...***')
        self.assertFalse(button)

    def test_category_delete_button_is_disabled(self):
        self.browser.get('http://localhost:8000/category/update/1/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'category_delete_submit_button').is_enabled()
        print('***Category Delete button disabled test...***')
        self.assertIn('btn btn-danger mt-2 disabled">Delete Project</a>', self.browser.page_source)


class TestNonDemoUserFunctionality(StaticLiveServerTestCase):

    # setUp and tearDown methods to open/close Chrome for each individual test (slower)

    # def setUp(self):
    #     # change these to test different users
    #     login_keys = 'demo@user.com'
    #     # login_keys = 'my@gmail.com'
    #     password_keys = 'testing321'
    #
    #     self.browser = webdriver.Chrome('chromedriver.exe')
    #     self.browser.get('http://localhost:8000')
    #     login = self.browser.find_element(By.NAME, 'username')
    #     password = self.browser.find_element(By.NAME, 'password')
    #     submit = self.browser.find_element(By.ID, 'login_button')
    #     login.send_keys(login_keys)
    #     password.send_keys(password_keys)
    #     submit.click()
    #
    # def tearDown(self):
    #     self.browser.quit()

    # setUpClass and tearDownClass classes to open Chrome once and run all tests (faster)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

        # change these to test different users
        # login_keys = 'demo@user.com'
        # login_keys = 'my@gmail.com'
        # password_keys = 'testing321'

        # change these to test different users
        login_keys = str(os.getenv('LOGIN_NON_DEMO_KEYS'))
        password_keys = str(os.getenv('PASSWORD_NON_DEMO_KEYS'))

        # cls.browser = webdriver.Chrome('chromedriver.exe')
        cls.browser.get('http://localhost:8000')
        login = cls.browser.find_element(By.NAME, 'username')
        password = cls.browser.find_element(By.NAME, 'password')
        submit = cls.browser.find_element(By.ID, 'login_button')
        # login.send_keys(login_keys)
        # password.send_keys(password_keys)

        for letter in login_keys:
            login.send_keys(letter)
            sleep(0.1)

        for letter in password_keys:
            password.send_keys(letter)
            sleep(0.05)

        submit.click()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        super().tearDownClass()

    def test_main_page_demo_user_alert(self):
        print('***"Demo accounts" notification...***')
        sleep(1)
        self.assertNotIn('(demo accounts have limited functionality)', self.browser.page_source)

    def test_task_create_button_is_disabled(self):
        self.browser.get('http://localhost:8000/create/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'task_create_button').is_enabled()
        print('***Task Create button disabled test...***')
        self.assertTrue(button)

    def test_user_create_button_is_disabled(self):
        self.browser.get('http://localhost:8000/user-create/')
        sleep(4)
        button = self.browser.find_element_by_id('user_create_button').is_enabled()
        print('***User Create button disabled test...***')
        self.assertTrue(button)

    def test_project_create_button_is_disabled(self):
        self.browser.get('http://localhost:8000/category/create/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'category_create_button').is_enabled()
        print('***Category Create button disabled test...***')
        self.assertTrue(button)

    def test_user_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000')
        self.browser.find_element_by_id('user_name_link').click()
        sleep(1)
        self.browser.find_element_by_id('user_settings_link').click()
        sleep(1)
        button = self.browser.find_element_by_id('user_update_submit_button').is_enabled()
        print('***User Update button disabled test...***')
        self.assertTrue(button)

    def test_user_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000')
        self.browser.find_element(By.ID, 'user_name_link').click()
        sleep(1)
        self.browser.find_element(By.ID, 'user_settings_link').click()
        sleep(1)
        self.browser.find_element(By.ID, 'update_company_info_link').click()
        sleep(3)
        button = self.browser.find_element(By.ID, 'company_update_submit_button').is_enabled()
        print('***Company Update button disabled test...***')
        self.assertTrue(button)

    def test_password_reset_button_is_disabled(self):
        self.browser.get('http://localhost:8000/password-reset/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'password_reset_submit_button').is_enabled()
        print('***Category Create button disabled test...***')
        self.assertTrue(button)

    def test_comment_button_is_disabled(self):
        self.browser.get('http://localhost:8000/detail/3/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'comment_submit_button').is_enabled()
        print('***Comment button disabled test...***')
        self.assertTrue(button)

    def test_task_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000/password-reset/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'password_reset_submit_button').is_enabled()
        print('***Category Create button disabled test...***')
        self.assertTrue(button)

    def test_task_delete_button_is_disabled(self):
        self.browser.get('http://localhost:8000/detail/3/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'task_delete_submit_button').is_enabled()
        print('***Task Delete button disabled test...***')
        self.assertNotIn('btn btn-sm btn-danger mt-3 disabled', self.browser.page_source)

    def test_task_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000/detail/3/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'task_update_submit_button').is_enabled()
        print('***Task Update button disabled test...***')
        self.assertTrue(button)

    def test_user_delete_button_is_disabled(self):
        self.browser.get('http://localhost:8000/manage_users/')
        sleep(1)
        print('***User Delete button disabled test...***')
        self.assertNotIn("m-0 p-0 btn d-inline disabled", self.browser.page_source)

    def test_category_update_button_is_disabled(self):
        self.browser.get('http://localhost:8000/category/update/1/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'category_update_submit_button').is_enabled()
        print('***Category Update button disabled test...***')
        self.assertTrue(button)

    def test_category_delete_button_is_disabled(self):
        self.browser.get('http://localhost:8000/category/update/1/')
        sleep(1)
        button = self.browser.find_element(By.ID, 'category_delete_submit_button').is_enabled()
        print('***Category Delete button disabled test...***')
        self.assertNotIn('btn btn-danger mt-2 disabled">Delete Project</a>', self.browser.page_source)
