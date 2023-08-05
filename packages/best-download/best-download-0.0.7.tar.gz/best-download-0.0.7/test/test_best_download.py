from best_download import download_file

import random
import struct
from flask import Flask, send_from_directory, request
import requests
import os
from multiprocessing import Process
import time
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer

import logging
logger = logging.getLogger(__name__)

# ================ SUPPORT CODE ================ #
test_file_name = "100mb.test"
file_directory = os.path.dirname(os.path.abspath(__file__))
test_file_path = os.path.join(file_directory, test_file_name)

hello_world_text = "<p>Hello, World!</p>"

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(503)
        self.end_headers()

    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", "http://localhost:5000/no_head")
        self.end_headers()

def basic_server():
    hostName = "localhost"
    serverPort = 5001

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

# Will sleep 1 second per chunk to delay file transmission 
def get_chunks(file_path, chunks_needed):
    with open(file_path, "rb") as fh:
        data = fh.read()
        chunk_size = int(len(data) / chunks_needed)
        start = 0
        end = min(start + chunk_size, len(data))
        while True:
            chunk = data[start:end]
            yield chunk
            if end == len(data):
                break
            time.sleep(1)
            start += chunk_size
            end = min(start + chunk_size, len(data))

def flask_server():
    app = Flask(__name__, static_url_path="", static_folder=file_directory)

    @app.route("/")
    def hello_world():
        return hello_world_text

    @app.route("/basic_test")
    def basic_test():
        return send_from_directory("", test_file_name)

    @app.route("/interrupted_with_head")
    def interrupted_with_head():
        # 5 second total send
        return app.response_class(get_chunks(test_file_path, 5), mimetype="application/octet-stream")

    @app.route("/no_head")
    def no_head_test():
        return send_from_directory("", test_file_name)

    app.run(debug=True)

class RunServer:
    p = None   
    function = None

    def __init__(self, function):
        self.function = function

    def __enter__(self):       
        self.p = Process(target=self.function)
        self.p.start()
        time.sleep(5)

    def __exit__(self, exc_type, exc_value, traceback):
        self.p.terminate()

def create_100mb_file():
    file_size = 104857600
    with open("100mb.test", "wb") as fh:
        for i in range(int(file_size / 8)):
            fh.write(struct.pack("Q", random.randint(0, 18446744073709551615)))

# ================ TESTS ================ #
# def test_chunking():
#     file_size = os.path.getsize(test_file_path)
#     total_size = 0
#     reconstructed = b""
#     with open(test_file_path, "rb") as fh:
#         original = fh.read()
#     for chunk in get_chunks(test_file_path, 5):
#         total_size += len(chunk)
#         reconstructed += chunk

#     assert(file_size == total_size)
#     assert(reconstructed == original)

# def test_create_file():    
#     if not os.path.exists(test_file_path):
#         logger.info("Creating test file")
#         create_100mb_file()

# def test_flask_server():
#     logger.info("testing flask server")
#     with RunServer(flask_server) as fs:
#         url = "http://localhost:5000"
#         result = requests.get(url)
#         # logger.info(result.text)
#         assert(result.text == hello_world_text)

# def test_basic_server():
#     with RunServer(basic_server) as s:
#         url = "http://localhost:5001/no_head"
#         result = requests.head(url)
#         assert(result.status_code == 503)

def get_checksum(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as fh:
        data = fh.read()
        hasher.update(data)
        return hasher.hexdigest()

# def test_standard_case():
#     expected_checksum = get_checksum(test_file_path)
#     logger.info(f"Expected Checksum: {expected_checksum}")        

#     with RunServer(flask_server) as fs:
#         url = "http://localhost:5000/basic_test"
#         out_file = test_file_name + "1"
#         download_file(url, out_file, expected_checksum)
#         # actual_checksum = get_checksum(test_file_name)
#         # logger.info(f"Actual Checksum: {actual_checksum}")
#         os.remove(out_file)
#         os.remove(out_file + ".ckpnt")

def rm(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def do_download(url, out_file, expected_checksum):
    try:
        download_file(url, out_file, expected_checksum)
    except Exception as ex:
        return ex

    return None


def test_interrupted_with_head():
    expected_checksum = get_checksum(test_file_path)
    # logger.info(f"Expected Checksum: {expected_checksum}")        

    with RunServer(flask_server) as fs:
        url = "http://localhost:5000/interrupted_with_head"
        out_file = test_file_name + "2"
        rm(out_file)
        p = Process(target=do_download, args=(url, out_file, expected_checksum))
        p.start()
        time.sleep(2.5) # Interrupt server half way through        
        # Leave with and interrupt flask server

    time.sleep(10) # let it fail out

    with RunServer(flask_server) as fs:
        url = "http://localhost:5000/interrupted_with_head"
        out_file = test_file_name + "2"
        rm(out_file)
        p = Process(target=do_download, args=(url, out_file, expected_checksum))
        p.start()
        time.sleep(2.5) # Interrupt server half way through        
        # Leave with and interrupt flask server    




    def __exit__(self, exc_type, exc_value, traceback):
        self.p.terminate()
        download_file(url, out_file, expected_checksum)
        # actual_checksum = get_checksum(test_file_name)
        # logger.info(f"Actual Checksum: {actual_checksum}")
        # os.remove(out_file)



# def test_no_head():
#     expected_checksum = get_checksum(test_file_path)
#     logger.info(f"Expected Checksum: {expected_checksum}")

#     # No idea how to handle head requests in flask - use http.server for head and redirect on the get
#     with RunServer(basic_server) as s:
#         with RunServer(flask_server) as fs:
#             url = "http://localhost:5001/no_head"
#             out_file = test_file_name + "3"
#             download_file(url, out_file, expected_checksum)
#             os.remove(out_file)
#             os.remove(out_file + ".ckpnt")



    # logger.info(result)
    # logger.info(result.text)

        # url = "http://localhost:5000/no_head"
        # result = requests.get(url)
        # logger.info(result)
        # logger.info(result.text)
        # logger.info(result.text)
        # assert(result.text == hello_world_text)



