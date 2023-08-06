import os, sys

def check_path(path):
    split_path = path.split('/')
    mix_path = ""
    for i in split_path:
        if i != "":
            mix_path = mix_path + "/" + i
            # print(mix_path)
            try:
                if not os.path.exists(mix_path):
                    os.mkdir(mix_path)
                    print("Create path " + mix_path)
            except Exception as e:
                print("Check path => "+ str(e))
    if os.path.exists(path):
        return True
    else:
        return False
