from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime

def check_time(str_time):
    '''
    检查日期是否大于6个月的函数
    '''
    # 去除空白符
    clean_time = str_time.strip()

    #处理“昨天这种特殊情况”
    if clean_time == "昨天":
        return False

    if "小时前" in clean_time:
        print("字符串中包含'小时前'")
        return False
    if "分钟前" in clean_time:
        print("字符串中包含'分钟前'")
        return False

    # 尝试解析为 datetime 对象
    try:
        dt = datetime.strptime(clean_time,"%Y-%m-%d")
    except ValueError:
        print("日期解析解析失败，尝试第二方案解析")
        clean_time = "2024-"+clean_time
        dt = datetime.strptime(clean_time,"%Y-%m-%d")
        

    # 获取当前时间
    now = datetime.now()

    # 计算时间差
    delta = now -dt

    # 计算月数差异
    months_diff = delta.days // 30  # 将天数差异转换为月数（假设一个月有 30 天）

    print(months_diff)
    
    if months_diff > 6:
        return True
    else:
        return False

# evilbili
# 最新的一个视频的时间是： 2020-6-30
# 是否大于六个月未更新？： False
# 小呆萝拉
# 最新的一个视频的时间是： 1-4
# 是否大于六个月未更新？： False
# 英短喵
# 最新的一个视频的时间是： 1-16
# 是否大于六个月未更新？： False
# 给你一个安安
# 最新的一个视频的时间是： 2017-11-6
# 是否大于六个月未更新？： False
# __小黄瓜__
# 最新的一个视频的时间是： 3-6
# 是否大于六个月未更新？： False
# 是西瓜酱啊
# 最新的一个视频的时间是： 2022-2-28
# 是否大于六个月未更新？： False


def open2CheckLastTime(page,up_name):
    # 这些其实都是录制的，逻辑是有问题的
    with page.expect_popup() as page1_info:
        page.locator("#page-follows").get_by_role("link", name=up_name).click()
    page1 = page1_info.value
    page1.locator("#navigator").get_by_role("link", name=" 投稿").click()
    page1.wait_for_timeout(700)
    # 从这里开始实际上就是从最新的视频列表里拿到最新更新视频时间的子例程了
    test_if_aviliable_user = len(page1.locator("css=.time").all())
    print("times的列表的长度为：",test_if_aviliable_user)
    if test_if_aviliable_user > 0:
        dd = page1.locator("css=.time").first
        print("最新的一个视频的时间是：",dd.text_content().strip())
        if_exceed_6_month = check_time(dd.text_content())
        print("是否大于六个月未更新？：",if_exceed_6_month)
        if if_exceed_6_month:
            page1.get_by_text("已关注").hover()
            page1.wait_for_timeout(500)
            page1.get_by_text("取消关注").click()
            print("该用户有六个月没更新了，取消关注吧")
        else:
            pass
        page1.close()
    else:
        print("该用户无有效视频了，该取关了")
        page1.get_by_text("已关注").hover()
        page1.wait_for_timeout(200)
        page1.get_by_text("取消关注").click()
        page1.close()

def checkOnePage(page):
    #等两秒钟这个页面正常加载后，这样不会出现一些麻烦的问题
    page.wait_for_timeout(2200)

    #取得当前所有up主的名字
    up_names = page.locator("css=.fans-name").all()

    for up_name in up_names:
        print(up_name.text_content())
        open2CheckLastTime(page,up_name.text_content())

# 保存断点信息到文件
def save_breakpoint_info(breakpoint):
    with open('breakpoint_info.txt', 'w') as file:
        file.write(str(breakpoint))

# 从文件中恢复断点信息
def load_breakpoint_info():
    try:
        with open('breakpoint_info.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return None


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    page.goto("https://space.bilibili.com/750367/fans/follow")
    page.locator("#page-follows input[type=\"text\"]").click()

    # 主程序逻辑
    breakpoint = 60  # 设置断点

    # 初次运行时，保存断点信息
    if load_breakpoint_info() is None:
        save_breakpoint_info(breakpoint)

    # 从断点处继续工作
    current_breakpoint = load_breakpoint_info()
    if current_breakpoint is not None:
        print(f"恢复断点: {current_breakpoint}")
        breakpoint = current_breakpoint

    # 示例用法
    save_breakpoint_info(breakpoint)
    page.locator("#page-follows input[type=\"text\"]").fill(str(breakpoint))
    page.locator("#page-follows input[type=\"text\"]").press("Enter")
    page.wait_for_timeout(1130)
    while True:
        checkOnePage(page)
        page.get_by_role("listitem", name="上一页").click()
        breakpoint = breakpoint -1
        # 示例用法
        save_breakpoint_info(breakpoint)
        page.wait_for_timeout(1130)
        pass
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
