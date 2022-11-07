import os
import time

from uitrace.api import *

import settings


class TestHoyo(object):
    def setup_class(self):
        init_driver(workspace=os.path.dirname(__file__))
        start_event_handler()

    def teardown_class(self):
        stop_driver()

    def setup_method(self, method):
        restart_app(settings.APPNAME, clear_data=False)

    def teardown_method(self, method):
        screenshot(label="finishForCheck", img_path=None, pos=None)
        logger.info("用例执行完成，杀app进程")
        # stop_app(settings.APPNAME)

    def test_login(self):
        if find(loc="obj_1667550056947.jpg", by=DriverType.CV, timeout=10):
            click(loc="obj_1667550056947.jpg", by=DriverType.CV, timeout=10)
            time.sleep(3)
        else:
            logger.info("没有找到同意并继续")
            # raise Exception("没有找到同意并继续")

        if find(loc="obj_1667550112916.jpg", by=DriverType.CV, timeout=10):
            logger.info("当前正在 请选择你关注的游戏页面")
            logger.info("找到了选好了， 准备点击")
            click(loc="obj_1667550112916.jpg", by=DriverType.CV, timeout=10)
        else:
            logger.info("没有找到选择选好了按钮")

        if click(loc="obj_1667550224158.jpg", by=DriverType.CV, timeout=5):
            logger.info("进入了青少年模式提示界面")
            logger.info("找到了 我知道了。点击确认")

            click(loc="obj_1667550224158.jpg", by=DriverType.CV, timeout=5)
        else:
            logger.info("没有找到青少年模式的我知道了确认")


        # 接下来要确认是否到达了首页，方法很简单，用CV找一下是否有签到福利
        if find("obj_1667549586170.jpg", by=DriverType.CV, timeout = 30):
            logger.info("找到了签到福利，成功到达首页")
        else:
            logger.info("没有找到签到福利")
            loc = find_ocr("签到福利", 10)
            if loc:
                logger.info("找到了签到福利，到达首页成功")
            else:
                raise Exception("到达首页失败")

        if find("//*[@resource-id='com.mihoyo.hyperion:id/mHomePageRbMe']/android.view.ViewGroup[1]", by=DriverType.UI):
            logger.info("找到了 我的")
            click(loc="//*[@resource-id='com.mihoyo.hyperion:id/mHomePageRbMe']/android.view.ViewGroup[1]", by=DriverType.UI, offset=None, timeout=30, duration=0.05, times=1)
            # 查找点击登录
            # 如果有新手提示
            times = 1
            while not find(loc="obj_1667549447833.jpg", by=DriverType.CV, timeout=30):
                if times >= 5:
                    logger.info("find 5 times, 点击登录failed")
                    raise Exception("找到点击登录按钮失败")
                logger.info("尝试点掉提示弹窗")
                long_click([0.134, 0.886], duration=0.5)
                times += 1

            times = 1
            while not find(loc="obj_1667552225140.jpg", by=DriverType.CV, timeout=5):
                if times >= 5:
                    logger.info("cannot click 点击登录")
                    raise Exception("无法点击 点击登录")
                click(loc="obj_1667549447833.jpg", by=DriverType.CV, timeout=30)
                time.sleep(1)
                times += 1
        else:
            logger.info("没有找到我的")
            raise Exception("首页上没有我的按钮")

        if find(loc="obj_1667552225140.jpg", by=DriverType.CV, timeout=30):
            logger.info("成功到达登陆页面")
        else:
            logger.info("未到达登陆页面")
            raise Exception("login failed")

        logger.info("login success")