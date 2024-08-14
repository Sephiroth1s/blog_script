import re
import requests
import os
import argparse

# Piclist API的基础URL和API密钥（请替换为实际的API密钥）
PICLIST_API_URL = 'http://127.0.0.1:36677/upload'
API_KEY = ''

def upload_image_to_piclist(image_path):
    with open(image_path, 'rb') as file:
        files = {'file': file}
        headers = {'Authorization': f'Bearer {API_KEY}'}
        data={
            "list":image_path
        }
        response = requests.post(PICLIST_API_URL, files=files, headers=headers)
        if response.status_code == 200:
            return response.json()['result'][0]
        else:
            print(f"Failed to upload image: {response.text}")
            return ""
            raise Exception(f"Failed to upload image: {response.text}")

def replace_image_links(markdown_text, base_path):
    # 匹配本地图片链接 ![alt text](image_path)
    image_pattern = r'!\[.*?\]\((?!http).*?\)'
    matches = re.findall(image_pattern, markdown_text)
    
    for match in matches:
        # 提取md图片链接中的()内容，并去除有可能的字符串两端空格
        match_pic = re.search(r'\(([^)]+)\)', match)
        if match_pic:
            ori_name = image_path = match_pic.group(1)
        else:
            continue
        # 去除路径中前后空格，防止后面的文件判断出错
        image_path = image_path.strip()
        # 判断是否绝对路径
        if not os.path.isabs(image_path):
            image_path = os.path.join(base_path, image_path)
        
        if os.path.isfile(image_path):
            # 上传图片到Piclist并获取新的URL
            new_url = upload_image_to_piclist(image_path)
            if new_url :
                new_url = match.replace(ori_name,new_url)
            else:
                continue
            # 替换旧的图片路径为新的URL
            markdown_text = markdown_text.replace(match, new_url)
    
    return markdown_text

def main(input_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取输入文件名
    input_filename = os.path.basename(input_file)
    base_path = os.path.dirname(input_file)
    output_file = os.path.join(output_folder, input_filename)
    
    # 读取Markdown文件
    with open(input_file, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    
    # 替换图片链接
    new_markdown_text = replace_image_links(markdown_text, base_path)
    
    # 将新的Markdown文本写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_markdown_text)
    
    print(f"图片链接替换完成！文件已保存至：{output_file}")
    
def process_directory(dirpath, output_folder):
    if os.path.isfile(dirpath):
        if dirpath.endswith('.md'):
            main(dirpath, output_folder)
    else:
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    main(filepath, output_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='处理Markdown文件中的图片链接并上传到Piclist')
    parser.add_argument('input_file', type=str, help='需要处理的Markdown文件路径')
    parser.add_argument('output_folder', type=str, help='导出路径')
    args = parser.parse_args()
    
    process_directory(args.input_file, args.output_folder)
