f = open('workfile.txt', 'rb+')
f.write(b'0123456789abcdef')

# 定位到文件中的第 6 个字节
print(f.seek(5))
print(f.read(1))
print(f.seek(-3, 2))  # 定位到倒数第 3 个字节)
