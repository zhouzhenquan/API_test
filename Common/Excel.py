"""
============================
Author:周振全
Time:2020/2/103:23 下午
E-mail:17764509133@163.com
============================
"""

"""分装Excel表格方法"""

import openpyxl


class operation_excel(object):

    def __init__(self, FileName, SheetName):
        self.FileName = FileName
        self.SheetName = SheetName

    """读数据"""
    def read_excel(self):
        self.open_excel()
        """读取数据"""
        data = list(self.sh.rows)
        """读取数据，保存为字典"""
        li = [i.value for i in data[0]]  # 这是Excel的第一行数据
        """创建一个列表"""
        cases = []
        """遍历除第一行以外的数据"""
        for i in data[1:]:
            """读取该数据的值"""
            values = [c.value for c in i]
            """将第一行数据与遍历出来的数据进行打包处理，后转换为字典"""
            case = dict(zip(li, values))
            """将字典添加到列表中"""
            cases.append(case)
        """然后返回整个列表"""
        return cases

    """写数据"""
    def write_excel(self, row, column, value):
        self.open_excel()
        """写入数据"""
        self.sh.cell(row=row, column=column, value=value)
        """保存文件"""
        self.wb.save(self.FileName)

    def open_excel(self):
        """选择工作薄"""
        self.wb = openpyxl.load_workbook(self.FileName)
        """选择表单"""
        self.sh = self.wb[self.SheetName]
