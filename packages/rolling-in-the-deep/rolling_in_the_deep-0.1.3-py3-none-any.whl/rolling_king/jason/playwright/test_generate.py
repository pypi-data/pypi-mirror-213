from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("Chatgpt")
    page.locator("#kw").press("Enter")
    page.locator("body").press("Enter")
    page.get_by_role("link", name=" 资讯").click()

    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="chatgpt，OpenAI发布的聊天机器人模型，百度百科").click()
    page1 = page1_info.value
    # ---------------------
    context.close()
    browser.close()


def generate_measure_platform(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://measure.csleasing.com.cn/")
    page.goto("https://measure.csleasing.com.cn/#/")
    page.goto("https://measure.csleasing.com.cn/#/login?redirect=/dashboard/analysis/analysis")
    page.get_by_placeholder("账号").dblclick()
    page.get_by_placeholder("账号").click()
    page.get_by_placeholder("账号").fill("zhengyu")
    page.get_by_placeholder("账号").press("Tab")
    page.get_by_placeholder("密码").fill("Jason1qaz!QAZ")
    page.pause()  # pause相当于断点调试，可模拟暂停。在弹出的录制窗体中点击Resume按钮即可继续自动化执行。
    page.get_by_role("button", name="登 录").click()
    page.pause()
    page.get_by_text("单一指标库").click()
    page.get_by_text("人员产能").click()
    page.wait_for_timeout(5000)  # 显示等待5s
    page.get_by_text("人员出勤报表").click()

    # ---------------------
    context.storage_state(path="auth.json")  # 录制的cookies、LocalStorage等信息存入指定文件。
    # 录制命令为：playwright codegen measure.csleasing.com.cn --save-storage=auth.json
    context.close()
    browser.close()


def simulate_post_situation(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth.json")  # 从auth.json中读取登录态，然后直接开始登录后的操作即可。
    # 若使用录制，则命令为：playwright codegen --load-storage=auth.json measure.csleasing.com.cn
    page = context.new_page()
    page.goto("https://measure.csleasing.com.cn/")
    page.goto("https://measure.csleasing.com.cn/#/")
    page.goto("https://measure.csleasing.com.cn/#/dashboard/analysis/analysis")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    generate_measure_platform(playwright)
