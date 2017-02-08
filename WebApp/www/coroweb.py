#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
def a(a, b=0, *c, d, e=1, **f):
    pass
    a:  kind:POSITIONAL_OR_KEYWORD default:empty
    b:  kind:POSITIONAL_OR_KEYWORD  default:0
    *c: kind:VAR_POSITIONAL   default:empty
    d: KEYWORD_ONLY  default:empty
    e=1:KEYWORD_ONLY    default:1
    **f: VAR_KEYWORD   default:empty
'''
import  asyncio
import inspect,logging,functools,os
import  inspect
from aiohttp import  web

from urllib import parse
from apis import APIError
def post(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func) #似的 func.__name__的时候 是本来fuc的名字  而不是decorator
        def wrapper(*args,**kw):
            return  func(*args,**kw)
        #函数相当于一个类 所以可以给一个类添加属性为__method__和__route__  方便后面标记和识别该方法
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func) #似的 func.__name__的时候 是本来fuc的名字  而不是decorator
        def wrapper(*args,**kw):
            return  func(*args,**kw)
        #函数相当于一个类 所以可以给一个类添加属性为__method__和__route__  方便后面标记和识别该方法
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return  wrapper
    return decorator


#这是什么?????
def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
    app.router.add_static('/upload/', path2)
    logging.info('add static %s => %s' % ('/static/', path))

def get_required_kw_args(fn):#  如果参数如: e   返回 e
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):#  如果参数如: e = 1 或e    返回 e
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

def has_named_kw_args(fn):#  如果参数如: e = 1
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):#  如果参数如: **f
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):#  如果参数为 request
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found
class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)

    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)






def add_route(app,fn):
    method = getattr(fn,'__method__',None)
    path = getattr(fn,'__route__',None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)

    logging.info('add route %s %s => %s(%s)' %(method,path,fn.__name__, ','.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method,path,RequestHandler(app,fn))

def add_routes(app,module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name,globals(),locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n],globals(),locals(),[name]),name)

    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod,attr)
        if callable(fn):
            method = getattr(fn,'__method__',None)
            path = getattr(fn,'__route__',None)
            if method and path:
                add_route(app,fn)

