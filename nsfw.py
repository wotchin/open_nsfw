import socket
import threading
import re
import random
import time
import urllib
import os
import gc
# import asyncore
import classify_nsfw as cn
# import time

HOST, PORT = "0.0.0.0", 8888


class Singleton(object):
    __instance = None
    __LinkedNum = 0
    __lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get():
        Singleton.__lock.acquire()
        num = Singleton.__LinkedNum
        Singleton.__lock.release()
        return num

    @staticmethod
    def increase():
        Singleton.__lock.acquire()
        Singleton.__LinkedNum += 1
        Singleton.__lock.release()

    @staticmethod
    def decrease():
        Singleton.__lock.acquire()
        Singleton.__LinkedNum -= 1
        Singleton.__lock.release()

    def __new__(cls, *args, **kwd):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls, *args, **kwd)
            #Singleton.__lock = threading.Lock
        return Singleton.__instance


def rand_str(length):
    string = "abcdefghijklmnopqrstuvwxyz123456789"
    t = int(round(time.time() * 1000))
    ret = ""
    for i in range(0, length):
        num = random.randrange(0, len(string) - 1)
        ret += string[num]
    return ret + str(t)


def customer(client_connection):
    Singleton().increase()
    url = ""
    http_response = "HTTP/1.1 200 OK\r\n\r\n"
    # time.sleep(3)
    try:
        request = client_connection.recv(100)
        try:
            url = re.findall("/url=(.*?) HTTP", request.decode('utf8'))[0]
            url = urllib.unquote(url)
        except:
            http_response += "format error"
            pass
        ## event
        if url != "":
            # print(request)
            # print(url)
            filename = "./tmp/" + rand_str(10)
            try:
                urllib.urlretrieve(url=url, filename=filename)
                try:

                    ret = (cn.check(filename, "nsfw_model/deploy.prototxt",
                                    "nsfw_model/resnet_50_1by2_nsfw.caffemodel"))
                    if ret >= 0.5:
                        http_response += "0"
                    elif ret <= 0.05:
                        http_response += "2"
                    else:
                        http_response += "1"
                except Exception, e:
                    http_response += "judge error : " + str(e)
                finally:
                    if os.path.exists(filename):
                        os.remove(filename)
            except Exception, e:
                http_response += "download error : " + str(e)
    ## event
        client_connection.sendall(http_response)
    except:
        pass
    finally:
        client_connection.close()
        Singleton().decrease()
        gc.collect()



def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(5)
    while True:
        client_connection, client_address = listen_socket.accept()
        # print(Singleton().get())
        if Singleton().get() > 30:
            client_connection.close()
        else:
            threading.Thread(target=customer, args=(client_connection,)).start()


if __name__ == '__main__':
    main()
