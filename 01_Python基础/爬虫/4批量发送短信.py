import re
from io import BytesIO
import requests
from PIL import Image

from pytesseract import pytesseract


def get_code_text():
    r = session.get(url=img_url)
    img = Image.open(BytesIO(r.content))
    if is_save:
        img.save("D:\\data\\code{}.PNG".format(mobile_no))
    image = img.convert('L')
    if is_save:
        image.save("D:\\data\\code_black{}.PNG".format(mobile_no))
    pixels = image.load()
    # 【二值化】阀值：standard
    standard1, standard2 = (100, 170)
    # 【描边邻域降噪】阀值：standard
    for x in range(image.width):
        for y in range(image.height):
            if x >= image.width - 1 or y >= image.height - 1:
                # 边缘过滤
                pixels[x, y] = 255
            elif pixels[x, y] < standard2 and pixels[x + 1, y] < standard2 and pixels[x, y + 1] < standard2:
                # 深色并且粗线保留
                # 浅色加深
                pixels[x, y] = 0
            else:
                # 细线过滤
                pixels[x, y] = 255
    if is_save:
        image.save("D:\\data\\code_scan{}.PNG".format(mobile_no))
    testdata_dir_config = '--tessdata-dir "D:/Program Files (x86)/Tesseract-OCR/tessdata"'
    text_code = pytesseract.image_to_string(image, lang='eng', config=testdata_dir_config)
    # 去掉非法字符，只保留字母数字
    return re.sub("\W", "", text_code)


def send_msg():
    mobile_params['imgVcode'] = text_code
    mobile_params['mobile'] = mobile_no
    r = session.post(mobile_url, params=mobile_params, timeout=10000)
    return r.text.strip()


if __name__ == '__main__':
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'google.jinhui365.cn',
               'Origin': 'http://google.jinhui365.cn',
               'Referer': 'http://google.jinhui365.cn/register/index',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    img_url = "http://google.jinhui365.cn/kaptcha?action=kaptcha_register&32"
    mobile_url = "http://google.jinhui365.cn/vcode/mobile"
    mobile_params = {'mobile': '11120190203',
                     'type': 'register',
                     'is_web_a': '2020',
                     'imgVcode': 'dhc8to',
                     'isCheckDup': 'true',
                     'isImgVcode': '1'}
    mobile_base = 11120200001
    is_save = True
    session = requests.Session()
    session.headers = headers
    for i in range(10):
        mobile_no = mobile_base + i
        text_code = get_code_text()
        result = send_msg()
        print(mobile_no, text_code, result)
