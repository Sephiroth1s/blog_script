import os
import frontmatter
from datetime import datetime
from dateutil.parser import parse

def process_date_property(date_value):
    try:
        # 尝试解析日期
        # 使用 dateutil 解析日期字符串
        dt = parse(str(date_value))
        # 提取日期部分
        date_only = dt.date()
        return date_only
    except ValueError:
        # 如果解析失败，则返回原始值
        return date_value

def process_markdown_file(filepath, property_name):
    with open(filepath, 'r', encoding='utf-8') as file:
        post = frontmatter.load(file)
        front_matter = post.metadata

        # 提取指定属性值
        if property_name in front_matter:
            value = front_matter[property_name]

            # 特殊处理 date 属性值
            if property_name == 'date':
                value = process_date_property(value)

            # 获取文件名和文件夹名（不含路径）
            dirname = os.path.dirname(filepath)
            basename = os.path.basename(filepath)
            filename, ext = os.path.splitext(basename)  # 去除扩展名的文件名

            # 构建新的文件名
            new_filename = f"{value}-{filename}{ext}"

            # 构建新的文件夹名
            parent_dirname = os.path.basename(dirname)
            if parent_dirname == filename:
                if parent_dirname[:10] == str(value)[:10]:
                    print("dir no need rename")
                else:
                    new_parent_dirname = f"{value}-{parent_dirname}"
                    new_dirpath = os.path.join(os.path.dirname(dirname), new_parent_dirname)
                    os.rename(dirname, new_dirpath)
                    print(f"Renamed directory: {dirname} -> {new_dirpath}")
                    dirname = new_dirpath  # 更新文件夹路径为新的文件夹名
                    filepath = os.path.join(dirname, basename)

            # 构建新的文件路径
            new_filepath = os.path.join(dirname, new_filename)

            # 修改文件名
            if filename[:10] == str(value)[:10]:
                print("file name no need rename")
            else:
                os.rename(filepath, new_filepath)
                print(f"Renamed file: {filepath} -> {new_filepath}")
        else:
            print(f"Property '{property_name}' not found in Front Matter of {filepath}")

def process_directory(dirpath, property_name):
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_markdown_file(filepath, property_name)

if __name__ == "__main__":
    start_dir = '.'  # 开始搜索的目录，当前目录
    property_name = 'date'  # 指定要提取的 Front Matter 属性名

    # 处理目录及其子目录中的 Markdown 文件
    process_directory(start_dir, property_name)
