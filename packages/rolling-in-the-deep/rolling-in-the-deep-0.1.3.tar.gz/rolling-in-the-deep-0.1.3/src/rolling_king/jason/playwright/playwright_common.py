# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# @Time    : 2023/4/12 10:55 上午
# @Author  : zhengyu1
# @FileName: playwright_common.py
# @Software: PyCharm

import enum
from typing import Literal, Optional, Callable

from playwright.sync_api import Playwright, sync_playwright, expect, Page, BrowserContext, Browser, Locator, \
    ElementHandle, Request
import logging

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
logger = logging.getLogger("playwright_common")


class LocatorManner(enum.Enum):
    ROLE = "ROLE"
    TEXT = "TEXT"
    LABEL = "LABEL"
    PLACEHOLDER = "PLACEHOLDER"
    ALT_TEXT = "ALT_TEXT"
    TITLE = "TITLE"
    TEST_ID = "TEST_ID"
    CSS = "CSS-Selector"
    XPATH = "XPATH"

    def info(self):
        print('这是一个元素定位方式为【%s】的枚举' % self.value)


class PlayWrightCommon(object):
    browser: Browser  # 浏览器
    context: BrowserContext  # 上下文
    page: Page  # 页面操作的关键对象。

    @classmethod
    def init(cls,
             playwright: Playwright,
             browser_type: Optional[Literal["webkit", "firefox", "chromium"]] = "chromium",
             **kwargs) -> None:
        """
        初始化Playwright的Page
        :param playwright: 同步或异步的Playwright对象
        :param browser_type: 浏览器类型
        :param kwargs: 其他初始化Browser所需的参数
        :return:
        """
        # 初始化浏览器
        if browser_type == "webkit":
            cls.browser = playwright.webkit.launch(
                headless=kwargs["headless"] if ("headless" in kwargs) else False)
        elif browser_type == "firefox":
            cls.browser = playwright.firefox.launch(
                headless=kwargs["headless"] if ("headless" in kwargs) else False)
        else:
            cls.browser = playwright.chromium.launch(
                headless=kwargs["headless"] if ("headless" in kwargs) else False)
        # 初始化上下文
        cls.context = cls.browser.new_context()
        # 初始化页面
        cls.page = cls.context.new_page()

    @classmethod
    def get_locator(cls, manner: LocatorManner, *args, **kwargs) -> Locator | list[Locator] | None:
        """
        通过多种方式定位元素
        :param manner: 方式枚举
        :param kwargs: 对应方式所需传入的参数
        :return: 单个元素 或 元素列表 或 None
        """
        logger.info(f"定位方式为{manner.name}")
        if manner == LocatorManner.ROLE:
            target: Locator = cls.page.get_by_role(**kwargs)
        elif manner == LocatorManner.TEXT:
            target: Locator = cls.page.get_by_text(**kwargs)
        elif manner == LocatorManner.LABEL:
            target: Locator = cls.page.get_by_label(**kwargs)
        elif manner == LocatorManner.PLACEHOLDER:
            target: Locator = cls.page.get_by_placeholder(**kwargs)
        elif manner == LocatorManner.ALT_TEXT:
            target: Locator = cls.page.get_by_alt_text(**kwargs)
        elif manner == LocatorManner.TITLE:
            target: Locator = cls.page.get_by_title(**kwargs)
        elif manner == LocatorManner.TEST_ID:
            target: Locator = cls.page.get_by_test_id(**kwargs)
        elif manner == LocatorManner.CSS or manner == LocatorManner.XPATH:
            target: Locator = cls.page.locator(selector=args[0])
        else:
            logger.error("传入方式不合法")
            return None
        # 判断定位到的是单个元素还是元素列表或者定位失败
        if target is not None:
            return target if len(target.all()) <= 1 else target.all()
        else:
            logger.error("未能定位到元素")
            return target

    @classmethod
    def get_locator_by_curr_locator(cls, curr_locator: Locator, manner: LocatorManner, *args, **kwargs) -> Locator | \
                                                                                                           list[
                                                                                                               Locator] | None:
        """
        基于当前的Locator来通过多种方式定位元素
        :param curr_locator: 当前的Locator对象
        :param manner: 方式枚举
        :param kwargs: 对应方式所需传入的参数
        :return: 单个元素 或 元素列表 或 None
        """
        logger.info(f"定位方式为{manner.name}")
        if manner == LocatorManner.ROLE:
            target: Locator = curr_locator.get_by_role(**kwargs)
        elif manner == LocatorManner.TEXT:
            target: Locator = curr_locator.get_by_text(**kwargs)
        elif manner == LocatorManner.LABEL:
            target: Locator = curr_locator.get_by_label(**kwargs)
        elif manner == LocatorManner.PLACEHOLDER:
            target: Locator = curr_locator.get_by_placeholder(**kwargs)
        elif manner == LocatorManner.ALT_TEXT:
            target: Locator = curr_locator.get_by_alt_text(**kwargs)
        elif manner == LocatorManner.TITLE:
            target: Locator = curr_locator.get_by_title(**kwargs)
        elif manner == LocatorManner.TEST_ID:
            target: Locator = curr_locator.get_by_test_id(**kwargs)
        elif manner == LocatorManner.CSS or manner == LocatorManner.XPATH:
            target: Locator = curr_locator.locator(selector_or_locator=args[0])
        else:
            logger.error("传入方式不合法")
            return None
        if target is not None:
            return target if len(target.all()) <= 1 else target.all()
        else:
            logger.error("未能定位到元素")
            return target

    @classmethod
    def navigate(cls, target_url: str) -> None:
        """
        用于浏览器当前页面的网址跳转
        :param target_url: 要跳转到的网页地址
        :return:
        """
        cls.page.goto(url=target_url, wait_until="domcontentloaded", timeout=20000)

    @classmethod
    def wait_for_element(cls,
                         selector: str,
                         state: Optional[Literal["attached", "detached", "hidden", "visible"]] = "visible",
                         strict: bool = True,
                         timeout: float = 30000
                         ) -> ElementHandle | None:
        """
        等待页面元素
        :param selector: 定位
        :param state: 预期状态
        :param strict: 严格模式与否
        :param timeout: 超时(毫秒)
        :return: 元素 或 None
        """
        return cls.page.wait_for_selector(selector=selector, state=state, strict=strict, timeout=timeout).as_element()

    @classmethod
    def add_console_log_output(cls, content: str):
        """
        向浏览器的console中输出内容。
        :param content: 输出的内容。
        :return:
        """
        # Get the next console log
        # with cls.page.expect_console_message() as msg_info:
        # Issue console.log inside the page
        if len(content) > 0:
            cls.page.evaluate("console.log('" + content + "')")
        else:
            pass
        # msg = msg_info.value
        # Deconstruct print arguments
        # logger.info(msg.args[0].json_value())  # hello
        # logger.info(msg.args[1].json_value())  # 42
        # logger.info(msg.args[2].json_value())

    @classmethod
    def listen_console_msg(cls, level: str = Literal["All", "Error"]) -> None:
        """
        基于level传入的级别，来打印浏览器console中的log。
        :param level: 级别
        :return:
        """
        if level == "All":
            # Listen for all console logs
            cls.page.on("console", lambda msg: logger.info(msg.text))
        elif level == "Error":
            # Listen for all console events and handle errors
            cls.page.on("console", lambda msg: logger.info(f"error: {msg.text}") if msg.type == "error" else None)
        else:
            pass

    @classmethod
    def execute_javascript(cls, js_command: str) -> None:
        """
        用于执行JS命令
        :param js_command:
        :return:
        """
        cls.page.evaluate(js_command)

    @classmethod
    def start_listener(cls,
                       event: Literal["request", "requestfailed", "requestfinished", "response"],
                       func: Callable[..., None]) -> None:
        """
        开启后持续监听拦截Request或Response
        :param event: 事件
        :param func: 事件处理方法（可对Request和Response做操作）
        :return: None
        """
        cls.page.on(event=event, f=func)

    @classmethod
    def remove_listener(cls,
                        event: Literal["request", "requestfailed", "requestfinished", "response"],
                        func: Callable[..., None]) -> None:
        """
        结束监听拦截Request或Response
        :param event: 事件
        :param func: 事件处理方法（可对Request和Response做操作）
        :return: None
        """
        cls.page.remove_listener(event=event, f=func)

    @classmethod
    def mouse_up_down(cls,
                      manner: Literal["up", "down", "down_up"],
                      button: Optional[Literal["left", "right", "middle"]] = "left",
                      click_count: Optional = 1) -> None:
        """
        模拟鼠标按键的【按下】【抬起】操作
        :param manner: 鼠标按键方式
        :param button: 鼠标按键
        :param click_count: 次数
        :return: None
        """
        if manner == "up":
            cls.page.mouse.up(button=button, click_count=click_count)
        elif manner == "down":
            cls.page.mouse.down(button=button, click_count=click_count)
        else:
            for i in range(click_count):
                cls.page.mouse.down(button=button)
                cls.page.mouse.up(button=button)

    @classmethod
    def mouse_move_click_wheel(cls,
                               manner: Literal["move", "click", "dblclick", "wheel"],
                               x: float,
                               y: float,
                               **kwargs
                               ) -> None:
        """
        模拟鼠标移动、单击、双击、滚轮操作
        :param manner: 模拟鼠标的哪一种操作
        :param x: 横坐标
        :param y: 纵坐标
        :param kwargs: 对应操作的附加参数，具体支持如下：
            button: Optional[Literal["left", "right", "middle"]] = "left",
            click_count: Optional = 1,
            delay: float = 0,
            steps: int = 1
        :return: None
        """
        if manner == "move":
            cls.page.mouse.move(x, y, **kwargs)
        elif manner == "click":
            cls.page.mouse.click(x, y, **kwargs)
        elif manner == "dblclick":
            cls.page.mouse.dblclick(x, y, **kwargs)
        elif manner == "wheel":
            cls.page.mouse.wheel(delta_x=x, delta_y=y)
        else:
            pass

    @classmethod
    def operate_keyboard(cls,
                         manner: Literal["up", "down", "press", "type", "insert_text"],
                         key_text: str,
                         *,
                         delay: float = 0) -> None:
        """
        模拟键盘的按键操作
        :param manner: 按键的操作方式
        :param key_text: 按键或内容
        :param delay: 按键按下与抬起中间的延迟（float类型，单位毫秒）
        :return: None
        """
        if manner == "up":
            cls.page.keyboard.up(key=key_text)
        elif manner == "down":
            cls.page.keyboard.down(key=key_text)
        elif manner == "press":
            cls.page.keyboard.press(key=key_text, delay=delay)
        elif manner == "type":
            cls.page.keyboard.type(text=key_text, delay=delay)
        elif manner == "insert_text":
            cls.page.keyboard.insert_text(text=key_text)
        else:
            pass

    @classmethod
    def close_context(cls, context: BrowserContext = None) -> None:
        cls.context.close() if context is None else context.close()

    @classmethod
    def close_browser(cls, browser: Browser = None) -> None:
        cls.browser.close() if browser is None else browser.close()


def print_request_sent(request: Request):
    logger.info(type(request))
    logger.info(f"Request sent: {request.url}, ResponseStatus={request.response().status}")


def print_remove_listener():
    logger.info("结束监听")


if __name__ == "__main__":
    with sync_playwright() as playwright:
        PlayWrightCommon.init(playwright=playwright, headless=False)
        PlayWrightCommon.start_listener("request", print_request_sent)
        PlayWrightCommon.start_listener("requestfinished", lambda request: logger.info(
            f"{request.method} {request.url} {request.response().status}"))
        PlayWrightCommon.navigate("https://measure.csleasing.com.cn/")
        # PlayWrightCommon.remove_listener("requestfinished", print_remove_listener)  # 该方法报错。
        PlayWrightCommon.get_locator(manner=LocatorManner.PLACEHOLDER, text="账号").fill(value="zhengyu")  # 直接输入
        PlayWrightCommon.get_locator(LocatorManner.XPATH, "//*[@id='form_item_password']").clear()
        PlayWrightCommon.get_locator(LocatorManner.XPATH, "//*[@id='form_item_password']").click(delay=3000)
        PlayWrightCommon.operate_keyboard(manner="insert_text", key_text="MyPassword")  # 通过模拟键盘输入
        PlayWrightCommon.page.pause()
        PlayWrightCommon.listen_console_msg(level="All")
        PlayWrightCommon.execute_javascript("prompt('Enter a number:')")
        PlayWrightCommon.execute_javascript("alert('Stop!')")
        PlayWrightCommon.page.wait_for_timeout(1000)
        PlayWrightCommon.mouse_up_down(manner="down")
        PlayWrightCommon.mouse_up_down(manner="up")
        PlayWrightCommon.mouse_up_down(manner="down_up", button="middle")
        PlayWrightCommon.mouse_move_click_wheel(manner="move", x=100.2, y=100.5, steps=10)
        PlayWrightCommon.mouse_move_click_wheel(manner="dblclick", x=100, y=100, button="right", delay=500)
        PlayWrightCommon.mouse_move_click_wheel(manner="click", x=200, y=300, button="left", delay=500, click_count=2)
        PlayWrightCommon.mouse_move_click_wheel(manner="dblclick", x=200, y=200, button="right", delay=500)
        PlayWrightCommon.page.pause()
        PlayWrightCommon.close_context()
        PlayWrightCommon.close_browser()
