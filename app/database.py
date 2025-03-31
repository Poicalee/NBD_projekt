from riak import RiakClient

from app.config import RIAK_HOST, RIAK_PORT


def connect_to_riak():
    try:
        client = RiakClient(protocol='pbc', host=RIAK_HOST, pb_port=RIAK_PORT)
        if client.ping():
            print("✅ Połączono z Riak!")
        else:
            print("❌ Błąd połączenia z Riak")
        return client
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None