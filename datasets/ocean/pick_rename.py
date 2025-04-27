import os
import shutil


# 从oc中，复制所有的植物数据，连带着部分其他和塑料：【1181:833:1964】
def getItems(source_IMGdir,source_LABdir,dest_IMGdir,dest_LABdir):

    # 创建目标目录（如果不存在）
    os.makedirs(dest_LABdir, exist_ok=True)
    os.makedirs(dest_IMGdir, exist_ok=True)

    txt_files = [f for f in os.listdir(source_LABdir) if f.endswith('.txt')]
    counter = 1         #[Edit]新文件命名计数
    total = 0           #[Edit]已搜索的文件数量
    ID1_sum = 0         #[Edit]已搜索的id1数量

    for txt_file in txt_files:
            txt_path = os.path.join(source_LABdir, txt_file)
            with open(txt_path, 'r') as file:
                lines = file.readlines()


            #[Edit]条件筛选
            id0_count = sum(1 for line in lines if line.strip().startswith('0'))
            id1_count = sum(1 for line in lines if line.strip().startswith('1'))
            if id0_count == 0 and id1_count > 0:
                print(f"在 {txt_file} 中发现 {id1_count} 个行首为1且不存在0的行")

                ID1_sum += id1_count
                counter += 1  # 更新计数器
                # 按顺序重命名并复制TXT文件
                new_txt_name = f"{counter}.txt"
                shutil.copy(txt_path, os.path.join(dest_LABdir, new_txt_name))

                # 复制对应的图片文件，并确保同名
                img_name = os.path.splitext(txt_file)[0] + '.jpg'  # 假设图片格式为.jpg
                img_path = os.path.join(source_IMGdir, img_name)
                if os.path.exists(img_path):
                    new_img_name = f"{counter}.jpg"
                    shutil.copy(img_path, os.path.join(dest_IMGdir, new_img_name))
            else:
                print(f"{txt_file} 中没有行首为1的行或者含有0")
            total += 1
            print(f"已处理搜索{total}个文件,发现{counter}个文件,总计：{ID1_sum}个id1")
            #[Edit]退出条件
            if ID1_sum > 2080:
                break

# 重命名图片和标签文件,前提是确保图片和标签文件是一一对应的
def rename(img_dir,label_dir,outIMG_dir,outLAB_dir):

    os.makedirs(outIMG_dir, exist_ok=True)
    os.makedirs(outLAB_dir, exist_ok=True)

    counter = 14285
    for imgname in os.listdir(img_dir):
        if imgname.endswith('.jpg'):
               
            img_path = os.path.join(img_dir, imgname)
            lab_path = os.path.join(label_dir, imgname.replace('.jpg', '.txt'))

            new_imgname = f"{counter}.jpg"
            new_labname = f"{counter}.txt"

            new_img_path = os.path.join(outIMG_dir, new_imgname)
            new_lab_path = os.path.join(outLAB_dir, new_labname)

            shutil.copy(img_path, new_img_path)
            shutil.copy(lab_path, new_lab_path)

            counter += 1
            print(f"{imgname} and txt       has been renamed to {new_imgname}")

# 将图片及对应的TXT随机划分为三组，比例为7:2:1，分别放在三个文件夹下     
#def div():

if __name__ == "__main__":
    img_dir = './images/valid'
    label_dir = './labels/valid'
    outIMG_dir = './re_images/valid'
    outLAB_dir = './re_labels/valid'
    
    
    #getItems()
    rename(img_dir,label_dir,outIMG_dir,outLAB_dir)
