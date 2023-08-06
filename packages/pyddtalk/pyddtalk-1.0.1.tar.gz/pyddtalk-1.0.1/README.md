# 版本更新

| ver   | desc               | date     |
| ----- | ------------------ | -------- |
| 1.0.1 | 初始化 | 20230611 |

# pyddtalk

- python wxwork server api
- version==1.0.1


# dingding python接口

- 写一个企微的python库，开箱即用。
- 这个接口库完全用于企微的服务端接口。


# how to use
### install pywxwork
`pip install pyddtalk`

### get token

```python
from pyddtalk.token import token

data = {
	"appKey":"dingasdfasdfasdfasd",
	"appSecret":"asdfasdfasfadsfads"
}

t = token(**data)
logger.debug(t.token)
```