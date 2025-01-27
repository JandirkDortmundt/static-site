from textnode import TextNode, TextType
import os
import shutil
from node_utils import generate_pages_recursive

def main():


    def setup_static_dir():
        public_d = os.path.abspath('.')+"/public"
        static_d = os.path.abspath('.')+"/static"
        #print(f"Contents before deletion: {os.listdir(public_d)}")
        shutil.rmtree(public_d)
        os.makedirs(f"{public_d}", exist_ok=True)
        def get_full_file_list(static_d):
            file_list = []
            for i in os.listdir(static_d):
                if os.path.isfile(static_d + "/" + i):
                    file_list.append(static_d + "/" + i)
                else:
                    file_list.extend(get_full_file_list(static_d + "/" + i))
            return file_list
        files_s = get_full_file_list(static_d)
        # print(f"these are all the files in static: {files_s}")
        files_p = [file.replace("/static/","/public/") for file in files_s]
        directories = list(set([file.rsplit("/",1)[0] for file in files_p]))
        # print(f"these are all the files to be created in plublic: {files_p}")
        # print(f"these are the directories that have to be created: {directories}")

        for dir in directories:
            os.makedirs(dir, exist_ok=True)
        for file_p in files_p:
            shutil.copy(file_p.replace("/public/","/static/"),file_p)
        
        # print(f"Contents after deletion: {os.listdir(public_d)}")
    setup_static_dir()
    
    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "public"

    generate_pages_recursive(dir_path_content,template_path,dest_dir_path)

    


main()

