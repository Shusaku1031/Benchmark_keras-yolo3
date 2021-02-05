import os

target_files = os.listdir(os.path.join("VOCDevkit","VOC2007","ImageSets","Main"))
xml_files = [ xml.split(".")[0] for xml in os.listdir(os.path.join("VOCDevkit","VOC2007","Annotations"))]
#print(xml_files)

train_rate = 0.8
val_rate = 0.1

train_names = xml_files[:round(len(xml_files)*train_rate)]
val_names = xml_files[round(len(xml_files)*train_rate):round(len(xml_files)*(train_rate+val_rate))]
test_names = xml_files[round(len(xml_files)*(train_rate+val_rate)):]

print("train:",train_names)
print("val:",val_names)
print("test:",test_names)


with open(os.path.join("VOCDevkit","VOC2007","ImageSets","Main","train.txt"), "w") as f:
    for n in train_names:
        f.write(n+"\n")

with open(os.path.join("VOCDevkit","VOC2007","ImageSets","Main","val.txt"), "w") as f:
    for n in val_names:
        f.write(n+"\n")  

with open(os.path.join("VOCDevkit","VOC2007","ImageSets","Main","test.txt"), "w") as f:
    for n in test_names:
        f.write(n+"\n")  