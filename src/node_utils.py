from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
import re
import os

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode instance.")

    tag_map = {
        TextType.TEXT: None,
        TextType.BOLD: "b",
        TextType.ITALIC: "i",
        TextType.CODE: "code",
        TextType.LINKS: "a",
        TextType.IMAGES: "img",
    }
    tag = tag_map.get(text_node.text_type)

    props = {}
    if text_node.text_type == TextType.LINKS and text_node.url:
        props["href"] = text_node.url
    elif text_node.text_type == TextType.IMAGES and text_node.url:
        props["src"] = text_node.url
        props["alt"] = text_node.text
        return LeafNode(value="",tag=tag,props=props)

    return LeafNode(value=text_node.text, tag=tag, props=props)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    # delimiter_map = {
    #     "**": TextType.BOLD,
    #     "*": TextType.ITALIC,
    #     "`": TextType.CODE,
    # }

    for node in old_nodes:
        #print(node.__repr__())
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: Unmatched {delimiter} in '{node.text}'")


        for index, part in enumerate(parts):
            if index % 2 == 0:
                if part:
                    if index % 2 == 0:
                        new_node_list.append(TextNode(part,TextType.TEXT))
            else:
                new_node_list.append(TextNode(part,text_type))

    return new_node_list

# def extract_markdown_images(text):
#     matches = re.findall(r'\[(.*?)\]|\((.*?)\)',text)
#     def extract_tuples(matches):
#         if len(matches) < 2:
#             return []
#         tuples_list = [(matches[0], matches[1])]
#         return tuples_list + extract_tuples(items[1:])
#     if len(matches) % 2 == 0:
#         return extract_tuples(matches)
#     else:
#         raise Exception(f"Odd amount of items found in text")
#
#
# def extract_markdown_links(text):
#     matches = re.findall(r'\[(.*?)\]|\((.*?)\)',text)
#     def extract_tuples(matches):
#         if len(matches) < 2:
#             return []
#         tuples_list = [(matches[0], matches[1])]
#         return tuples_list + extract_tuples(items[1:])
#     if matches:
#         return extract_tuples(matches)
#     else:
#         raise Exception(f"Odd amount of items found in text")


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if not images:
            new_node_list.append(node)
            continue
        
        current_text = node.text
        for image_alt, image_link in images:
            parts = current_text.split(f"![{image_alt}]({image_link})", 1)
            
            if parts[0]:
                new_node_list.append(TextNode(parts[0], TextType.TEXT))
            
            new_node_list.append(TextNode(image_alt, TextType.IMAGES, image_link))
            
            if len(parts) > 1:
                current_text = parts[1]
            else:
                break
        
        if current_text:
            new_node_list.append(TextNode(current_text, TextType.TEXT))
    
    return new_node_list

def split_nodes_link(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if not links:
            new_node_list.append(node)
            continue
        
        current_text = node.text
        for link_text, link_url in links:
            parts = current_text.split(f"[{link_text}]({link_url})", 1)
            
            if parts[0]:
                new_node_list.append(TextNode(parts[0], TextType.TEXT))
            
            new_node_list.append(TextNode(link_text, TextType.LINKS, link_url))
            
            if len(parts) > 1:
                current_text = parts[1]
            else:
                break
        
        if current_text:
            new_node_list.append(TextNode(current_text, TextType.TEXT))
    
    return new_node_list


def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]

    node_list = split_nodes_link(node_list)
    node_list = split_nodes_image(node_list)
    
    delimiter_map = {
        "**": TextType.BOLD,
        "*": TextType.ITALIC,
        "`": TextType.CODE,
    }
    for delimiter, text_type in delimiter_map.items():
        node_list = split_nodes_delimiter(node_list, delimiter, text_type)
    
    return node_list

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = list(filter(None,blocks))
    blocks = [block.strip() for block in blocks]
    return blocks


def block_to_block_type(block):
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return 'quote'
    if lines[0] == '```' and lines[-1] == '```':
        return 'code'
    if all(line.startswith('* ') or line.startswith('- ') for line in lines):
        return 'unordered_list'
    if all(line.startswith(f'{i+1}. ') for i, line in enumerate(lines)):
        return 'ordered_list'
    if (block.startswith('#') and block[0:6].count('#') <= 6 and block[len(block.split()[0])] == ' '):
        return 'heading'
    return 'paragraph'

def create_html_children(text_nodes):
    return [text_node_to_html_node(node) for node in text_nodes]

def proper_parent_node(block_type, block):
    if block_type == 'paragraph':
        html_children = create_html_children(text_to_textnodes(block))
        return ParentNode('p', html_children)
    elif block_type == 'heading':
        html_children = create_html_children(text_to_textnodes(block.lstrip('#').strip()))
        heading_level = block[0:6].count('#')
        return ParentNode(f'h{heading_level}', html_children)
    elif block_type == 'quote':
        html_children = create_html_children(text_to_textnodes(block.lstrip('>').strip()))
        return ParentNode('blockquote', html_children)
    elif block_type == 'code':
        # Remove backticks and strip whitespace
        clean_block = block.strip('`').strip()
        text_nodes = text_to_textnodes(clean_block)
        html_children = create_html_children(text_nodes)
        return ParentNode('pre', [ParentNode('code', html_children)])
    elif block_type == 'unordered_list':
        list_items = []
        for line in block.split('\n'):
            if line.startswith("* "):
                clean_line = line.lstrip("* ").strip()
            elif line.startswith("- "):
                clean_line = line.lstrip('- ').strip()
            text_nodes = text_to_textnodes(clean_line)
            html_children = create_html_children(text_nodes)
            list_item = ParentNode('li', html_children)
            list_items.append(list_item)
        return ParentNode('ul', list_items)
    elif block_type == 'ordered_list':
        list_items = []
        for line in block.split('\n'):
            clean_line = line.split('. ', 1)[1].strip()
            text_nodes = text_to_textnodes(clean_line)
            html_children = create_html_children(text_nodes)
            list_item = ParentNode('li', html_children)
            list_items.append(list_item)
        return ParentNode('ol', list_items)



# def proper_parent_node(block_type, block):
#     if block_type == 'paragraph':
#         html_children = create_html_children(text_to_textnodes(block))
#         return ParentNode('p', html_children)
#     elif block_type == 'heading':
#         html_children = create_html_children(text_to_textnodes(block))
#         heading_level = block[0:6].count('#')
#         return ParentNode(f'h{heading_level}', html_children)
#     elif block_type == 'quote':
#         html_children = create_html_children(text_to_textnodes(block))
#         return ParentNode('blockquote', html_children)
#     elif block_type == 'code':
#         clean_block = block.strip('`')
#         html_children = create_html_children(text_to_textnodes(block))
#         return ParentNode('code',ParentNode('pre',html_children))
#     elif block_type == 'unordered_list':
#         list_items  = []
#         for line in block.split('\n'):
#             clean_line = line[2:]
#             text_nodes = text_to_textnodes(clean_line)
#             html_children = create_html_children(text_nodes)
#             list_item = ParentNode('li', html_children)
#             list_items.append(list_item)
#         return ParentNode('ul', list_items)
#     elif block_type == 'ordered_list':
#         list_items  = []
#         for line in block.split('\n'):
#             clean_line = line[2:]
#             text_nodes = text_to_textnodes(clean_line)
#             html_children = create_html_children(text_nodes)
#             list_item = ParentNode('li', html_children)
#             list_items.append(list_item)
#         return ParentNode('ol', list_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        parent = proper_parent_node(block_type, block)
        children.append(parent)
    
    return ParentNode('div', children)

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# ") and len(line) > 2:
            return line[2:].strip()
    raise Exception("No H1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(os.path.abspath('.')+"/"+from_path, "r") as file:
        markdown = file.read()
    html_nodes = markdown_to_html_node(markdown)
    html_code = html_nodes.to_html()
    # html_code = ""
    # for node in html_nodes:
    #     html_code += node.to_html()

    title = extract_title(markdown)

    with open(os.path.abspath('.')+"/"+template_path, "r") as file:
        template = file.read()
    template = template.replace("{{ Title }}",title)
    template = template.replace("{{ Content }}",html_code)

    with open(os.path.abspath('.')+"/"+dest_path,'w') as file:
        file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_d = os.path.abspath('.') + "/" + dir_path_content
    public_d = os.path.abspath('.') + "/" + dest_dir_path

    def get_full_file_list(content_d):
        file_list = []
        for i in os.listdir(content_d):
            if os.path.isfile(content_d+ "/" + i):
                file_list.append(content_d+ "/" + i)
            else:
                file_list.extend(get_full_file_list(content_d+ "/" + i))
        return file_list

    files = get_full_file_list(content_d)
    print(f"these are all the files in content: {files}")
    files = [file for file in files if file.endswith(".md")]
    if files:
        files_p = [file.replace(f"/{dir_path_content}/",f"/{dest_dir_path}/") for file in files]
        directories = list(set([file.rsplit("/",1)[0] for file in files_p]))
        print(f"these are all the files to be created in public: {files_p}")
        print(f"these are the directories that have to be created: {directories}")
        for dir in directories:
            os.makedirs(dir, exist_ok=True)

        for file in files:
            with open(file, "r") as file_r:
                markdown = file_r.read()
            html_nodes = markdown_to_html_node(markdown)
            html_code = html_nodes.to_html()

            title = extract_title(markdown)

            with open(os.path.join(os.path.abspath('.'),template_path), "r") as file_r2:
                template = file_r2.read()
            template = template.replace("{{ Title }}",title)
            template = template.replace("{{ Content }}",html_code)
            file = file.replace(".md",".html")
            with open(file.replace(f"/{dir_path_content}/",f"/{dest_dir_path}/"),'w') as file:
                file.write(template)

    else:
        raise Exception("no markdown files found")

