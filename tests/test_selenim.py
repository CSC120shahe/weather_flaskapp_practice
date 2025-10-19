# 导入selenium的主接口模块，webdriver是selenium中的核心类库，负责创建浏览器实例（Chrome，Edge，Firefox等）.
# 可以理解为我通过selenium控制一个浏览器。
from selenium import webdriver
# 导入Chrome专用的浏览器服务类。Service()类整合了selenium-manager：会自动检测Chrome版本；自动下载匹配的chromedriver，自动启动服务进程。
# 使用一个自动管理的chromedriver服务。
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC 
import time


# Initialize WebDriver
# 创建一个service对象。没有指定路径，代表启用selenium-manager自动驱动管理器：它会在后台执行如下步骤：
# 1.检查系统中国是否安装了Google Chrome；2.获取当前的Chrome版本号；3.自动下载匹配的chromedriver；
# 4.在缓存目录（例如：～/Library/Caches/selenium/chromedriver/...）中保存；5.启动chromedriver进程。
service = Service()
# 通过这个Service()对象创建Chrome浏览器实例。1.启动后台的chromedriver进程；2.连接到chromedriver；
# 3.chromedriver再启动真实的Chrome浏览器；4. selenium通过WebSocket（DevTools Protocol）控制浏览器。
# 可以理解为启动一个Chrome，并让python代码可以远程控制它。
driver = webdriver.Chrome(service=service)

def test_login_e2e():
    try:
        driver.get("heeps://example.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "dom-username-input"))).send_keys("sasafifelity")
        driver.find_element(By.ID, "dom-pswd-input").send_keys("yourpassword")
        driver.find_element(By.ID, "dom-login-button").click()
        print("Clicked Log in button successfully.")

    except Exception as e:
        print("Login test failed.")

        print(f"Error: {e}")

driver.quit()