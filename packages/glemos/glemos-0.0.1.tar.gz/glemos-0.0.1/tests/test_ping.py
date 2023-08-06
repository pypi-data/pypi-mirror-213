from glemos.ping import ping

def test_ping():
    assert ping() == "pong"
