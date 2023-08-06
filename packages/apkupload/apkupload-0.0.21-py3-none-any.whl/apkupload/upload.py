import configargparse
import base64
import hashlib
import hmac
import json
import os
import requests
import time
import urllib.parse
from datetime import datetime
from androguard.core.bytecodes.apk import APK
# 解析输入的参数

content_template = """
{apk_info}
* 更新说明：
{changelog}
* 历史版本：[戳这里]({url})
![图片]({image})
"""

apk_info_template = """
* 应用名称：{name}
* 应用包名：{package}
* 版本名称：[{version_name}]({download_url})
* 版本号：{version_code}
* MD5：{md5}
* 包大小：{size}
----------------------------
"""


def parse():
    p = configargparse.ArgParser(
        config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.add('--config', required=True, is_config_file=True)
    p.add('--version_code', required=False)
    p.add('--version_code_suffix', required=False)
    p.add('--version_name', required=False, nargs="+")
    p.add('--delete', required=False)
    p.add('--send', required=False)
    p.add('--name', required=False)
    p.add('--base', required=True)
    p.add('--input', required=False)
    p.add('--output', required=False)
    p.add('--key', required=False)
    p.add('--password', required=False)
    p.add('--url', required=True)
    p.add('--upload_url', required=True)
    p.add('--secret', required=True)
    p.add('--token', required=True)
    p.add('--user', required=True)
    p.add('--repository', required=True)
    p.add('--github', required=True)
    p.add('--workflow', required=True, )
    p.add('--changelog', required=True, nargs="+")
    p.add('--at', required=True, nargs="+")
    p.add('--image', required=True)
    p.add('--retry_count', required=True, type=int)
    p.add('--apks',  required=False, nargs="+")
    p.add('--protect_enable',  required=False)
    p.add('--protect_base_url', required=False)
    p.add('--protect_app_secret', required=False)
    p.add('--protect_app_key', required=False)
    p.add('--protect_username', required=False)
    p.add('--protect_password', required=False)
    return p.parse_args()


def rename_apk_name(apk_info, apk):
    """重新命名文件"""
    name = apk_info.get("name")
    version_name = apk_info.get("version_name")
    dir = os.path.dirname(apk)
    now = datetime.strftime(datetime.now(), "%m_%d_%H%M")
    new_apk = f"{dir}/{name}_{version_name}_{now}.apk"
    os.makedirs(dir, exist_ok=True)
    os.rename(apk, new_apk)
    return new_apk


def build_json(changelog, base, path, download_url, apk_info):
    return {
        "name": apk_info.get("name"),
        "version_name": apk_info.get("version_name"),
        "version_code": apk_info.get("version_code"),
        "url": download_url,
        "date": datetime.now().strftime("%Y-%m-%d %H时%M分%S秒"),
        "changelog": changelog,
        "md5": apk_info.get("md5"),
        "size": apk_info.get("size"),
        "file": path,
        "base": base,
        "package": apk_info.get("package")
    }


def build_web(user, repository, workflow, headers, content):
    print(">>>> build web <<<<")
    body = {"ref": "main", "inputs": {"content": json.dumps(content)}}
    r = requests.post(
        f"https://api.github.com/repos/{user}/{repository}/actions/workflows/{workflow}/dispatches",
        headers=headers,
        json=body
    )
    print(r.status_code)


def change_version(input, version_code, version_name, version_code_suffix):
    """修改版本号"""
    print(">>>> change version <<<<")
    if (version_code_suffix == "True"):
        suffix = version_name.split("_")[0].split(".")[-1]
        version_code = f"{version_code}{suffix}"
    result = ""
    with open(input + "/apktool.yml", 'r') as f:
        lines = f.readlines()
        for line in lines[:-2]:
            result += line
        result += "  versionCode: '{version_code}'\n".format(
            version_code=version_code)
        result += "  versionName: " + version_name
    with open(input + "/apktool.yml", "w") as f:
        f.write(result)


def build_apk(output, input, key, password):
    """打包"""
    unalign = output + "/unalign.apk"
    unsign = output + "/unsign.apk"
    sign = output + "/sign.apk"
    print(">>>> building apk <<<<")
    os.system(
        'apktool b -o {unalign} {decode}'.format(unalign=unalign, decode=input))
    print(">>>> aligning apk <<<<")
    os.system(
        'zipalign -f 4 {unalign} {unsign}'.format(unalign=unalign, unsign=unsign))
    print(">>>> signing apk <<<<")
    os.system('apksigner sign --ks {key} --ks-pass pass:{password} --out {sign} {unsign}'.format(
        key=key, password=password, sign=sign, unsign=unsign))
    return sign


def sign(unsign, key, password):
    sign_apk = unsign[0:-4]+"_sign.apk"
    print(sign_apk)
    os.system('apksigner sign --ks {key} --ks-pass pass:{password} --out {sign} {unsign}'.format(
        key=key, password=password, sign=sign_apk, unsign=unsign))
    return sign_apk


def get_apk_info(name, apk):
    """获取apk信息"""
    md5 = hashlib.md5(open(apk, 'rb').read()).hexdigest()
    size = str(os.path.getsize(apk))+"字节"
    apk = APK(apk)
    if (name == None):
        name = apk.get_app_name()
    package = apk.get_package()
    version_name = apk.get_androidversion_name()
    version_code = apk.get_androidversion_code()
    return {"md5": md5, "size": size, "name": name, "package": package, "version_name": version_name, "version_code": version_code}


def send_to_dingding(url, changelog, apk_info_list, secret, token, at, image):
    print(">>>> send to dingding <<<<")
    apk_info = ""
    for item in apk_info_list:
        apk_info += apk_info_template.format(name=item.get("name"), download_url=item.get("download_url"),
                                             md5=item.get("md5"), package=item.get("package"), version_name=item.get("version_name"), version_code=item.get("version_code"), size=item.get("size"))
    content = content_template.format(
        changelog=changelog, apk_info=apk_info, url=url, image=image)
    atMobiles = []
    for i in at:
        atMobiles.append(i)
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url2 = f'https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp=' + \
        timestamp + '&sign=' + sign
    h = {'Content-Type': 'application/json; charset=utf-8'}
    body = {"at": {"isAtAll": True},
            "msgtype": "markdown", "markdown": {"text": content, "title": "更新日志"}
            }
    r = requests.post(url2, headers=h, data=json.dumps(body))


def upload(upload_url, file, count, retry_count, delete):
    print(">>>> uploading <<<<")
    count += 1
    files = {'file': open(file, 'rb')}
    response = requests.post(upload_url, files=files)
    url = ""
    print(response.status_code)
    if (response.status_code == 200 or response.status_code == 201):
        url = response.json()["data"]
        print(f">>>>上传成功<<<< url = {url}")
        if delete=="True":
            os.remove(file)
    else:
        print(
            f">>>>上传失败 code = {response.status_code} message = {response.json()} count = {count}<<<")
        if (count < retry_count):
            url = upload(upload_url, file, count, retry_count, delete)
    return url


HEX_CHARS = '0123456789abcdef'


def get_sign(src, key):
    mac = hmac.new(key.encode('utf-8'), src.encode('utf-8'), hashlib.sha1)
    result = mac.digest()

    hex_chars = []
    for b in result:
        bite = b & 0xff
        hex_chars.append(HEX_CHARS[bite >> 4])
        hex_chars.append(HEX_CHARS[bite & 0xf])

    return ''.join(hex_chars)


def upload_protect(base_url, api_key, api_secret, password, username, apk_file):
    """上传文件"""
    print(">>>> upload_protect <<<<")
    url = f"{base_url}/webbox/v5/protect/upload"
    policy_id = "2"
    upload_type = "2"
    src = api_key+password+policy_id+upload_type+username
    sign = get_sign(src, api_secret)
    files = {'apk_file': open(apk_file, 'rb')}
    data = {'username': username, "password": password,
            "policy_id": policy_id, "upload_type": upload_type}
    headers = {"api_key": api_key, "sign": sign}
    response = requests.post(url, files=files, data=data, headers=headers)
    print(response.json())
    if response.status_code == 200 and response.json().get("code") == 0:
        return get_status(base_url, api_key, api_secret, password, username, response.json().get("info").get("id"), apk_file)
    else:
        return None


code_dict = {
    9001: "应用加固排队中",
    9002: "应用加固中",
    9008: "应用加固失败",
    9009: "应用加固成功",
}


def get_status(base_url, api_key, api_secret, password, username, apkInfo_id, apk):
    time.sleep(10)
    url = f"{base_url}/webbox/v5/protect/get_state"
    src = api_key+str(apkInfo_id)+password+username
    sign = get_sign(src, api_secret)
    data = {'username': username, "password": password, "apkinfo_id": apkInfo_id}
    headers = {"api_key": api_key, "sign": sign}
    response = requests.post(url, data=data, headers=headers)
    # 检查响应状态码
    if response.status_code == 200 and response.json().get("code") == 0:
        code = response.json().get("info").get("status_code")
        print(code_dict.get(code))
        if code == 9009:
            return download(base_url, api_key, api_secret, apkInfo_id, apk)
        elif code == 9008:
            return None
        else:
            return get_status(base_url, api_key, api_secret, password, username, apkInfo_id, apk)
    else:
        return None


def download(base_url, api_key, api_secret, apkInfo_id, apk):
    print("开始下载...")
    url = f"{base_url}/webbox/v5/protect/download"
    apk = apk[0:-4]+"_sec.apk"
    download_type = "1"
    src = api_key+str(apkInfo_id)+download_type
    sign = get_sign(src, api_secret)
    data = {"apkinfo_id": apkInfo_id, "download_type": download_type}
    headers = {"api_key": api_key, "sign": sign}
    response = requests.post(url, data=data, headers=headers)
    # 检查响应状态码
    if response.status_code == 200:
        print("文件下载成功！")
        with open(apk, 'wb') as file:
            file.write(response.content)
        return apk
    else:
        print("文件上传失败！")
        return None


def main():
    args = parse()
    version_code_suffix = args.version_code_suffix
    version_name_list = args.version_name
    version_code = args.version_code
    base = args.base
    send = args.send
    name = args.name
    delete = args.delete
    input = args.input
    output = args.output
    key = args.key
    password = args.password
    secret = args.secret
    url = args.url
    upload_url = args.upload_url
    token = args.token
    changelog = args.changelog
    changelog = [f"> - {item}" for item in changelog]
    changelog = "\n".join(changelog)
    github = args.github
    workflow = args.workflow
    at = args.at
    user = args.user
    repository = args.repository
    image = args.image
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"token {github}"}
    retry_count = args.retry_count
    apks = args.apks
    protect_enable = args.protect_enable
    protect_base_url = args.protect_base_url
    protect_app_secret = args.protect_app_secret
    protect_app_key = args.protect_app_key
    protect_username = args.protect_username
    protect_password = args.protect_password
    if delete == "True":
        os.system(f"rm -rf {output}")
    apk_info_list = []
    content = []
    if apks != None:
        for apk in apks:
            apk_info = get_apk_info(name, apk)
            apk = rename_apk_name(apk_info, apk)
            if protect_enable == "True":
                sec_apk = upload_protect(protect_base_url, protect_app_key,
                                        protect_app_secret, protect_password, protect_username, apk)
                if sec_apk != None:
                    apk = sec_apk
                    apk = sign(apk, key, password)
            #重新计算一次md5
            apk_info = get_apk_info(name, apk)
            download_url = upload(upload_url, apk, 0, retry_count, delete)
            apk_info["download_url"] = download_url
            path = datetime.now().strftime("%Y%m%d%H%M")
            content.append(build_json(changelog, base,
                        path, download_url, apk_info))
            apk_info_list.append(apk_info) 
    else:
        for version_name in version_name_list:
            change_version(input, version_code, version_name, version_code_suffix)
            apk = build_apk(output, input, key, password)
            apk_info = get_apk_info(name, apk)
            apk = rename_apk_name(apk_info, apk)
            if protect_enable == "True":
                sec_apk = upload_protect(protect_base_url, protect_app_key,
                                        protect_app_secret, protect_password, protect_username, apk)
                if sec_apk != None:
                    apk = sec_apk
                    apk = sign(apk, key, password)
            #重新计算一次md5
            apk_info = get_apk_info(name, apk)
            download_url = upload(upload_url, apk, 0, retry_count, delete)
            apk_info["download_url"] = download_url
            path = datetime.now().strftime("%Y%m%d%H%M")
            content.append(build_json(changelog, base,
                        path, download_url, apk_info))
            apk_info_list.append(apk_info)
    build_web(user, repository, workflow, headers, content)
    if send == "True":
        send_to_dingding(url, changelog, apk_info_list,
                         secret, token, at, image)


if __name__ == "__main__":
    main()
