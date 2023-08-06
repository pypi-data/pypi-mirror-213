import logging
import time

from .yunxiao import YunXiao, UsedTime
import requests


class V2(YunXiao):
    def __init__(self, configfile: str = "yunxiao_config.ini", campus: list = None):
        """
        初始化，输入用户账号密码，以及要操作的校区。
        :param campus: 校区
        :param configfile: 配置文件路径
        """
        super().__init__(configfile)
        if campus is None:
            self.campus = []
        else:
            self.campus = campus

        self.reportpath = "https://yunxiao.xiaogj.com/api/cs-report/report/"
        self.orderpath = "https://yunxiao.xiaogj.com/api/cs-edu/order"
        self.edupath = "https://yunxiao.xiaogj.com/api/cs-edu/"
        self.crmpath = "https://yunxiao.xiaogj.com/api/cs-crm/"

    def request(self, **kwargs) -> dict:
        response = requests.request(
            method=kwargs.get("method"),
            url=kwargs.get("url"),
            json=kwargs.get("json"),
            params=kwargs.get("params"),
            headers={"x3-authentication": self.token}
        )

        if response.status_code != 200:
            logging.error("无法到连接云校服务器。")
            return {"data": "无法到连接云校服务器。"}

        if response.json()["code"] == 401:
            logging.error(response.json()["msg"])
            self.renew_token()
            response = requests.request(
                method=kwargs.get("method"),
                url=kwargs.get("url"),
                json=kwargs.get("json"),
                params=kwargs.get("params"),
                headers={"x3-authentication": self.token, "Cookie": self.cookie}
            )

        return response.json()

    # 列出全部校区
    def campus_list_all(self) -> list:
        return self.request(
            method="get",
            url="https://yunxiao.xiaogj.com/api/cs-crm/campus/list?type=2"
        )["data"]

    # 列出全部老师[最大9999条]
    def teacher_list_all(self) -> list:
        """
        列出全部老师<MAX-9999>
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/pageList",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": [],
                "statusList": [1, 0],
                "page": {"pageNum": 1, "pageSize": 9999}
            }
        )["data"]

    # 查询老师
    def teacher_query(self, name: str, status: int, size: int) -> list:
        """
        :return:
        """
        return self.request(
            method="post",
            url=self.crmpath + "teacher/pageList",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "queryKey": name,
                "statusList": [status],
                "page": {"pageNum": 1, "pageSize": size}
            }
        )["data"]

    # 列出全部学生[最大99999条]
    def student_listall(self) -> list:
        """
        列出全部学生[最大99999条]
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-crm/student/list",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "status": [],
                "orgTag": 1,
                "page": {"pageNum": 1, "pageSize": 99999}
            }
        )["data"]

    # 查询学生
    def student_query(self, curriculumids: list = None, classids: list = None, name: str = "",
                      status: list = None, class_student_status: int = 0, size: int = 99999) -> list:
        """
        [教务管理/学员]
        列出学生
        :param size: 项目数量
        :param curriculumids: 课程筛选
        :param classids: 班级筛选
        :param name: 姓名查询关键字
        :param status: 学员状态 0>未收费 1>在读 6>曾就读 7>停课 99>无效学员
        :param class_student_status: 0>不筛选 1>未入班 2>已入班
        :return:
        """
        if status is None:
            status = [1, 7]
        return self.request(
            method="post",
            url=self.crmpath + "student/list",
            json={
                "_t_": UsedTime.stamp,
                "name": name,
                "campusIds": self.campus,
                "status": status,
                "intentionStatus": 0,
                "curriculumIds": curriculumids,
                "classIds": classids,
                "classStudentStatus": class_student_status,
                "orgTag": 1,
                "page": {"pageNum": 1, "pageSize": size}
            }
        )["data"]

    # 列出全部课程[最大9999条]
    def curriculum_list_all(self) -> list:
        """
        列出全部课程[最大9999条]
        :return:
        """
        return self.request(
            method="post",
            url=self.edupath + "curriculum/pageList",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "page": {
                    "pageNum": 1,
                    "pageSize": 9999
                }
            }
        )["data"]

    # 查询课程
    def curriculum_query(self, searchname: str = None, haltsalelist: list = None, size: int = 9999) -> list:
        """
        查询所有在开的课程
        :param size:
        :param searchname: 查找关键字。
        :param haltsalelist: 是否在售。0>在售 1>停售
        :return:
        """
        return self.request(
            method="post",
            url=self.edupath + "curriculum/pageList",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "curriculumName": searchname,
                "haltSaleList": haltsalelist,
                "page": {
                    "pageNum": 1,
                    "pageSize": size
                }
            }
        )["data"]

    # 列出指定日期范围全部排课[最大99999条]
    def arrange_list_daterange(self, before_today: int, after_today: int) -> list:
        """
        列出全部排课[最大99999条]
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/arrange/page",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "startDate": time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * before_today)),
                "endDate": time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * after_today)),
                "displayCompletedClass": True,
                "page": {"pageNum": 1, "pageSize": 99999}
            }
        )["data"]

    # 列出指定日期全部排课[最大9999条]
    def arrange_list_date(self, date: str = UsedTime.today) -> list:
        """
        列出日期范围全部排课[最大9999条]
        :param date:
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/arrange/getCompanyCourse",
            json={
                "_t_": UsedTime.stamp,
                "date": date,
                "campusIds": self.campus,
                "page": {
                    "pageNum": 1,
                    "pageSize": 9999
                }
            }
        )["data"]

    # 查询指定日期范围排课
    def arrange_query_daterange(self, starttime: str = None, endtime: str = None,
                                displayCompletedClass=False, size: int = 99999) -> list:
        """
        排课管理。
        :param displayCompletedClass: 显示已结班排课
        :param size:
        :param starttime: 查询起始时间
        :param endtime: 查询截止时间
        :return:
        """
        return self.request(
            method="post",
            url=self.edupath + "arrange/page",
            json={
                "_t_": UsedTime.stamp,
                "campusIds": self.campus,
                "startDate": starttime,
                "endDate": endtime,
                "displayCompletedClass": displayCompletedClass,
                "page": {"pageNum": 1, "pageSize": size}
            }
        )["data"]

    # 查询指定日期排课
    def arrange_queery_date(self, date: str = UsedTime.today) -> list:
        """
        ⚠ 未完成，无法使用 查询指定日期排课
        :param date:
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/arrange/getCompanyCourse",
            json={
                "_t_": UsedTime.stamp,
                "date": date,
                "campusIds": self.campus,
                "page": {
                    "pageNum": 1,
                    "pageSize": 9999
                }
            }
        )["data"]

    # 列出指定月份的每日费用数据
    def money_list_month(self, yy_mm: str) -> list:
        """
        :param yy_mm: 月份，格式示例： 2023-02
        :return:
        """
        course = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findCourseMoney",
            json={"campusIds": self.campus, "date": yy_mm, "dateType": 1, "_t_": UsedTime.stamp}
        )["data"]

        refund = self.request(
            method="post",
            url=self.reportpath + "findRefundMoney",
            json={"campusIds": self.campus, "date": yy_mm, "dateType": 1, "_t_": UsedTime.stamp}
        )["data"]

        tuition = self.request(
            method="post",
            url=self.reportpath + "findTuition",
            json={"campusIds": self.campus, "date": yy_mm, "dateType": 1, "_t_": UsedTime.stamp}
        )["data"]

        return list(map(lambda x: {**x[0], **x[1], **x[2]}, zip(course, refund, tuition)))

    # 分校区列出指定日期的费用数据
    def campus_todaymoney_list_all(self, date: str = UsedTime.today) -> list:
        """
        分校区列出指定日期的费用数据。
        :param date: 日期
        :return:
        """
        data_list = self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findDataReportList",
            json={
                "campusIds": self.campus,
                "startDate": date,
                "endDate": date,
                "orderByCampus": 1,
                "_t_": UsedTime.stamp
            }
        )["data"]["dataReportVos"]
        return list(map(lambda item: {**item, "id": f"{date}-{item['campusId']}"}, data_list))

    # 列出全部班级
    def class_list_all(self) -> list:
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-edu/classInfo/page",
            json={
                "_t_": UsedTime.stamp,
                "orgTag": 1,
                "campusIds": self.campus,
                "page": {"pageNum": 1, "pageSize": 9999}
            }
        )["data"]

    # 列出指定上课日期范围的所有课消记录
    def charge_record_list_daterange(self, startdate: str = "", enddate: str = "") -> list:
        """
        :param startdate: YY-MM-DD
        :param enddate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findOrderItemAll/page",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 100000},
                "campusIds": self.campus,
                "courseStartTime": startdate,
                "courseEndTime": enddate,
                "sort": 1,
                "sortField": "operationTime"
            }
        )["data"]

    # 列出指定上课日期范围的所有课消详情
    def charge_detail_list_daterange(self, startdate: str = "", enddate: str = "") -> list:
        """
        :param startdate: YY-MM-DD
        :param enddate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findCourseSignChargeDetail",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 100000},
                "campusIds": self.campus,
                "courseStartTime": startdate,
                "courseEndTime": enddate,
            }
        )["data"]

    # 列出指定操作日期范围的所有订单记录
    def order_item_list_all(self, startdate: str = "", enddate: str = "") -> list:
        """
        列出指定操作日期范围的所有订单记录
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/findOrderItemAll/page",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate
            }
        )["data"]

    # 列出指定操作日期范围的所有退费详情
    def payment_refund_list_all(self, startdate: str = "", enddate: str = "") -> list:
        """
        列出指定操作日期范围的所有订单记录
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentRefundList",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "refundFinishStartTime": startdate,
                "refundFinishEndTime": enddate
            }
        )["data"]

    # 列出指定操作日期范围的所有支出详情
    def payment_item_list_all(self, startdate: str = "", enddate: str = "") -> list:
        """
        列出指定操作日期范围的所有订单记录
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentList",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "payStartTime": startdate,
                "payEndTime": enddate
            }
        )["data"]

    # 列出指定操作日期范围的所有账户收支记录
    def payment_record_list_all(self, startdate: str = "", enddate: str = "") -> list:
        """
        列出指定操作日期范围的所有订单记录
        :param enddate: YY-MM-DD
        :param startdate: YY-MM-DD
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-pc-report/cs-report/reports/findPaymentAccountCustomRecord",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 10000},
                "campusIds": self.campus,
                "startTime": startdate,
                "endTime": enddate,
                "displayInvalidOrder": True
            }
        )["data"]

    # 列出所有课程卡
    def card_list_all(self) -> list:
        """
        列出所有课程卡
        :return:
        """
        return self.request(
            method="post",
            url="https://yunxiao.xiaogj.com/api/cs-report/report/studentCourseCard/report",
            json={
                "_t_": UsedTime.stamp,
                "page": {"pageNum": 1, "pageSize": 100000},
                "campusIds": self.campus,
                "displayHistory": True
            }
        )["data"]


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
