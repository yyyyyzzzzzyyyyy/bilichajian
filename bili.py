import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


class BilibiliSearchPlugin:
    def __init__(self, driver_path):
        """
        初始化 BilibiliSearchPlugin 类。
        :param driver_path: ChromeDriver 的路径
        """
        self.driver_path = driver_path

    def search_bilibili(self, keyword):
        """
        在 B 站搜索指定关键词，并返回相关视频链接。
        :param keyword: 搜索关键词
        :return: 视频链接列表
        """
        url = f"https://search.bilibili.com/all?keyword={keyword}"
        # 设置 Chrome 浏览器为无头模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        try:
            driver.get(url)
            # 等待页面加载
            time.sleep(5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            video_links = []
            # 查找所有视频链接
            for item in soup.find_all('a'):
                link = item.get('href')
                if link and 'video' in link:
                    if link.startswith('//'):
                        link = 'https:' + link
                    video_links.append(link)
            return video_links
        except Exception as e:
            print(f"请求出错: {e}")
            return []
        finally:
            driver.quit()

    def handle_user_question(self, question):
        """
        处理用户的问题，调用 search_bilibili 方法进行搜索，并返回结果。
        :param question: 用户的问题
        :return: 搜索结果信息
        """
        keyword = question.strip()
        links = self.search_bilibili(keyword)
        if links:
            response = "找到的相关课程链接：\n" + "\n".join(links)
        else:
            response = "未找到相关课程链接。"
        return response
