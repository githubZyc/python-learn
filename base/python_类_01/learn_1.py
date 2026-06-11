# print("Hello, World!")
# user_names = ["赵敏","王刚","赵本山","赵小环"]
# for i in range(0,len(user_names)):
#     #print(user_names[i])
#     if user_names[i].startswith("赵"):
#         #print(user_names[i])
#         user_names[i] = "王"+user_names[i][1:]
#         print(user_names[i])
#
# pop = user_names.pop(0)
# print(pop)


user_names = ["赵敏", "王刚", "赵本山", "赵小环"]
for item in user_names:
    if item.startswith("赵"):
        user_names.remove(item)
print(user_names)
