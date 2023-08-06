from typing import List

import pandas as pd
import json


# 表单处理类
class Excel:
    path: str
    sheet: str
    data: pd.DataFrame

    # 初始化 并读取数据
    def __init__(self, path, sheet="Sheet1"):
        self.path = path
        self.sheet = sheet
        self.data = pd.read_excel(path, sheet_name=sheet)

    # 过滤数据
    def filter(self, cols: List[str]):
        df = self.data
        # 筛选列名与传入字符串匹配的列
        matched_cols = [col for col in df.columns if col in cols]
        self.data = df[matched_cols]
        return df[matched_cols]

    # 获取数据
    def data(self):
        return self.data

    # 获取列
    def columns(self):
        return self.data.columns.tolist()

    # 转化为JSON
    def toJson(self):
        j_data = self.data.to_dict(orient='records')
        json_data = json.dumps(j_data)
        return json_data

    def to_json(self):
        return self.toJson()

    # 修改指定行
    def edit(self, _index_: int, k: str, v: str) -> bool:
        t_data = self.data
        t_data.loc[_index_, k] = v
        self.data = t_data
        return True

    # 写入文件
    def flush(self) -> bool:
        # 先写入
        self.data.to_excel(self.path, index=False)
        return True

    # 关闭 执行写入
    def close(self):
        self.flush()


if __name__ == '__main__':
    print("读取文件")
