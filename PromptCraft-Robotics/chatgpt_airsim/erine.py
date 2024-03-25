import os
import qianfan

# 使用安全认证AK/SK鉴权，通过环境变量初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_ACCESS_KEY"] = "NezTyNjYkUdXExhuyX4JhvD1"
os.environ["QIANFAN_SECRET_KEY"] = "3M4qRRQlfmQPTV8WYxx1Q92AMJzuf8pk"

chat_comp = qianfan.ChatCompletion()

# 指定特定模型
resp = chat_comp.do(model="ERNIE-Bot", messages=[{
    "role": "user",
    "content": "你好"
}])

print(resp)