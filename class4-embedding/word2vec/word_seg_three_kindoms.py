# -*-coding: utf-8 -*-
# 对txt文件进行中文分词
import jieba
import os
from utils import files_processing

# 源文件所在目录
source_folder = './three_kingdoms/source'
segment_folder = './three_kingdoms/segment'

# 确保输出目录存在
os.makedirs(segment_folder, exist_ok=True)

# 字词分割，对整个文件内容进行字词分割
def segment_lines(file_list,segment_out_dir,stopwords=[]):
    print(f"找到 {len(file_list)} 个文件需要分词")
    for i, file in enumerate(file_list):
        print(f"正在处理文件: {file}")
        segment_out_name = os.path.join(segment_out_dir, 'segment_{}.txt'.format(i))
        try:
            with open(file, 'rb') as f:
                document = f.read()
                print(f"文件大小: {len(document)} 字节")
                document_cut = jieba.cut(document)
                sentence_segment = []
                for word in document_cut:
                    if word not in stopwords:
                        sentence_segment.append(word)
                result = ' '.join(sentence_segment)
                result = result.encode('utf-8')
                with open(segment_out_name, 'wb') as f2:
                    f2.write(result)
                    print(f"已保存分词文件: {segment_out_name}")
        except Exception as e:
            print(f"处理文件 {file} 时出错: {e}")

# 对source中的txt文件进行分词，输出到segment目录中
print(f"从目录 {source_folder} 获取文件列表...")
file_list = files_processing.get_files_list(source_folder, postfix='*.txt')
print(f"文件列表: {file_list}")
segment_lines(file_list, segment_folder)
print("分词完成")
