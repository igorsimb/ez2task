from django.test import SimpleTestCase, tag
from django.urls import reverse, resolve

from main_app.views import IndexView, ManageUsersView, ItemListView, MyTasksView, ItemDetailView

@tag('unit')
class TestUrls(SimpleTestCase):

    def test_main_page_url_resolves(self):
        url = reverse('main')
        self.assertEquals(resolve(url).func.view_class, IndexView)

    def test_manage_users_url_resolves(self):
        url = reverse('manage_users')
        self.assertEquals(resolve(url).func.view_class, ManageUsersView)

    def test_manage_tasks_url_resolves(self):
        url = reverse('manage_tasks')
        self.assertEquals(resolve(url).func.view_class, ItemListView)

    def test_my_tasks_url_resolves(self):
        url = reverse('my_tasks')
        self.assertEquals(resolve(url).func.view_class, MyTasksView)

    def test_task_detail_url_resolves(self):
        url = reverse('detail', args=[10])
        self.assertEquals(resolve(url).func.view_class, ItemDetailView)

