import usocket as socket
import os
HTTP_HEAD="""HTTP/1.1 200 OK
Content-Type: %s; charset=utf-8
Content-Length: %d\n\n"""

def server():
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0",8080))
    s.listen(5)
    print("Server started at port 8080")
    while True:
        res=s.accept()
        client=res[0]
        req=client.recv(1024).decode()
        #处理请求头
        method=req[0:req.find(" ")]
        path=req[4:req.find("HTTP")-1]
        print(method,path)
        if method=="GET":
            #尝试获取文件
            try:
                filesize=os.stat(path)[6]
                file=open(path,"rb")
                client.write(HTTP_HEAD%("text/plain",filesize))
                while True:
                    buf=file.read(4096)
                    if buf==b'':
                        file.close()
                        break
                    client.write(buf)
            except:
                content="File Not Found: "+path
                client.write(HTTP_HEAD%("text/html",len(content)))
                client.write(content)
        client.close()
server()