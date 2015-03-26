import unittest
import transaction

from pyramid import testing

from .models import DBSession


class TestBlogPages(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        from .models import Base, Blog

        request = testing.DummyRequest()
        self.config = testing.setUp(request=request)

        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = Blog(title='testing title', body='testing body')
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def _makeOne(self, request):
        from .views import BlogPages
        inst = BlogPages(request)
        return inst

    def test_all_blogs_view(self):
        request = testing.DummyRequest()
        info = self._makeOne(request)
        data = info.all_blogs()
        self.assertIn(data[0]['title'], 'testing title')

    def test_add_blog_view(self):
        json_object = {'title': 'testing add_blog view', 'body': 'testing add_blog view body'}
        request = testing.DummyRequest(method='POST', json_body=json_object)
        info = self._makeOne(request)
        data = info.add_blog()
        self.assertEqual(data.status_int, 200)
        self.assertIn('Successfully added', data.body)

    def test_one_blog_view(self):
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = self._makeOne(request)
        data = info.one_blog()
        self.assertIn(data[0]['title'], 'testing title')

    def test_update_blog_view(self):
        json_object = {'title': 'testing update', 'body': 'testing update body'}
        request = testing.DummyRequest(method='PUT', json_body=json_object)
        request.matchdict['id'] = 1
        info = self._makeOne(request)
        data = info.update_blog()
        self.assertEqual(data.status_int, 200)
        self.assertIn('Successfully Updated', data.body)

    def test_delete_blog_view(self):
        from .models import Blog
        json_object = {'title': 'testing update', 'body': 'testing update body'}
        request = testing.DummyRequest(method='DELETE', json_body=json_object)
        request.matchdict['id'] = 1
        info = self._makeOne(request)
        data = info.delete_blog()
        query = DBSession.query(Blog).filter_by(id=request.matchdict['id']).first()
        self.assertIn('Successfully Deleted', data.body)
        self.assertEqual(query, None)
