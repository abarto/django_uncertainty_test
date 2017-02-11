from random import randint

from django.http import StreamingHttpResponse


DEFAULT_CHUNK_SIZE = 1024 * 256


def _test_stream_generator(content_length, chunk_size=DEFAULT_CHUNK_SIZE):
    for _ in range(0, content_length, chunk_size):
        yield bytes([randint(0, 127) for _ in range(0, chunk_size)])


def test_stream(request):
    return StreamingHttpResponse(_test_stream_generator(1024 * 1024 * 100),
                                 content_type='application/octet-stream')
