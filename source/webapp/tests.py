from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from selenium.webdriver import Chrome
from time import sleep


class LoginTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_login_as_admin(self):
        self.driver.get('http://localhost:8000/login/')
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin2')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/'

    def test_login_error(self):
        self.driver.get('http://localhost:8000/login/')
        self.driver.find_element_by_name('username').send_keys('this-is-no-admin')
        self.driver.find_element_by_name('password').send_keys('this-is-no-admin')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/login/'
        error = self.driver.find_element_by_css_selector('.text-danger')
        assert error.text == "Неверное имя пользователя или пароль."


class RegistrationTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_registration(self):
        self.driver.get('http://localhost:8000/')
        self.driver.find_element_by_css_selector('#create-user').click()
        sleep(1)
        self.driver.find_element_by_name('username').send_keys('new_user')
        self.driver.find_element_by_name('password').send_keys('new_user77')
        self.driver.find_element_by_name('password_confirm').send_keys('new_user77')
        self.driver.find_element_by_css_selector('#register').click()
        sleep(1)
        assert self.driver.current_url == 'http://localhost:8000/login/'
        self.driver.find_element_by_name('username').send_keys('new_user')
        self.driver.find_element_by_name('password').send_keys('new_user77')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/'

    def test_registration_error(self):
        self.driver.get('http://localhost:8000/')
        self.driver.find_element_by_css_selector('#create-user').click()
        sleep(1)
        self.driver.find_element_by_name('username').send_keys('new_user')
        self.driver.find_element_by_css_selector('#register').click()
        sleep(1)
        error = self.driver.find_element_by_css_selector('.id_username')
        assert error.text == "Пользователь с таким именем уже существует."
        self.driver.find_element_by_name('password').send_keys('new')
        self.driver.find_element_by_css_selector('#register').click()
        sleep(1)
        error = self.driver.find_element_by_css_selector('.id_password')
        assert error.text == 'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.'
        self.driver.find_element_by_name('password').send_keys('new_user77')
        self.driver.find_element_by_name('password_confirm').send_keys('new_user')
        self.driver.find_element_by_css_selector('#register').click()
        sleep(1)
        error = self.driver.find_element_by_css_selector('.id_password_confirm')
        assert error.text == 'Пароли не совпадают!'


class UserChangePasswordTest(TestCase):
    def setUp(self):
        self.driver = Chrome()

    def tearDown(self):
        self.driver.close()

    def test_user_change_password(self):
        self.driver.get('http://localhost:8000/login/')
        self.driver.find_element_by_name('username').send_keys('new_user')
        self.driver.find_element_by_name('password').send_keys('new_user77')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/'
        sleep(1)
        self.driver.find_element_by_css_selector('#detail-user').click()
        self.driver.find_element_by_css_selector('#user-change').click()
        sleep(1)
        self.driver.find_element_by_css_selector('#id_password').send_keys('test-test')
        self.driver.find_element_by_css_selector('#id_password_confirm').send_keys('test-test')
        self.driver.find_element_by_css_selector('#id_old_password').send_keys('new_user77')
        self.driver.find_element_by_css_selector('#change').click()
        sleep(1)
        assert self.driver.current_url == 'http://localhost:8000/login/'
        self.driver.find_element_by_name('username').send_keys('new_user')
        self.driver.find_element_by_name('password').send_keys('test-test')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/'

    def test_user_change_password_error(self):
        self.driver.get('http://localhost:8000/login/')
        self.driver.find_element_by_name('username').send_keys('new_user')
        self.driver.find_element_by_name('password').send_keys('test-test')
        self.driver.find_element_by_css_selector('button[type="submit"]').click()
        assert self.driver.current_url == 'http://localhost:8000/'
        sleep(1)
        self.driver.find_element_by_css_selector('#detail-user').click()
        self.driver.find_element_by_css_selector('#user-change').click()
        sleep(1)
        self.driver.find_element_by_css_selector('#id_password').send_keys('test')
        self.driver.find_element_by_css_selector('#id_password_confirm').send_keys('tes')
        self.driver.find_element_by_css_selector('#id_old_password').send_keys('test-test')
        self.driver.find_element_by_css_selector('#change').click()
        sleep(1)
        error = self.driver.find_element_by_css_selector('#error_id_password_confirm')
        assert error.text == 'Пароли не совпадают!'
        self.driver.find_element_by_css_selector('#id_password').send_keys('test')
        self.driver.find_element_by_css_selector('#id_password_confirm').send_keys('test')
        self.driver.find_element_by_css_selector('#id_old_password').send_keys('test-test')
        self.driver.find_element_by_css_selector('#change').click()
        error = self.driver.find_element_by_css_selector('#error_id_password')
        assert error.text == 'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.'




