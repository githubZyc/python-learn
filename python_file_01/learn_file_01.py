import pandas as pd

excel = pd.read_excel("/Volumes/files/yonghe-files/所有已经配置了私有化的院部.xlsx", sheet_name="SheetJS")
# 1. 查看前几行数据
print("=== 前5行数据 ===")
print(excel.head())

pd.read_json()

# f = open("/Volumes/files/yonghe-files/所有已经配置了私有化的院部.xlsx","r",encoding="utf-8",errors="ignore")
# readline = f.readline()
# print(readline)


f2 = open("/Users/zhengyanchuang/Documents/支付宝开放平台密钥工具/密钥20240819152701/应用公钥RSA2048.txt",
          mode="r")
readline = f2.readline()
print(readline)

with open("/Users/zhengyanchuang/Documents/支付宝开放平台密钥工具/密钥20240819152701/应用公钥RSA2048.txt") as f:
    for line in f:
        print(line)
