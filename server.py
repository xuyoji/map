#-*- coding:utf-8 -*-
import sys, os, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

#-------------------------------------------------------------------------------

class ServerException(Exception):
    '''服务器内部错误'''
    pass

#-------------------------------------------------------------------------------

class base_case(object):
    '''条件处理基类'''

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)
            
    def handle_text(self, handler, content):
        text = str(content)
        handler.send_content(text)
    
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'

#-------------------------------------------------------------------------------

class case_no_file(base_case):
    '''文件或目录不存在'''

    def test(self, handler):
        print(handler.path, handler.path.startswith('/getpath'))
        return (not handler.path.startswith('/getpath') and not os.path.exists(handler.full_path))

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

#-------------------------------------------------------------------------------

class case_cgi_file(base_case):
    '''可执行脚本'''

    def run_cgi(self, handler):
        data = subprocess.check_output(["python", handler.full_path])
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
               handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)

#-------------------------------------------------------------------------------

class case_existing_file(base_case):
    '''文件存在的情况'''

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)

#-------------------------------------------------------------------------------
class case_get_path(base_case):
    '''返回请求的两点之间的路径'''
    import data
    import mapHandler
    aMap = mapHandler.Map(data.node, data.edge)
    first_act  = True
    
    def test(self, handler):
        return handler.path.startswith("/getpath") and \
            len(handler.path[8:].split('-')) == 3
        
    def act(self, handler):
        [node1, node2] = [int(_) for _ in handler.path[9:].split('-')]
        if self.first_act:
            self.aMap.get_min_path()
            first_act = False
        path = self.aMap.get_one_path(node1, node2)
        self.handle_text(handler, path)
        
        
#-------------------------------------------------------------------------------
class case_directory_index_file(base_case):
    '''在根路径下返回主页文件'''

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

#-------------------------------------------------------------------------------

class case_always_fail(base_case):
    '''默认处理'''

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))

#-------------------------------------------------------------------------------

class RequestHandler(BaseHTTPRequestHandler):
    '''
    请求路径合法则返回相应处理
    否则返回错误页面
    '''

    Cases = [case_get_path(),
             case_cgi_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_no_file(),
             case_always_fail()]

    # 错误页面模板
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    def do_GET(self):
        try:

            # 得到完整的请求路径
            self.full_path = os.getcwd() + self.path

            # 遍历所有的情况并处理
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break

        # 处理异常
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

    # 发送数据到客户端
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        if  type(content) is str:
            content = bytes(content, 'utf-8')
        self.wfile.write(content)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    serverAddress = ('', 8081)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
