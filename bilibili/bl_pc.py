import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree

from methons import dt_s


class BlPc:
    def __init__(self) -> None:
        super().__init__()
        self.driver = self.initialization_driver()

    def analysis_datas(self,page_source):
        tree = etree.HTML(page_source)

        datas = tree.xpath("/html/body/pre/text()")[0]
        data = str(datas)
        data = json.loads(data)
        aweme_detail = data.get("aweme_detail")

        create_time = dt_s(aweme_detail.get("create_time"))
        title = aweme_detail.get("caption")
        statistics = aweme_detail.get("statistics")
        aweme_id = statistics.get("aweme_id")
        author = aweme_detail.get("author")
        nickname = author.get("nickname")
        unique_id = author.get("unique_id")
        platform = "抖音"
        detail = None
        content_url = "https://www.douyin.com/video/" + aweme_id
        playcount = statistics.get("play_count")
        digg_count = statistics.get("digg_count")
        comment_count = statistics.get("comment_count")
        share_count = statistics.get("share_count")
        collect_count = statistics.get("collect_count")
        demu = 0
        note = None
        is_delete = 0

        print(platform)
        print(nickname)
        print(unique_id)
        print(aweme_id)
        print(title)
        print(detail)
        print(create_time)
        print(content_url)
        print(playcount)
        print(digg_count)
        print(comment_count)
        print(share_count)
        print(collect_count)
        print(demu)
        print(note)
        print(is_delete)

    # 初始化窗口
    def initialization_driver(self):
        chrome_path = os.path.join(r"D:/Drive", 'resources', 'chrome', 'chrome.exe')
        driver_path = os.path.join(r"D:/Drive", 'resources', 'chromedriver.exe')

        print(f"Chrome binary path: {chrome_path}")
        print(f"ChromeDriver path: {driver_path}")

        # 设置 ChromeDriver 服务
        driver_service = Service(executable_path=driver_path)

        # 配置 Chrome 选项
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path
        options.add_experimental_option("excludeSwitches", ['enable-automation'])

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")

        # 禁止自动化检测
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")  # 隐身模式
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")

        # 启用 Performance 日志（监听 network 请求）
        caps = DesiredCapabilities.CHROME
        caps["goog:loggingPrefs"] = {"performance": "ALL"}

        # 启动 WebDriver
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # 正确设置 network 日志监听
        driver = webdriver.Chrome(service=driver_service, options=options)

        driver.maximize_window()

        return driver
    # 打开链接
    def get_driver(self, url):
        self.driver.get(url)

        # 反反爬：去除 WebDriver 痕迹
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

    def run(self):
        self.get_driver(url)

        page_source = self.driver.page_source
        print(page_source)






# 运行程序
# url = "https://www.douyin.com/video/7453366124625874236"
# url = "https://www.bilibili.com/video/BV12XADenE8k/"
url = "http://localhost:63342/DBX/bilibili/t1.html?_ijt=4jmllq73q5kn19oulji2oce311&_ij_reload=RELOAD_ON_SAVE"
BlPc().run()
