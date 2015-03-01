__author__ = 'wuwy'

import requests
import re
import os
import json
import zhihuSpider.model
import urllib
import zhihuSpider.config


class Spider:
    def __init__(self):
        self.login_url = "http://www.zhihu.com/#signin"
        self.commit_url = "http://www.zhihu.com/login"

        self.login_username = zhihuSpider.config.login_username
        self.login_password = zhihuSpider.config.login_password

        self.seed_user = zhihuSpider.config.seed_user_url

        self.layer = zhihuSpider.config.layer
        self.spider = requests.session()

    def login(self):
        r = self.spider.get(self.login_url)
        _xsrf = re.findall(r"name=\"_xsrf\" value=\"(\w*)\"", str(r.text))[0]
        form_date = {'_xsrf': str(_xsrf), 'email': str(self.login_username), 'password': str(self.login_password),
                     'rememberme': 'y'}
        self.spider.post(self.commit_url, data=form_date)

    def creep(self, seed_user_url):
        flowers_url = seed_user_url + "/followers"
        html = self.spider.get(flowers_url)
        _xsrf = re.findall(r"name=\"_xsrf\" value=\"(\w*)\"", str(html.text))[0]
        hash_id = re.findall(r"data-id=\"(\w+)\"", str(html.text))[0]
        flowers_size = int(re.findall(r"被 (\d+) 人关注", str(html.text))[0])
        count = 0

        while True:
            params = json.dumps({"offset": count, "order_by": "created", "hash_id": hash_id})
            date = {'method': 'next', 'params': params, '_xsrf': _xsrf}
            headers = {'Referer': flowers_url, 'Host': 'www.zhihu.com', 'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0"}
            response = self.spider.post('http://www.zhihu.com/node/ProfileFollowersListV2', data=date, headers=headers)
            self.json_to_user(response.json()['msg'], True, False)
            if count > 50: return
            count += 20

    def json_to_user(self, msg, detailed, download):
        list = []
        for u in msg:
            nu = zhihuSpider.model.User()
            title_and_url = re.findall(r'<h2.+</h2>', str(u))
            nu.user_name = re.findall(r'title=\"(.+)\">', str(title_and_url))[0]
            nu.url = re.findall(r'href=\"(.+)\" c', str(title_and_url))[0]
            nu.answer_count = re.findall(r'(\d+) 回答', str(u))[0]
            nu.flower_count = re.findall(r'(\d+) 关注者', str(u))[0]
            nu.agree = re.findall(r'(\d+) 赞同', str(u))[0]
            if detailed :
                nu_html = self.spider.get(nu.url+"/about").text
                nu.thanks = re.findall(r'<strong>(\d+)</strong> 感谢', str(nu_html))[0]
                nu.fav = re.findall(r'<strong>(\d+)</strong> 收藏', str(nu_html))[0]
                nu.share = re.findall(r'<strong>(\d+)</strong> 分享', str(nu_html))[0]

                company = re.findall(r'<h3><i class=\"zm-profile-icon zm-profile-icon-company\"></i> '
                            r'<span>职业经历</span></h3>\n.+\n\n.+\n\n.+title="(.*)".+title="(.*)"', str(nu_html))
                if len(company) > 0:
                    nu.company = company[0][0]
                    nu.position = company[0][1]

                location = re.findall(r'<h3><i class=\"zm-profile-icon zm-profile-icon-location\"></i> '
                            r'<span>居住信息</span></h3>\n.+\n\n.+\n\n.+title=\"(.*)\".+title=\".*\"', str(nu_html))
                if len(location) > 0:
                    nu.location = location

                edu = re.findall(r'<h3><i class=\"zm-profile-icon zm-profile-icon-edu\"></i> '
                            r'<span>教育经历</span></h3>\n.+\n\n.+\n\n.+title=\"(.*)\".+title=\"(.*)\"', str(nu_html))
                if len(edu) > 0:
                    nu.school = edu[0][0]
                    nu.major = edu[0][1]

                nu.image_url = re.findall(r'src=\"(.+)\"\nclass=\"zm-profile-header-img zg-avatar-big zm-avatar-editor-preview\"', str(nu_html))[0]
                if download:
                    if nu.image_url != "http://pic1.zhimg.com/da8e974dc_l.jpg":
                        file_name = str(re.findall(r'com/(.+)', str(nu.image_url))[0])
                        nu.img_file = file_name
                        urllib.request.urlretrieve(nu.image_url, os.path.expanduser("~/image/"+file_name))
            list.append(nu)
        return list



if __name__ == "__main__":
    spider = Spider()
    spider.login()
    spider.creep(spider.seed_user)
