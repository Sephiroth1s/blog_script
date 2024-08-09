import os
import frontmatter
import re
import random
import ruamel.yaml
from ruamel.yaml.compat import StringIO
def extract_image_links_from_md(md_content):
    # 正则表达式匹配 Markdown 图片链接
    pattern = r"!\[[^\]]*\]\(([^)]+)\)"
    matches = re.findall(pattern, md_content)
    return [match for match in matches if match.startswith("http")]

def select_thumbnail_image(image_links):
    # 如果有多个图片链接，随机选择一个
    if len(image_links) > 1:
        return random.choice(image_links)
    # 如果只有一个图片链接，直接返回
    elif image_links:
        return image_links[0]
    # 如果没有图片链接，返回空字符串
    else:
        return ""

def update_thumbnail_in_md_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)

                # 读取 Markdown 文件
                with open(filepath) as f:
                    post = frontmatter.load(f)
                 
                # 使用 frontmatter.load(f) 分离出 front matter 和 Markdown 内容
                fm_metadata = post.metadata
                # 检查 front matter 是否为空
                if not fm_metadata:
                    print(f"Skipping {filename} because the front matter is empty.")
                    continue
                fm_content = post.content

                # 检查是否存在 thumbnail 属性
                if 'thumbnail' in fm_metadata:
                    # 提取当前文件中的所有图片链接
                    image_links = extract_image_links_from_md(fm_content)
                    thumbnail = select_thumbnail_image(image_links)

                    # 更新 thumbnail 属性 frontmatter的方便写法
                    post['thumbnail'] = thumbnail

                # 合并 front matter 和 Markdown 内容
                # 在 YAML front matter 和 Markdown 内容之间添加两个换行符
                # 确保前front matter和md文本包含两个换行符
                # 能识别出front matter和md内容已经包含了一个换行符了
                fm_content = '\n' + fm_content.lstrip()

                # 标准化yaml
                yaml = ruamel.yaml.YAML()
                yaml.preserve_quotes = True  # 保留原有的引号
                yaml.width = 1000  # 设置宽度，防止自动换行
                yaml.indent(mapping=2, sequence=4, offset=2)  # 设置缩进
                
                # 使用 ruamel.yaml 将字典转换为 YAML 格式的字符串
                fm_dict = post.metadata
                print(dict(fm_dict))
                stream = StringIO()
                yaml.dump(fm_dict,stream)
                yaml_content = stream.getvalue()
                updated_content = '---\n' + yaml_content + '---\n' + fm_content
                # updated_content = frontmatter.dumps(post, handler=yaml)

                # 写回更新后的文件
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(updated_content)

# 调用函数
if __name__ == "__main__":
    update_thumbnail_in_md_files('./')