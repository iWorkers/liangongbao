# lgb登录账号,
# 2022年为账号密码 {'USER': 'USER', 'PWD': 'PWD'}
# 2023年为微信登录获取的tokenid {'memberId': 'memberId', 'token': 'token'}
ACCOUNT = [
    {'memberId': 'memberId', 'token': 'token'},
]

# 仅查询用户信息不进入答题：积分，抽奖信息等值为'True'，进入答题为'False'
ONLY_QUERYINFO = True
# 查询到的用户信息写入文件值默认为'True',不写入为'False'
QUERYINFO_WRITE_FILE = True
QUERYINFO_WRITE_FILE_PATH = 'user_info.txt'

# 是否自动抽奖，自动抽奖失去快乐,是为'True', 否为'False'
AUTO_LOTTERY = False
# 终端二维码显示乱码将此项设置为'True'弹出二维码扫描框, 不弹出二维码扫描框为'False'，也可以使用浏览器点击二维码下的链接
SHOW_WECHAT_QRCODE = True

# winodws文件夹分隔符 '\' unix 文件夹分隔符 '/'，可以给绝对路径
# Excel 题库
EXCEL_QUESTION_BANK_PATH = r'question_bank\2022_6_21.xls'
# TXT 题库
ANSWER_QUESTION_BANK_PATH = r'question_bank\2023_answers.txt'
# 文章 题库
PAPER_QUESTION_BANK_PATH = r'question_bank\2022_wenzhang.txt'
# 题库匹配优先级
QUESTION_BANK_PRIORITY = [ANSWER_QUESTION_BANK_PATH, EXCEL_QUESTION_BANK_PATH]
# 错题收集本
WRONG_QUESTIONS_PATH = r'question_bank\wrong_questions.txt'

# 随机答对题数,默认全部作答,给定值大于答题数目即可
# import random;CORRECT_ANSWER_NUM = random.randint(11,16)  #随机取消注释
# CORRECT_ANSWER_NUM = 15   # 指定确定作答数目
CORRECT_ANSWER_NUM = 9999

# 不自动安装chrome请设置这个参数
# CHROME_CHROME_PATH = r'.wdm\drivers\chromedriver\win32\x.x.x\chromedriver.exe'
CHROME_CHROME_PATH = None
CHROME_TIMEOUT = 15

# adb devices 命令得到的手机序列号
ADB_DEVICE_SERIAL = "xxxxxxxx"

# 保护官网请求频率，设置随机请求时间
# 最大间隔请求时间
MAX_TIME = 3
# 最小间隔请求时间
MIN_TIME = 1

# 软件版本
RE_VERSION = '2023.06.04.11.00'
