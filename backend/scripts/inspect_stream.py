import sys, json
sys.path.insert(0, '.')
from app.api.endpoints.pois import get_pois
print('creating streaming response')
r = get_pois(27.670649,85.423223,0.3, True)
print('type:', type(r))
# attempt to find iterator
it = getattr(r, 'body_iterator', None) or getattr(r, 'streaming_content', None) or getattr(r, 'iterator', None)
print('iterator attr:', type(it))
try:
    # If it's a generator, consume one item
    first = next(it)
    print('first chunk type:', type(first))
    if isinstance(first, (bytes, bytearray)):
        print('first chunk length:', len(first))
        print(first[:200])
    else:
        s = json.dumps(first, default=str)
        print('first chunk as json len:', len(s))
except Exception as e:
    print('error while iterating:', e)
print('done')
