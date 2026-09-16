# Python 学习笔记

---

## 1. 基础语法

### 1.1 变量与数据类型
Python 是动态类型语言，无需声明变量类型。
```python
# 基本数据类型
integer_num = 10          # int
float_num = 3.14          # float
string_val = "Hello"      # str
boolean_val = True        # bool
none_val = None           # NoneType

# 查看类型
print(type(integer_num))  # <class 'int'>
```

### 1.2 字符串操作
```python
s = "Python"
# 格式化字符串 (f-string, Python 3.6+)
name = "Alice"
print(f"Hello, {name}!")

# 常用方法
print(s.upper())          # PYTHON
print(s.lower())          # python
print(s[0:3])             # Pyt (切片)
print(len(s))             # 6
```

---

## 2. 控制流

### 2.1 条件语句
注意 Python 使用缩进（通常是 4 个空格）表示代码块，没有大括号。
```python
x = 10
if x > 5:
    print("x 大于 5")
elif x == 5:
    print("x 等于 5")
else:
    print("x 小于 5")
```

### 2.2 循环语句
```python
# for 循环
for i in range(5):       # range(5) 生成 0, 1, 2, 3, 4
    print(i)

# while 循环
count = 0
while count < 3:
    print(count)
    count += 1

# break 和 continue
for i in range(5):
    if i == 2:
        continue # 跳过本次循环
    if i == 4:
        break    # 跳出整个循环
    print(i)
```

---

## 3. 数据结构

### 3.1 列表 - 有序、可变
```python
my_list = [1, 2, 3, "a"]
my_list.append(4)        # 末尾添加 [1, 2, 3, 'a', 4]
my_list.pop()           # 弹出末尾元素 4
my_list[0] = 100        # 修改元素 [100, 2, 3, 'a']
```

### 3.2 元组 - 有序、不可变
```python
my_tuple = (1, 2, 3)
# my_tuple[0] = 100     # 报错！元组不可变
```

### 3.3 字典 - 键值对、可变
```python
my_dict = {"name": "Bob", "age": 25}
my_dict["age"] = 26      # 修改值
my_dict["city"] = "NYC"  # 新增键值对
print(my_dict.keys())    # dict_keys(['name', 'age', 'city'])
```

### 3.4 集合 - 无序、不重复
```python
my_set = {1, 2, 2, 3, 3}
print(my_set)            # {1, 2, 3}
my_set.add(4)
```

---

## 4. 函数

### 4.1 定义与调用
```python
def greet(name, greeting="Hello"):
    """
    这是一个文档字符串
    带有默认参数的函数
    """
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!
```

### 4.2 匿名函数
```python
# 适用于简短的、单行函数
add = lambda x, y: x + y
print(add(5, 3))               # 8
```

---

## 5. 面向对象编程 (OOP)

### 5.1 类与对象
```python
class Dog:
    # 类变量
    species = "Canis familiaris"

    # 初始化方法 (构造函数)
    def __init__(self, name, age):
        # 实例变量
        self.name = name
        self.age = age

    # 实例方法
    def bark(self):
        return f"{self.name} says Woof!"

# 实例化
my_dog = Dog("Rex", 3)
print(my_dog.bark())  # Rex says Woof!
```

### 5.2 继承
```python
class Puppy(Dog):
    def __init__(self, name, age, toy):
        super().__init__(name, age) # 调用父类构造方法
        self.toy = toy

    # 重写父类方法
    def bark(self):
        return f"{self.name} says Yip!"
```

---

## 6. 文件操作

推荐使用 `with` 语句，它会自动处理文件的关闭。
```python
# 写入文件
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")
    f.write("这是第二行。")

# 读取文件
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

---

## 7. 异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"错误: {e}")  # 错误: division by zero
except Exception as e:
    print(f"发生了未知错误: {e}")
else:
    print("没有发生异常时执行")
finally:
    print("无论是否异常，都会执行")
```

---

## 8. 模块与包

### 8.1 导入模块
```python
# 导入标准库
import math
print(math.pi)

# 导入并设置别名
import numpy as np
print(np.array([1, 2, 3]))

# 从模块导入特定函数
from random import randint
print(randint(1, 10))
```

### 8.2 安装第三方库
在命令行中使用 `pip`：
```bash
pip install requests
pip install -r requirements.txt
```

---

## 9. 进阶特性

### 9.1 列表推导式
非常 Pythonic 的写法，简洁且运行速度快。
```python
# 生成 0-9 的平方列表
squares = [x**2 for x in range(10)]

# 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

### 9.2 生成器
使用 `yield` 关键字，节省内存，按需生成数据。
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num, end=" ") # 0 1 1 2 3 5 8 13 21 34 
```

### 9.3 装饰器
不修改原函数代码的情况下，扩展函数功能。
```python
def my_timer(func):
    def wrapper(*args, **kwargs):
        print("函数开始执行...")
        result = func(*args, **kwargs)
        print("函数执行完毕。")
        return result
    return wrapper

@my_timer
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("World")
# 输出:
# 函数开始执行...
# Hello, World!
# 函数执行完毕。
```

---

---

## 10. 内存管理：栈与堆

在 Python 中，内存管理主要由解释器自动完成（垃圾回收机制），但理解栈和堆的区别，对于掌握变量赋值、函数调用以及可变/不可变对象的行为至关重要。

### 10.1 栈
栈用于**静态内存分配**，主要管理函数的调用和局部变量。
- **特点**：遵循“后进先出”（LIFO）原则，由操作系统自动分配和释放，速度极快。
- **存储内容**：
  - 函数的调用栈帧（包括返回地址、参数等）。
  - **基本类型的变量名和对象的引用（内存地址）**。
- **示例**：
  ```python
  def do_something():
      a = 10  # 'a' 这个变量名和指向整数对象 10 的引用存储在栈上
      b = "hello"
  # 函数执行完毕后，a 和 b 的栈空间立即被自动回收

### 10.2 堆
堆用于**动态内存分配**，主要存储在程序运行期间创建的对象。
- **特点**：空间大，但分配和管理相对较慢。Python 的垃圾回收器会自动回收不再被引用的堆内存（引用计数机制 + 分代回收）。
- **存储内容**：
  - **几乎所有的 Python 对象实体**（包括 int, str, list, dict, 类实例等）。
- **示例**：
  ```python
  x = [1, 2, 3]
  # 'x' 这个变量名存在栈上，它保存了一个地址
  # 真正的列表 [1, 2, 3] 对象实体存储在堆上
  ```

### 10.3 变量赋值的本质（深浅拷贝的根源）
理解了栈和堆，就能明白 Python 中“一切皆引用”的原理。
```python
a = [1, 2, 3]
b = a       # 将 a 的引用（堆地址）赋给 b，栈上多了个变量 b，指向堆上同一个对象
b[0] = 99
print(a)    # 输出 [99, 2, 3]，因为 a 和 b 指向堆里的同一个列表
```

---

## 11. 并发编程：进程与线程

Python 提供了多个模块来处理并发，最常用的是 `threading`（多线程）和 `multiprocessing`（多进程）。

### 11.1 进程与线程的概念
- **进程**：操作系统资源分配的最小单位。一个程序运行起来就是一个进程。进程间内存独立。
- **线程**：CPU 调度的最小单位。一个进程可以包含多个线程，线程共享进程的内存空间。

### 11.2 Python 的 GIL (全局解释器锁)
- CPython 解释器中存在 GIL。它确保**同一时刻只有一个线程在执行 Python 字节码**。
- **结论**：在 Python 中，多线程**不适合** CPU 密集型任务（会争夺 GIL），但**非常适合** I/O 密集型任务（如网络请求、文件读写，因为 I/O 阻塞时会释放 GIL）。
- 对于 CPU 密集型任务，应使用**多进程**来利用多核 CPU。

### 11.3 多线程
使用 `threading` 模块处理 I/O 密集型任务。
```python
import threading
import time

def worker(id):
    print(f"线程 {id} 开始工作...")
    time.sleep(2)  # 模拟 I/O 操作
    print(f"线程 {id} 完成.")

# 创建线程
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("所有线程执行完毕")
```

### 11.4 多进程
使用 `multiprocessing` 模块处理 CPU 密集型任务。
```python
import multiprocessing
import os

def cpu_heavy_task(id):
    print(f"进程 {id} 启动, PID: {os.getpid()}")
    total = 0
    for i in range(10**7): # 模拟大量计算
        total += i
    print(f"进程 {id} 计算完成")

if __name__ == '__main__': # 多进程必须在 __main__ 保护下运行
    processes = []
    for i in range(2):
        p = multiprocessing.Process(target=cpu_heavy_task, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("所有进程执行完毕")
```

### 11.5 线程池与进程池
实际开发中，推荐使用 `concurrent.futures` 模块提供的线程池/进程池，更易于管理。
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 线程池 (适合 I/O 密集型)
with ThreadPoolExecutor(max_workers=5) as executor:
    # executor.map(function, iterable)
    pass

# 进程池 (适合 CPU 密集型)
with ProcessPoolExecutor(max_workers=4) as executor:
    pass
```

### 11.6 进程间通信 (IPC) 与 线程安全
- **线程间通信**：因为线程共享内存，可以直接读写同一变量。但这会引发**线程安全**问题（数据竞争），因此需要加锁 `threading.Lock()`。
- **进程间通信**：进程间内存独立，需要使用 `multiprocessing.Queue` 或 `Pipe` 来传递数据。
```python
# 线程锁示例
import threading

lock = threading.Lock()
counter = 0

def safe_increment():
    global counter
    with lock: # 获取锁，执行完后自动释放
        temp = counter
        temp += 1
        counter = temp
```
非常好的问题！一份全面的 Python 学习笔记，除了语法和底层原理，还应该涵盖**语言特性进阶、现代并发模型、常用标准库以及工程化开发**的知识。

经过仔细复盘，我为你梳理了以下 **5 个遗漏的重要模块**。你可以继续将它们追加到笔记的末尾：

```markdown
---

## 12. 类型与内存进阶

### 12.1 可变与不可变类型
这是 Python 中极其重要且容易踩坑的概念。
- **不可变类型**：数字、字符串、元组。修改它们的值实际上是在堆区创建了一个新对象，栈上的引用指向新对象。
- **可变类型**：列表、字典、集合。修改它们的值（如 `append`），堆上的对象本身发生变化，引用地址不变。
```python
def modify_list(lst):
    lst.append(4)  # 修改了堆上的原对象

def modify_int(x):
    x = x + 1      # 在堆上新建了一个整数对象，局部变量 x 指向新对象

my_list = [1, 2, 3]
modify_list(my_list)
print(my_list)  # [1, 2, 3, 4] (被改变)

my_int = 10
modify_int(my_int)
print(my_int)  # 10 (未改变)
```

### 12.2 深浅拷贝
针对可变类型的嵌套结构，需要特别注意拷贝的深度。
```python
import copy
list_a = [[1, 2], [3, 4]]

# 赋值：只拷贝引用，完全指向同一个对象
b = list_a  

# 浅拷贝：只拷贝最外层，内层嵌套对象仍共享引用
c = copy.copy(list_a) 
c[0][0] = 99  # 会影响 list_a

# 深拷贝：递归拷贝所有层级，完全独立的新对象
d = copy.deepcopy(list_a)
d[0][0] = 100 # 不会影响 list_a
```

### 12.3 类型提示
Python 3.5+ 引入，不强制执行，但极大地提高了代码可读性和 IDE 智能提示。
```python
from typing import List, Dict, Optional

def process_data(items: List[int], config: Dict[str, str]) -> Optional[str]:
    if not items:
        return None
    return "Success"
```

---

## 13. 面向对象进阶

### 13.1 魔术方法
以双下划线开头和结尾的方法，定义了对象的行为。
```python
class MyVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 定义 print() 时的显示内容
    def __repr__(self):
        return f"MyVector({self.x}, {self.y})"

    # 定义加法运算符 +
    def __add__(self, other):
        return MyVector(self.x + other.x, self.y + other.y)

v1 = MyVector(1, 2)
v2 = MyVector(3, 4)
print(v1 + v2)  # MyVector(4, 6)
```

### 13.2 类方法与静态方法
```python
class Date:
    def __init__(self, year, month, day):
        self.year = year

    # 类方法：接收 cls 作为第一个参数，常用于定义工厂方法
    @classmethod
    def from_string(cls, date_str):
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day) # 实例化类

    # 静态方法：既不接收 self 也不接收 cls，通常作为工具函数
    @staticmethod
    def is_valid_date(date_str):
        # 校验逻辑...
        return True
```

### 13.3 属性装饰器
将方法伪装成属性进行访问，可以在获取或设置值时加入逻辑校验。
```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("名字必须是字符串")
        self._name = value

p = Person("Alice")
p.name = "Bob"  # 像属性一样赋值，但会触发 setter 校验
```

---

## 14. 现代并发编程：Asyncio

在多线程之外，Python 3.5+ 引入了 `asyncio`，用于单线程内的**异步 I/O 并发**。它比多线程更轻量，是现代 Python 网络爬虫、Web 框架（如 FastAPI）的核心。

```python
import asyncio
import time

async def fetch_data(id):
    print(f"开始获取数据 {id}...")
    # 模拟网络请求耗时，遇到 await 会交出控制权
    await asyncio.sleep(2)
    print(f"数据 {id} 获取完毕")
    return f"Data_{id}"

async def main():
    start = time.time()
    # 并发执行多个协程任务
    tasks = [fetch_data(i) for i in range(3)]
    # asyncio.gather 会等待所有任务完成
    results = await asyncio.gather(*tasks)
    print(f"结果: {results}, 耗时: {time.time() - start:.2f}s")

# 运行异步入口函数
asyncio.run(main())
# 输出总耗时约 2s，而不是 6s
```

---

## 15. 常用标准库与数据序列化

### 15.1 JSON 处理
Python 与外部系统交互（如 API、配置文件）最常用的格式。
```python
import json

data = {"name": "Alice", "age": 30, "scores": [90, 85]}

# 字典转 JSON 字符串 (序列化)
json_str = json.dumps(data, ensure_ascii=False) # 处理中文
print(json_str)

# JSON 字符串转字典 (反序列化)
parsed_data = json.loads(json_str)
```

### 15.2 Collections 模块
扩展了内建数据结构，非常实用。
```python
from collections import Counter, defaultdict, namedtuple

# 1. Counter: 计数器
words = ['apple', 'banana', 'apple', 'orange']
word_counts = Counter(words)
print(word_counts.most_common(1)) # [('apple', 2)]

# 2. defaultdict: 带默认值的字典 (避免 KeyError)
dd = defaultdict(list)
dd['fruits'].append('apple') # 即使 'fruits' 键不存在也不会报错

# 3. namedtuple: 可命名元组 (像对象一样访问的轻量级结构)
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, y=20)
print(p.x, p.y)
```

### 15.3 日期时间处理
```python
from datetime import datetime, timedelta

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S")) # 格式化输出

tomorrow = now + timedelta(days=1) # 时间加减
```

---

## 16. 工程化与测试

### 16.1 虚拟环境与依赖管理
在真实开发中，每个项目的依赖包应该相互隔离。
```bash
# Python 内置方案
python -m venv myenv       # 创建虚拟环境
source myenv/bin/activate  # 激活
pip freeze > requirements.txt # 导出依赖
pip install -r requirements.txt # 安装依赖

# 现代方案推荐 (更快速、更强大):
# uv, poetry, pipenv
```

### 16.2 单元测试
使用 `pytest` 是 Python 社区测试的标准做法。
```python
# 文件名: test_math.py
def add(a, b):
    return a + b

# 测试函数必须以 test_ 开头
def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
```
在终端运行 `pytest test_math.py` 即可执行测试。

---



