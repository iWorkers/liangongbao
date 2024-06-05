import copy
import time
from io import BytesIO
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
from http_utils import HTTPClient
from url_conf import URLS
from LgbConfig import SHOW_WECHAT_QRCODE
import requests

def get_tok_uid():
    http_client = HTTPClient()
    res_text = http_client.send(URLS['wexin_request_qrcode'])
    assert isinstance(res_text, str), "错误：" + URLS['wexin_request_qrcode']
    key_str = '<img class="web_qrcode_img" src="/'
    idx = res_text.find(key_str)
    assert idx != -1, "没有找到微信提供的二维码图片"

    qrcode_href = res_text[idx:idx+70].split('"')[3]
    qrcode_uuid = qrcode_href.split('/')[-1]
    # print(qrcode_href, qrcode_uuid)

    qrcode_url = copy.deepcopy(URLS['wexin_request_uuid'])
    qrcode_url['req_url'] += qrcode_href

    res_content = http_client.send(qrcode_url)
    assert isinstance(res_text, str), "错误：" + qrcode_url
    image = Image.open(BytesIO(res_content))
    barcodes = decode(image)
    for barcode in barcodes:
        barcode_url = barcode.data.decode("utf-8")
    qr = qrcode.QRCode()
    barcode_url = URLS['wexin_confirm_request_uuid']['req_url'] + qrcode_uuid
    qr.add_data(barcode_url)
    #qr.print_ascii(invert=True)
    #print(qrcode_url['req_url'])
    if SHOW_WECHAT_QRCODE:
        img = qr.make_image()
        img.show()
    
    scan_qrcode_sucess = False
    wexin_poll_confirm_request_uuid_url = copy.deepcopy(URLS['wexin_poll_confirm_request_uuid'])
    for _ in range(100):
        time.sleep(1)
        current_milli_time = lambda: str(int(round(time.time() * 1000)))
        wexin_poll_confirm_request_uuid_url['req_url'] += qrcode_uuid + '&_=' + current_milli_time()
        res_text = http_client.send(wexin_poll_confirm_request_uuid_url)
        if not isinstance(res_text, str): continue
        res = res_text.find('window.wx_errcode=405;window.wx_code=')
        if res == -1:
            continue

        scan_qrcode_sucess = True
        wx_code = res_text.split('=')[-1]
        wx_code = wx_code.replace('\'', '')
        wx_code = wx_code.replace(';', '')
        break
    assert scan_qrcode_sucess, "微信扫码超时,退出登录"

    get_log2023_uid_tok_url = copy.deepcopy(URLS['lgb2023_login'])
    get_log2023_uid_tok_url['req_url'] += wx_code + get_log2023_uid_tok_url['req_url_suffix']
    token_dict = http_client.send(get_log2023_uid_tok_url)
    status = token_dict.get("status")
    if status == 20000 and 'data' in token_dict:
        token = token_dict.get("data").get("uidtok")
        memberId = token_dict.get("data").get("unionId")
        #cookie='acw_tc='+requests.utils.dict_from_cookiejar(http_client.get_cookies())['acw_tc']
        cookie=requests.utils.dict_from_cookiejar(http_client.get_cookies())
        cookie_string = "; ".join([f"{name}={value}" for name, value in requests.utils.cookiejar_from_dict(cookie).items()])+"; "
        user_info = {'memberId': memberId, 'token': token, 'cookie': cookie_string}
        print("微信登录LGBtoken:", user_info)
        print("登录成功")
        #print(cookie_string)
        
        return memberId, token,cookie_string
    print(token_dict)
    print("登录失败")
    return 'memberId', 'token'
