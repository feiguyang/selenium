import xlsxwriter

from Base.BaseElementEnmu import Element
from Base.BaseExcel import OperateReport
from Base.BaseInit import destroy
from Base.BasePickle import *
from datetime import datetime

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

'''
统计数据相关
'''

'''
result bool
logTest 记录日志类 class
driver
testinfo

'''


def countInfo(**kwargs):
    _info = {}
    step = ""  # 操作步骤信息
    check_step = ""  # 检查点步骤信息

    for case in kwargs["testCase"]:
        step = step + case["info"] + "\n"

    if type(kwargs["testCheck"]) == list:  # 检查点为列表
        for check in kwargs["testCheck"]:
            check_step = check_step + check["info"] + "\n"
    elif type(kwargs["testCheck"]) == dict:
        check_step = kwargs["testCheck"]["info"]
    else:
        print("获取检查点步骤数据错误，请检查")
        print(kwargs["testCheck"])

    _info["step"] = step  # 用例操作步骤
    _info["checkStep"] = check_step  # 用例检查点

    if kwargs["result"]:
        _info["result"] = "通过"
        kwargs["logTest"].checkPointOK(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
                                       checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
                                           "msg", " "))
    else:
        _info["result"] = "失败"  # 用例接开关
        _info["img"] = kwargs["logTest"].checkPointNG(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
                                                      checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
                                                          "msg", " "))
    _info["id"] = kwargs["testInfo"][0]["id"]  # 用例id
    _info["title"] = kwargs["testInfo"][0]["title"]  # 用例名称
    _info["caseName"] = kwargs["caseName"]  # 测试函数
    _info["name"] = kwargs["name"]  # 设备名
    _info["msg"] = kwargs["testInfo"][0].get("msg", "")  # 备注
    _info["info"] = kwargs["testInfo"][0]["info"]  # 前置条件

    writeInfo(data=_info, path=PATH("../Log/" + Element.INFO_FILE))
    # print(read(PATH("../Log/info.pickle")))


# 统计所有用例数
def countSum(result):
    # print("----countSum----")
    data = {"sum": 0, "pass": 0, "fail": 0}
    _read = read(PATH("../Log/sum.pickle"))
    if _read:
        data = _read
    data["sum"] += 1
    if result:
        data["pass"] += 1
    else:
        data["fail"] += 1
    write(data=data, path=PATH("../Log/" + Element.SUM_FILE))
    # print(read(PATH("../Log/sum.pickle")))


def countDate(testDate, testSumDate):
    data = read(PATH("../Log/" + Element.SUM_FILE))
    if data:
        data["testDate"] = testDate
        data["testSumDate"] = testSumDate
        write(data=data, path=PATH("../Log/" + Element.SUM_FILE))
    else:
        print("统计数据失败")
    data = read(PATH("../Log/" + Element.SUM_FILE))
    print("==统计数据：%s==" % data)


'''
测试报告
'''


def writeExcel():
    workbook = xlsxwriter.Workbook(PATH('../Report/' + Element.REPORT_FILE))
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    operateReport = OperateReport(workbook)
    operateReport.init(worksheet, read(PATH("../Log/" + Element.SUM_FILE)))
    operateReport.detail(worksheet2, readInfo(PATH("../Log/" + Element.INFO_FILE)))
    operateReport.close()

    # destroy()  # 删除文件


if __name__ == '__main__':
    # data = {'result': '失败', 'caseName': 'FirstOpenTest', 'title': '第一次打开', 'phoneName': 'samsung_GT-I9500_android_4.4.2', 'img': 'D:\\app\\appium\\log\\samsung_GT-I9500_android_4.4.220170607184558\\第一次打开CheckPoint_1_NG.png', 'id': 'test001'}
    # writeInfo(data, PATH("../Log/info.pickle"))
    # writeInfo(data, PATH("../Log/info.pickle"))
    # _read = readInfo(PATH("../Log/info.pickle"))
    writeExcel()
