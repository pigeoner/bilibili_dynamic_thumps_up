import requests
import json
import re
import logging
from time import sleep

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class DynamicLike:
    def __init__(self, cookie: str, host_uid: str, interval: int = 2):
        """
        :param cookie: 自己的B站cookie
        :param host_uid: 需要点赞的用户的B站UID
        """
        self._cookie = cookie
        self._host_uid = host_uid
        self._user_id = re.search(
            r'DedeUserID=(\d+)', cookie).group(1).strip()
        self._csrf = re.search(
            r"bili_jct=([0-9a-zA-Z]{32})", cookie).group(1).strip()
        self._dlst_url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={self._host_uid}&need_top=1&platform=web&offset_dynamic_id="
        self._like_url = "https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb"
        self._headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            "Referer": f"https://space.bilibili.com/{self._host_uid}/dynamic",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "Cookie": cookie,
        }
        self._interval = interval

    def _get(self, url: str):
        r = requests.get(url, headers=self._headers)
        if r.status_code == 200:
            res = json.loads(r.text)
            if res['code'] != 0:
                raise Exception(res['msg'])
        else:
            raise Exception('get请求出错，返回状态码为{}'.format(r.status_code))
        return res

    def _post(self, url: str, data: dict, headers: dict):
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == 200:
            res = json.loads(r.text)
            if res['code'] != 0:
                logging.error(f"给动态{data['dynamic_id']}点赞失败，错误信息：{res['msg']}")
        else:
            raise Exception('post请求出错，返回状态码为{}'.format(r.status_code))
        return res

    def get_unliked_dynamic_lst(self):
        """
        获取所有未点赞的动态
        """
        has_more = 1
        dynamic_lst = []
        offset_dynamic_id = 0
        while has_more:
            url = self._dlst_url + str(offset_dynamic_id)
            res = self._get(url)
            has_more = res['data']['has_more']
            if not has_more:
                break
            dynamic_lst += [e['desc']['dynamic_id_str']
                            for e in res['data']['cards'] if not e['desc']['is_liked']]
            offset_dynamic_id = res['data']['cards'][-1]['desc']['dynamic_id_str']
        return dynamic_lst

    def like(self):
        """
        给指定用户的所有未点赞动态点赞
        """
        print('--------------------开始收集--------------------')
        print(f'正在收集用户 {self._host_uid} 的全部未点赞动态...')
        dynamic_lst = self.get_unliked_dynamic_lst()
        print(f'全部未点赞动态收集完毕，共 {len(dynamic_lst)} 个。')
        print('--------------------开始点赞--------------------')
        data = {
            "uid": self._host_uid,
            "dynamic_id": "",
            "up": 1,
            "csrf_token": self._csrf,
            "csrf": self._csrf,
        }
        for i, d in enumerate(dynamic_lst):
            data['dynamic_id'] = d
            self._post(self._like_url, data, self._headers)
            logging.info(
                f'给用户 {self._host_uid} 的动态 {d} 点赞完毕（{i+1}/{len(dynamic_lst)}）')
            sleep(self._interval)
        print(f'用户 {self._host_uid} 的全部动态点赞完毕')


if __name__ == '__main__':

    cookie = ""  # 这里填写自己的B站cookie

    host_id = ""  # 这里填写需要点赞的用户的B站UID

    interval = 2  # 这里填写点赞时间间隔，默认为2秒

    dlike = DynamicLike(cookie, host_id, interval)

    dlike.like()
