import os

path = "data"
name_list = [i for i in os.listdir(path) if i != '.DS_Store']
pic_num = 0
each_pic = []
for name in name_list:
    pic_path = path + "/" + name
    pic_list = [i for i in os.listdir(pic_path) if i != '.DS_Store']
    each_pic.append([name,len(pic_list)])
    pic_num += len(name)

print(pic_num)
print(each_pic)
