import memcache

client =memcache.Client(['192.168.5.7:11211'])

data =client.get_stats()
print(data)