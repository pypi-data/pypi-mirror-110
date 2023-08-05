# encoding=utf-8

from http.server import HTTPServer, SimpleHTTPRequestHandler
import re
from threading import Thread

from logbook import Logger
from requests import HTTPError


log = Logger(__name__)


UPLOAD_PATH = '/image-upload'
PATH_PATTERN = re.compile(r'^/(?:image-upload/)?(?P<image_id>[a-f0-9\-]+)(?P<extension>\.nfi(:?\.idx)?)(:?\?.*)?$',
                          re.IGNORECASE)
PATH_TEMPLATE = '/image-upload/{image_id}{extension}'


def read_chunked(fobj):
    # read hexadecimal number of bytes in the next chunk
    chunk_size = int(fobj.readline(), 16)
    while chunk_size:
        yield fobj.read(chunk_size)
        # consume \r\n at the end of chunk
        fobj.readline()
        # read hexadecimal number of bytes in the next chunk
        chunk_size = int(fobj.readline(), 16)


class WebHDFSRequestHandler(SimpleHTTPRequestHandler):
    """
    HTTP request handler that mimics WebHDFS's handling of PUT requests.
    """
    def log_message(self, format, *args):
        # avoid super writing to stderr
        log.debug('{} - {}', self.address_string(), format % args)

    def do_redirect(self):
        path = PATH_PATTERN.match(self.path)
        if path:
            location = PATH_TEMPLATE.format(**path.groupdict())
            log.debug('sending temporary redirect from {} to {}', self.path, location)
            self.send_response(307)
            self.send_header('Location', location)
            self.end_headers()
            return None
        else:
            log.debug('sending bad request (cannot match path {} for redirect)', self.path)
            self.send_response(400)
            self.end_headers()
            return None

    def do_upload(self):
        path = PATH_PATTERN.match(self.path)
        if path:
            image_id = path.group('image_id')
            extension = path.group('extension')
            data = self.rfile
            if self.headers.get('Transfer-Encoding') == 'chunked':
                log.debug('getting chunked data, wrapping rfile with chunk generator')
                data = read_chunked(self.rfile)

            try:
                log.debug('forwarding image data as-is to remote')
                self.server.upload_callback(image_id=image_id, extension=extension, data=data)
            except HTTPError as e:
                log.exception('upload image data failed, no retry available: {}: {}: {}',
                              e.response.status_code, e.response.reason, e.response.text.strip(),
                              e)
                # close i/o resources (force broken pipe on the client side)
                data.close()
                self.rfile.close()
                # remote service can't process our request, indicate gateway error to client
                log.debug('sending bad gateway response for image {}', image_id)
                self.send_response(502)
                self.end_headers()
                return None

            log.debug('sending created response for image {}', image_id)
            self.send_response(201)
            self.end_headers()
            return None
        else:
            log.debug('sending bad request (cannot match path {} for upload)', self.path)
            self.send_response(400)
            self.end_headers()
            return None

    def do_PUT(self):  # noqa: N802
        log.debug('got PUT request for {}', self.path)

        try:
            if self.path.startswith(UPLOAD_PATH):
                return self.do_upload()
            else:
                return self.do_redirect()
        except Exception as e:
            log.exception('handling PUT request for {} failed', self.path, e)
            self.send_response(500)
            self.end_headers()
            return None


class WebHDFSServer(HTTPServer):
    """
    HTTP server that mimics WebHDFS on a local address.
    """
    def __init__(self, upload_callback):
        # bind to port 0, let OS find a free port
        super().__init__(('localhost', 0), WebHDFSRequestHandler)

        self.upload_callback = upload_callback
        self._thread = None

    def __enter__(self):
        if not self._thread:
            self._thread = Thread(name='webhdfs-server-{}'.format(self.server_port),
                                  target=self.serve_forever)
            log.info('starting WebHDFS server on port {} in the background', self.server_port)
            self._thread.start()

            return super().__enter__()
        else:
            raise ValueError('server already started or in error state')

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.info('shutting down WebHDFS server on port {}', self.server_port)
        self.shutdown()
        # wait for server thread to exit
        self._thread.join()
        self._thread = None

        return super().__exit__(exc_type, exc_val, exc_tb)
