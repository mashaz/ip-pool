# An component to get a valid ip in ip pool

```python
from ip_pool import IPPool
pool = IPPool(file_path=PROXY_FILE_PATH, req_per_proxy=1000)
while request:
    proxy = pool.get_an_ip()
```