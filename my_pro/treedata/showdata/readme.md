# showdata

### PFMEA

启动pfmea.py
**启动时本地需要安装rabbitmq并启动**

> nameko run pfmea --broker amqp://guest:guest@localhost

pfmea的json单独字段的格式
```
{ 'id': 1,
   'icon':'',
   'state':{},
   'text': '',
'nodes': [{
   'id': 1,
   'icon': '',
   'state': '',
    'text': **json**'}]
  ```
  其中json为之后的数据不存在`id`这个key,

JSON字段的导出的样例
```json
[
  {
    'id': 43,
    'icon': 'glyphicon glyphicon-retweet',
    'state': {},
    'text': 'FF-01-01核对发动机正确性、检查外观',
    'nodes': [
      {
        'color': '#00EE76',
        'icon': 'glyphicon glyphicon-cog',
        'text': '正确的发动机图号',
        'tags': [
          'requirement'
        ]
      },
      {
        'color': '',
        'icon': '',
        'text': '',
        'tags': [
          'severity'
          ]
      },



```

JSON insert的标准数据

```json
{'id': 1,
  'icon': 'xxx',
  'tags': ['process']
  }
```

前端的逻辑在用户修改之后，传回json


### 关系型的增删改

#### 修改
前端返回数据的ID在后端进行接收参数并进行修改

#### JSON字段的增删改
前端返回字段的ID和修改后该行的内容，具体格式是
```json
{
		"requirements": {
			"failure_mode": {
				"causes_content": {
					"action_taken_result": {
						"severity": None,
						"occurrence": None,
						"detection": None,
						"RPN": None,
						"responsibility": None,
						"completion_date": None,
					},
					"occurrence": None,
					"detection": None,
					"control_prevention": None,
					"control_detection": None,
					"RPN": None,
					"recommended_action": None,
				},

				"effects_content": None,
				"severity": None,
				"classification": None,
			}
		}
	}
```
传回一个json id为pfmea的表id json为如上的样例
