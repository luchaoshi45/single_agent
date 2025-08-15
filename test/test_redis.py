import redis

r = redis.Redis.from_url("rediss://default:ARUBAAImcDFlNTUzZmY4Yjc0ODc0M2NjYjBlMDY5ZjlmMTJmOGUzYXAxNTM3Nw@great-kingfish-5377.upstash.io:6379")

r.set('foo', 'bar')
value = r.get('foo')