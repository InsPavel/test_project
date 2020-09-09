from django.core.paginator import Paginator
from django.test import TestCase
from webapp.forms import CategoryForm
from webapp.models import Article, Category


class LoginTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def test_login(self):
        response = self.client.login(username='admin', password='admin')
        self.assertEqual(response, True)

    def test_login_error(self):
        response = self.client.login(username='no-admin', password='no-admin')
        self.assertEqual(response, False)


class RegistrationTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def setUp(self):
        self.data = {
            'username': 'test_new_user',
            'password': 'new_user_password',
            'password_confirm': 'new_user_password',
        }

    def test_registration(self):
        self.create_user()
        response = self.client.login(username=self.data['username'], password=self.data['password'])
        self.assertEqual(response, True)

    def test_registration_error(self):
        self.create_user()
        self.check_url('error', '/accounts/create/user/', '/accounts/login/')

    def test_password_validation(self):
        self.data['password'] = 'test'
        response = self.client.post('/accounts/create/user/', data=self.data)
        form = response.context['form']
        self.assertEqual(form.errors['password'][0], 'Введённый пароль слишком короткий.'
                                                     ' Он должен содержать как минимум 8 символов.')

    def test_password_confirm_validation(self):
        self.data['password_confirm'] = 'test'
        response = self.client.post('/accounts/create/user/', data=self.data)
        form = response.context['form']
        self.assertEqual(form.errors['password_confirm'][0], 'Пароли не совпадают!')

    def create_user(self):
        self.check_url('success', '/accounts/create/user/', '/accounts/login/')

    def check_url(self, status, url, redirect_url):
        response = self.client.post(url, data=self.data)
        if status == 'error':
            self.assertEqual(response.status_code, 200)
        elif status == 'success':
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, redirect_url)


class UserDetailTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_pagination_first_page(self):
        response = self.client.get('/accounts/user/1/')
        page = response.context['page_obj']
        self.assertEqual("<Page 1 of 4>", str(page))
        self.assertEqual(len(page.object_list), 10)

    def test_pagination_last_page(self):
        response = self.client.get('/accounts/user/1/?page=4')
        page = response.context['page_obj']
        self.assertFalse(page.has_next())
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_other_pages())

    def test_page_not_an_integer(self):
        response = self.client.get('/accounts/user/1/?page=None')
        page = response.context['page_obj']
        self.assertEqual("<Page 1 of 4>", str(page))

    def test_page_empty(self):
        response = self.client.get('/accounts/user/1/?page=44')
        page = response.context['page_obj']
        self.assertEqual("<Page 4 of 4>", str(page))


class UserChangePasswordTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def setUp(self):
        self.client.login(username='test_user', password='test_user')
        self.data = {
            'password': 'test_new_password',
            'password_confirm': 'test_new_password',
            'old_password': 'test_user'
        }
        self.password_message = 'Введённый пароль слишком короткий.' ' Он должен содержать как минимум 8 символов.'
        self.password_confirm_message = 'Пароли не совпадают!'
        self.old_password_message = 'Старый пароль неправильный!'

    def test_change_password(self):
        self.check_url('/accounts/user/2/password_change/', '/accounts/login/')
        response = self.client.login(username='test_user', password=self.data['password'])
        self.assertEqual(response, True)

    def test_change_password_error(self):
        self.data['password_confirm'] = 'test'
        response = self.client.post('/accounts/user/2/password_change/', data=self.data)
        self.assertEqual(response.status_code, 200)

    def test_password_validation(self):
        self.field_validation('password', self.password_message)

    def test_password_confirm_validation(self):
        self.field_validation('password_confirm', self.password_confirm_message)

    def test_old_password_validation(self):
        self.field_validation('old_password', self.old_password_message)

    def field_validation(self, field, message):
        self.data[field] = 'test'
        response = self.client.post('/accounts/user/2/password_change/', data=self.data)
        form = response.context['form']
        self.assertEqual(form.errors[field][0], message)

    def check_url(self, url, redirect_url):
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_url)


class UserPermissionTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def setUp(self):
        self.client.login(username='test_user', password='test_user')

    def test_get_page(self):
        self.client.logout()
        self.check_url('/', '/accounts/login/?next=/')
        self.check_url('/article/create/', '/accounts/login/?next=/article/create/')
        self.check_url('/categories/', '/accounts/login/?next=/categories/')
        self.check_url('/category/create/', '/accounts/login/?next=/category/create/')

    def test_user_no_perm_update(self):
        response = self.client.get('/article/update/1/')
        self.assertEqual(response.status_code, 403)

    def test_user_no_perm_delete(self):
        response = self.client.get('/article/delete/1/')
        self.assertEqual(response.status_code, 403)

    def test_user_has_perm_update(self):
        response = self.client.get('/article/update/5/')
        self.assertEqual(response.status_code, 200)

    def test_user_has_perm_update_admin(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/article/update/2/')
        self.assertEqual(response.status_code, 200)

    def test_user_has_perm_delete(self):
        response = self.client.get('/article/delete/5/')
        self.assertEqual(response.status_code, 200)

    def test_user_has_perm_delete_admin(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/article/delete/2/')
        self.assertEqual(response.status_code, 200)

    def check_url(self, url, redirect_url):
        response = self.client.get(url)
        self.assertEqual(response.url, redirect_url)


class ArticleCRUDTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def setUp(self):
        self.client.login(username='test_user', password='test_user')
        self.data = {
            'category_id': 2,
            'title': 'Test Article',
            'user_id': 2,
            'description': 'Test Article Description'
        }

    def test_article(self):
        self.add_article()
        self.update_article()
        self.delete_article()

    def test_article_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_article_view(self):
        response = self.client.get('/article/2/')
        self.assertEqual(response.status_code, 200)

    def test_article_crud_error(self):
        self.add_article_error()
        self.update_article_error()

    def add_article(self):
        response = self.client.post('/article/create/', data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/article/41/')

    def update_article(self):
        self.data['category_id'] = 1
        self.data['title'] = 'Test Article Update'
        self.data['description'] = 'Test Article Description Update'
        self.client.post('/article/update/41/', data=self.data)
        article = Article.objects.filter(title=self.data['title'], category_id=self.data['category_id'])
        self.assertEqual(len(article), 1)

    def delete_article(self):
        self.check_method('/article/delete/41/', 'DEL')

    def add_article_error(self):
        self.data['title'] = ''
        self.check_method('/article/create/')

    def update_article_error(self):
        self.data['category_id'] = ''
        self.check_method('/article/update/2/')

    def check_method(self, url, method=None):
        if method == 'DEL':
            self.client.delete(url)
        else:
            self.client.post(url, data=self.data)
        article = Article.objects.filter(title=self.data['title'])
        self.assertEqual(len(article), 0)


class CategoryCRUDTest(TestCase):
    fixtures = ['fixtures/test_dump.json']

    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.data = {
            'title': 'Test',
            'parent_id': 1,
        }
        self.validation_message = 'Данная категория уже существует!'

    def test_category(self):
        self.add_category()
        self.update_category()
        self.delete_category()

    def test_category_error(self):
        self.add_category_error()
        self.update_category_error()

    def test_category_title_validation(self):
        self.add_category()
        form = CategoryForm(data=self.data, old_category=None)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], self.validation_message)

    def test_category_list(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

    def add_category(self):
        self.check_method('/category/create/')

    def update_category(self):
        self.data['title'] = 'Test_Category'
        self.check_method('/category/update/3/')

    def delete_category(self):
        self.check_method('/category/delete/3/', 'DEL')

    def add_category_error(self):
        self.data['title'] = ''
        self.check_method_error('/category/create/')

    def update_category_error(self):
        self.data['title'] = ''
        self.check_method_error('/category/update/2/')

    def check_method(self, url, method=None):
        if method == 'DEL':
            self.client.delete(url)
            self.category_filter(0)
        else:
            response = self.client.post(url, data=self.data)
            self.assertEqual(response.status_code, 302)
            self.category_filter(1)

    def check_method_error(self, url):
        self.client.post(url, data=self.data)
        self.category_filter(0)

    def category_filter(self, len_array):
        category = Category.objects.filter(title=self.data['title'])
        self.assertEqual(len(category), len_array)
