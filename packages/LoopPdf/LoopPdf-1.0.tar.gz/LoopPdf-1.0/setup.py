import setuptools
from pathlib import Path

# name参数一定不能与其他pipy的包重名
# find_package方法会自动搜索我们定义的模块，传入数组是为了声明排除两个没有源码的文件夹
# readme文件中的内容，将会放在pipy模块的首页
setuptools.setup(
    name="LoopPdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
