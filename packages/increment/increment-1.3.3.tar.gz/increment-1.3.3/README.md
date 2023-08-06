# 项目描述

分布式主键生成器，支持多机器|多进程|多线程并发生成。

# 安装

```
pip install increment
```

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR-max.jpg)、[技术交流群](https://raw.githubusercontent.com/lcctoor/me/main/lccpy/WechatReadersGroupQR-original.jpg) 与我联系。

# 关于作者

作者：许灿标

邮箱：lcctoor@outlook.com

[主页](https://github.com/lcctoor/me#readme) | [微信](https://raw.githubusercontent.com/lcctoor/me/main/author/WeChatQR-max.jpg) | [微信公众号](https://raw.githubusercontent.com/lcctoor/me/main/author/WechatSubscribeQRAndSearch-max.png) | [Python技术交流群](https://raw.githubusercontent.com/lcctoor/me/main/lccpy/WechatReadersGroupQR-original.jpg)

开源项目：[让Python更简单一点](https://github.com/lcctoor/lccpy#readme)

# 教程

#### 导入

```python
from increment import incrementer
```

#### 创建生成器

```python
inc = incrementer()
```

#### 使用创建生成器时的时间

```python
inc.pk1()
# >>> 'lg85x42f_gsdo_258_1'

inc.pk1()
# >>> 'lg85x42f_gsdo_258_2'

# 'lg85x42f'是创建生成器时的时间
```

#### 使用当前时间

```python
inc.pk2()
# >>> 'lg8657cj_gsdo_258_3'

# 'lg8657cj'是当前时间
```

#### 只返回自增主键

```python
inc.pk3()
# >>> '4'

inc.pk3()
# >>> '5'
```

# 支持作者1元

increment 是一个免费的开源项目，由个人维护。

每个小的贡献，都是构成车轮的一份子，可以帮助保持车轮完美旋转。

<img src="https://raw.githubusercontent.com/lcctoor/me/main/donation/donationQR-1rmb-max.jpg" width="200px">
