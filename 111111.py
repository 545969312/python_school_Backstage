import redis

# conn = redis.Redis(host='192.168.11.121', port=6379)

# conn.set('pengjing_name', '彭晶')

# val = conn.get('pengjing_name').decode('utf8')


# val = conn.keys()
# conn.flushall()

# print(val)

li = [ { "id": "2", "price_policy_dict": "{2: {'id': 2, 'price': 30000.0, 'valid_period_display': '6个月', 'valid_period': 180}, 3: {'id': 3, 'price': 10000.0, 'valid_period_display': '3个月', 'valid_period': 90}}", "name": "Linux运维基础", "default_price_id": "2", "img": "Linux运维基础" }, { "id": "1", "price_policy_dict": "{1: {'id': 1, 'price': 20000.0, 'valid_period_display': '6个月', 'valid_period': 180}, 4: {'id': 4, 'price': 20000.0, 'valid_period_display': '2个月', 'valid_period': 60}}", "name": "python入门", "default_price_id": "1", "img": "python入门" } ]
for i in li:
    print(i)
    print('-------------------')
    print(i.get('id'))