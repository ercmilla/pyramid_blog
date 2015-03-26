import json

from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from sqlalchemy.exc import DBAPIError

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
        return Response('Success add blog titled: ' + request.json_body['title'])

    @view_config(route_name='one_blog', request_method='GET', renderer='json')
    def one_blog(self):
        blog_id = self.request.matchdict['id']
        blog_entry = DBSession.query(Blog).filter_by(id=blog_id).one()

        blog_json = [{'title': blog_entry.title, 'body': blog_entry.body}]

        return blog_json

    @view_config(route_name='one_blog', request_method='PUT')
    def update_blog(self):
        blog_id = self.request.matchdict['id']
        DBSession.query(Blog).filter_by(id=blog_id).update().values(
                title=self.request.json_body['title'], 
                body=self.request.json_body['body'])

        return Response('Successfully Updated Blog ID: ' + blog_id)



# @view_config(route_name='all_blogs', request_method='GET',  renderer='json')
# def my_view(request):
#     all_blogs = DBSession.query(Blog).all()
#     blogs_json = []
# 
#     for blog in all_blogs:
#         json_prod = {'title': blog.title, 'body': blog.body}
#         blogs_json.append(json_prod)
# 
#     return blogs_json
# @view_config(route_name='all_blogs', request_method='POST')
# def add_blog(request):
#     blog_entry = Blog(title=request.json_body['title'], body=request.json_body['body'])
#     DBSession.add(blog_entry)
#     return Response('Success')
