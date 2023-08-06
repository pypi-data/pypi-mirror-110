# Concurrent_Decorator

## 简介
用于python进行并发工作的装饰器
- [x] 多线程装饰器
- [] ~~多进程装饰器~~
- [] 多进程+协程装饰器


## 用法
```python
from concurrent_decorator import mul_threadpool
import time
# 单参数函数可以直接调用
@mul_threadpool(max_workers=2,args_list=[1,2,1])  
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times

print(get_html())

# 多参数函数丢进字典后使用
a=[1,1,1]
b=[0.5,0,1]
data=[]
for i in range(len(a)):
    data.append({'a':a[i],'b':b[i]})
@mul_threadpool(max_workers=2,args_list=data)
def add(data=None):
    a=data['a']
    b=data['b']
    # print(a,b)
    time.sleep(a+b)
    return a+b
print(add())
```