# 链工宝自动答题 2024

这是一个用于自动答题链工宝 2023 年活动的 Python 脚本。它可以自动登录、开始答题、提交答案并查询积分和抽奖次数。

## 功能

- 微信扫码登录
- 自动开始答题
- 根据题库自动作答
- 提交答题结果
- 查询当前积分
- 查询抽奖次数
- 自动抽奖

## 使用方法

1. 克隆或下载本仓库到本地。
2. 安装所需的 Python 依赖库,如 `requests`、`Pillow`、`pyzbar` 等。
3. 根据需要修改 `LgbConfig.py` 文件中的配置项。
4. 运行 `main.py` 文件。
5. 根据终端提示进行操作,如扫码登录、选择功能等。

## 配置文件

`LgbConfig.py` 文件包含了一些可配置的选项,如:

- `ACCOUNT`: 登录账号信息
- `SHOW_WECHAT_QRCODE`: 是否显示微信二维码
- `QUESTION_BANK_PRIORITY`: 题库匹配优先级
- `CORRECT_ANSWER_NUM`: 随机答对题数
- `MAX_TIME`、`MIN_TIME`: 请求间隔时间范围

你可以根据需要修改这些配置项。

## 依赖库

- `requests`
- `Pillow`
- `pyzbar`
- ...

## 注意事项

- 本脚本仅供学习和研究使用,请勿用于非法用途。
- 使用本脚本产生的一切后果由使用者自行承担。
- 请尊重链工宝的服务条款和隐私政策。


## 感谢

- @fangyuansisi
<a href="https://github.com/fangyuansisi/liangongbao_help">项目地址</a>
## 贡献

如果你发现任何问题或有改进建议,欢迎提交 issue 或 pull request。

