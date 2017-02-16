#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Leon Hwa'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from aiohttp import web
from coroweb import get, post

from Models import User, Comment, Blog,Tag, next_id
from  apis import APIValueError,APIError,APIPermissionError,PageManager

import os
COOKIE_NAME = 'awesession'
_COOKIE_KEY = 'nkjnihyugyftff'

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

@asyncio.coroutine
def getAdmin():
    admins = yield from User.findAll('admin = 1')
    admin = None
    if len(admins):
        admin = admins[0]
    return  admin

@asyncio.coroutine
def getTagLen():
    return  (yield from Tag.findNumber('count(id)'))

@get('/')
def index(*,page = '1'):
    page_index = get_page_index(page)
    blogCount = yield from Blog.findNumber('count(id)')
    page = PageManager(blogCount, page_index)
    blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    admin = None
    admin = yield from getAdmin()
    if admin:
        admin.tagLen = yield from getTagLen()
    # jinja2
    return {
        '__template__': 'blogs.html',
        'blogCount':blogCount,
        'page_index' : page_index,
         'page':page,
         'blogs':blogs,
         'admin':admin
    }

@get('/register')
def user_registers(request):
    admin = None
    admin = yield from getAdmin()
    if admin:
      admin.tagLen = yield from getTagLen()
    return {
        '__template__':'register.html',
        'admin': admin
    }


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@get('/archives/')
def  archives(*,page = '1'):
    page_index = get_page_index(page)
    blogCount = yield from Blog.findNumber('count(id)')
    page = PageManager(blogCount, page_index,page_base = 6)
    blogs = yield from  Blog.findAll(orderBy='created_at desc',limit=(page.offset,page.limit))
    admin = None
    admin = yield from getAdmin()
    if admin:
        admin.tagLen = yield from getTagLen()
    return {
        '__template__':'blog_list.html',
        'blogCount': blogCount,
        'page_index': page_index,
        'page': page,
        'blogs': blogs,
        'admin':admin
    }

@get('/tags/{tag}')
def tag_archives(*,page = '1',tag):
    page_index = get_page_index(page)
    t_tag = '#'+tag
    tags_arr = yield from Tag.findAll('tag=?',[t_tag])
    ids = tags_arr[0].blog_ids
    id_arr = re.findall(r'#([0-9a-zA-Z]*)',ids)
    length = len(id_arr)
    base_sql = 'id=? '
    base_arr = []
    for i in range(length):
         base_arr.append(base_sql)
    sql = 'or '.join(base_arr)
    temp_blogs = yield from Blog.findAll(sql,id_arr)
    sort_blogs = []
    page = PageManager(len(temp_blogs), page_index,page_base = 6)
    blogs = temp_blogs[page.offset:page.limit]
    admin = None
    admin = yield from getAdmin()
    if admin:
        admin.tagLen = yield from getTagLen()
    return {
        '__template__':'blog_list.html',
        'blogCount': len(temp_blogs),
        'page_index': page_index,
        'page': page,
        'blogs': blogs,
        'admin':admin,
        'tag':tags_arr[0]
    }
@get('/tags')
def  tags(request):
    blogCount = yield from Blog.findNumber('count(id)')
    admin = yield from getAdmin()
    tags = yield from  Tag.findAll()
    if admin:
        admin.tagLen = len(tags)
    return {
        '__template__': 'tags.html',
        'blogCount': blogCount,
        'admin':admin,
        'tags': tags,
    }

@get('/signin')
def user_sigin(request):
    return {
        '__template__' :'login.html'
    }


def user2cookie(user,max_age):
    expiress = str(int(time.time()) + max_age)
    s = '%s-%s-%s-%s' % (user.id,user.passwd,expiress,_COOKIE_KEY)
    L = [user.id,expiress,hashlib.sha1(s.encode('utf-8')).hexdigest()]
    logging.info('-'.join(L))
    logging.info('cookie设置好了')
    return '-'.join(L)

@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r



#请求创建博客页面
@get('/manager/blog/create')
def editBlog(request):
    return {
            '__template__': 'manage_blog_create.html',
            'id': '',
            'action': '/api/blogs'
    }
#修改博客
@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }

#可编辑博客列表
@get('/manager/blogs')
def manage_blogs(*, page='1'):
    page_index = get_page_index(page)
    blogCount = yield from Blog.findNumber('count(id)')
    page = PageManager(blogCount, page_index)
    blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    admins = yield from User.findAll('admin = 1')
    admin = None
    if len(admins):
        admin = admins[0]
    if admin:
        admin.tagLen = yield from getTagLen()
    return {
        '__template__': 'manage_blogs.html',
        'blogCount': blogCount,
        'page_index': page_index,
        'page': page,
        'blogs': blogs,
        'admin':admin
    }
@get('/blog/{id}')
def get_detailBlog(request,*,id):
    blog = yield from Blog.find(id)
    blogCount = yield from Blog.findNumber('count(id)')
    user = request.__user__
    if not user:
       blog.scan_count = blog.scan_count + 1
       yield from blog.update()
    elif user.admin == 0:
        blog.scan_count = blog.scan_count + 1
        yield from blog.update()
    admin = None
    admin = yield from getAdmin()
    if admin:
        admin.tagLen = yield from getTagLen()
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'blogCount':blogCount,
        'admin':admin
    }



@post('/upload/blogs/imgae/')
def upload_image(request):
    # data = await request.post()
    # image_data = data['upload']
    #
    # filename = image_data.filename
    # image_file = image_data.file
    # image_content = image_file.read()
    # logging.info(data)
    # logging.info(filename)
    # return web.Response(text='success:%s ' % filename)
    reader = yield from request.multipart()
    image_data = yield from reader.next()
    filename = image_data.filename
    size = 0
    upload_path = '/upload/blogs/image/'
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    with open(os.path.join(upload_path, filename), 'wb') as f:
        while True:
            chunk = yield from image_data.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='../upload/blogs/image/' + filename)

@post('/upload/icon')
def upload_icon(request):
    reader = yield from request.multipart()
    image_data = yield from reader.next()
    filename = image_data.filename
    logging.info(image_data)
    size = 0
    upload_path = '/upload/adminIcon/'
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    with open(os.path.join(upload_path, filename), 'wb') as f:
        while True:
            chunk = yield from image_data.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    admins = yield from User.findAll('admin = 1')
    admin = admins[0]
    admin.image = os.path.join('../upload/adminIcon/', filename)
    yield from  admin.update()
@get('/manager')
def manager(request):
    admin = None
    if request.__user__.admin:
        admin = request.__user__
    return {
        '__template__': 'manage.html',
        'admin' : admin
    }
# ######################################################------API--------#####################################################
'''
API
'''



@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    else:
        logging.info('找到用户')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    logging.info('设置cookie成功')
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 注册
@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    logging.info('注册~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    users = yield from User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    yield from user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


#翻页
@get('/api/blogs')
def get_api_blogs(*,page= '1'):
    page_index = get_page_index(page)
    blogCount = yield from Blog.findNumber('count(id)')
    page = PageManager(blogCount, page_index)
    blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    return  dict(blogs = blogs,page = page,page_index = page_index)

#创建博客
@post('/api/blogs')
def api_create_blog(request, *, blogtitle, blogsummary, blogcontent,tags):
    # check_admin(request)
    if not blogtitle or not blogtitle.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not blogsummary or not blogsummary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not blogcontent or not blogcontent.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(tag=tags,user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=blogtitle.strip(), summary=blogsummary.strip(), content=blogcontent)
    yield from  blog.save()
    logging.info(blogcontent)
    yield from addTag(blog,tags)
    return blog

@asyncio.coroutine
def  addTag(blog,tags):
    tag_str_arr = tags.split()
    for tag_str in tag_str_arr:
        if not tag_str.startswith('#'):
            continue
        tag_arr = yield from Tag.findAll('tag=?', [tag_str])
        if tag_arr:  # 数据库有此tag
            has_tag = tag_arr[0]
            blog_id_arr = has_tag.blog_ids.split('#')
            if not blog.id in blog_id_arr:  # 该tag 和该条blog没关联过
                has_tag.blog_ids = has_tag.blog_ids + '#' + blog.id
                yield from has_tag.update()
        else:  # 没有此tag  new一个
            tag = Tag(tag=tag_str, blog_ids=('#' + blog.id))
            yield from tag.save()
#修改博客
@post('/api/blogs/{id}')
def api_update_blog(id, request, *, name, summary, content,tags):
    check_admin(request)
    blog = yield from Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    blog.tag = tags
    yield from blog.update()
    yield from addTag(blog, tags)
    return blog

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

# @get('/api/blogs')
# async def api_blogs(*, page='1'):
#     page_index = get_page_index(page)
#     blogCount = await Blog.findNumber('count(id)')
#     page = PageManager(blogCount,page_index)
#     blogs = await Blog.findAll(orderBy='created_at desc',limit=(page.offset,page.limit))
#     return dict(blogs = blogs,page = page)

@get('/api/blogs/{id}')
def get_blog(request,*,id):
    blog = yield from Blog.find(id)
    return dict(blog = blog)

@post('/api/blogs/{id}/delete')
def api_delete_blog(request, *, id):
    check_admin(request)
    blog = yield from  Blog.find(id)
    yield from blog.remove()
    return dict(id=id)


@post('/manager/{id}')
def saveManagerInfo(id,*,image,blogName,blogDescription,ownName,ownDescription,githubSite):
     user = yield from User.find(id)
     if user:
       user.image = image
       user.blogName = blogName
       user.blogDescription = blogDescription
       user.ownName = ownName
       user.ownDescription = ownDescription
       user.githubSite = githubSite
       yield from  user.update()

