# 作用：统计txt中每个标签的数量
# 用法：在标签文件所在的上层运行，该脚本会递归搜索所有txt文件
import os
from collections import defaultdict

def count_first_characters(directory):
    first_char_count = defaultdict(int)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:  # Skip empty lines
                            first_char = line[0]
                            first_char_count[first_char] += 1
    
    return first_char_count

if __name__ == "__main__":
    directory = '.'  # Specify the directory containing your text files
    result = count_first_characters(directory)
    print(result)
    input()