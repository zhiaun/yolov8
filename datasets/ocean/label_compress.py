# 用于标签整合


import os
import shutil

# 定义替换规则
REPLACE_RULES = {
    '0': '2',
    '1': '0',
    '2': '0',
    '3': '1',
    '4': '2',
    '5': '2',
    '6': '1',
    '7': '0'
}
# 标签整合
def process_files():
    label_dir = './labels'
    new_label_dir = './labels2'

    # 创建目标目录（如果不存在）
    os.makedirs(new_label_dir, exist_ok=True)

    txt_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    total_files = len(txt_files)
    replaced_lines = 0

    for txt_file in txt_files:
        txt_path = os.path.join(label_dir, txt_file)
        new_txt_path = os.path.join(new_label_dir, txt_file)

        with open(txt_path, 'r') as file:
            lines = file.readlines()

        # 替换每一行的首字符
        modified_lines = []
        for line in lines:
            if line.strip():  # 确保行不为空
                first_char = line[0]
                if first_char in REPLACE_RULES:
                    modified_line = REPLACE_RULES[first_char] + line[1:]
                    replaced_lines += 1
                else:
                    modified_line = line
                modified_lines.append(modified_line)

        # 写入修改后的文件
        with open(new_txt_path, 'w') as file:
            file.writelines(modified_lines)

    print(f"共处理了 {total_files} 个文件，替换行数为 {replaced_lines}")

if __name__ == "__main__":
    process_files()