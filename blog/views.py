from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from .models import (
    DBSession,
    Blog,
    )


@view_defaults(route_name='all_blogs')
class BlogPages:

    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='json')
    def all_blogs(self):
        all_blogs = DBSession.query(Blog).all()
        blogs_json = []

        for blog in all_blogs:
            json_prod = {'title': blog.title, 'body': blog.body}
            blogs_json.append(json_prod)

        return blogs_json

    @view_config(request_method='POST')
    def add_blog(self):
        blog_entry = Blog(title=self.request.json_body['title'], body=self.request.json_body['body'])
        DBSession.add(blog_entry)
        return Response('Successfully added blog titled: ' + self.request.json_body['title'])

    @view_config(route_name='one_blog', request_method='GET', renderer='json')
    def one_blog(self):
        blog_id = self.request.matchdict['id']
        blog_entry = DBSession.query(Blog).filter_by(id=blog_id).one()

        blog_json = [{'title': blog_entry.title, 'body': blog_entry.body}]

        return blog_json

    @view_config(route_name='one_blog', request_method='PUT')
    def update_blog(self):
        blog_id = self.request.matchdict['id']
        title = self.request.json_body.get('title', None)
        body = self.request.json_body.get('body', None)
        data = DBSession.query(Blog).filter_by(id=blog_id).first()
        if title is not None:
            data.title = title
        if body is not None:
            data.body = body

        return Response('Successfully Updated Blog ID: ' + str(blog_id))

    @view_config(route_name='one_blog', request_method='DELETE')
    def delete_blog(self):
        blog_id = self.request.matchdict['id']
        DBSession.query(Blog).filter_by(id=blog_id).delete()
        return Response('Successfully Deleted Blog ID: ' + str(blog_id))
