import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree


class DyPc:
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

    def get_driver(self, url):
        """ 打开页面并去除 Selenium 痕迹 """
        if not url:
            print("❌ 无效的 URL")
            return

        self.driver.get(url)

        # 反反爬：去除 WebDriver 痕迹
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })

    def get_network_responses(self):
        """ 获取抖音 API 响应的 JSON 数据 """
        logs = self.driver.get_log("performance")

        for log in logs:
            log_json = json.loads(log["message"])
            message = log_json["message"]

            if message["method"] == "Network.responseReceived":
                request_id = message["params"]["requestId"]
                response_url = message["params"]["response"]["url"]
                status = message["params"]["response"]["status"]

                if "https://www.douyin.com/aweme/v1/web/aweme/detail" in response_url:
                    print(f"✅ 找到目标 URL: {response_url}, 状态码: {status}")
                    print("~"*200)
                    return response_url  # 返回 API URL


    def run(self, url):
        self.get_driver(url)

        # 等待 5 秒加载页面（可改成 WebDriverWait）
        time.sleep(5)

        # 获取 network 请求信息
        api_url = self.get_network_responses()
        # 打开 API URL 页面（如果找到了）
        if api_url:
            self.get_driver(api_url)
            page_source = self.driver.page_source
            self.analysis_datas(page_source)
        else:
            #TODO 这里在数据库中修改
            print("⚠️ 未找到目标 API 请求")


        # 关闭浏览器
        self.driver.quit()


# 运行程序
# url = "https://www.douyin.com/video/7453366124625874236"
url = "https://www.douyin.com/video/7479251080337984825"
DyPc().run(url)
