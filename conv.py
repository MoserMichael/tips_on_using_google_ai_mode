# script for converting LLM saved talks from html to markdown.
# 
# Installation:
#
#    python3 -m venv .venv
#    source .venv/bin/activate
#    pip3 install html-to-markdown
#    pip3 install mistune
#
# repeated usage:
#    source .venv/bin/activate
#
# python conv.py -d dir-name-that-contains-talks-to-llm

import argparse
import sys
import pathlib
from urllib.parse import urlparse
from markdownify import MarkdownConverter
from mistune.renderers.markdown import MarkdownRenderer
import mistune

question_prefix = "Question> "  

def parse_arguments():
    usage = """Convert files from html to markdown.
    Useful when dealing with saved chats to an llm.
    
    Inline images are skipped, so no emojies in the resulting text.
    
    Local links are also removed.
    """

    parser = argparse.ArgumentParser(
        description=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument(
        "-d",
        "--dirname",  #
        help="directory name",
        type=str,
        required=False
    ) 

    parser.add_argument(
        "-f",
        "--fname",  #
        help="file name",
        type=str,
        required=False
    )

    ret = parser.parse_args()

    if ret.dirname == "" or ret.fname == "":
        print("Error: either -d or -f arguments required")
        sys.exit(1)

    return ret

class CustomConverter(MarkdownConverter):

    def convert_span(self, el, text, parent_tags):
        # deepseek
        cl = el.get('role', []) 
        if 'heading' in cl:
            return question_prefix + text

        # google AI mode - https://www.google.com/search?u9dm=50
        cl = el.get('class', []) 
 
        # add question marker in google ai mode
        if  any(it.find('VndcI') != -1 or it.find('veK2kb') != -1 for it in cl): # 'VndcI veK2kb' 
            return question_prefix + text

        return text
 
    def convert_div(self, el, text, parent_tags):

        # deepseek
        # Check for the specific class
        # d29f3d7d ?
        cl = el.get('class', []) 
        if 'fbb737a4' in cl or 'ilZyRc R7mRQb' in cl:
            return question_prefix + super().convert_div(el, text, parent_tags)
        
        return super().convert_div(el, text, parent_tags)

  
    def convert_p(pself, el, text, parent_tags):
        # gemini
        cl = el.get('class', []) 
        if any('query-text' in item for item in cl):
            return question_prefix + super().convert_p(el, text, parent_tags)
        return super().convert_p(el, text, parent_tags)


def conv_to_markdown(html_text):
    #md_text = convert(html_text)
    conv = CustomConverter()
    return conv.convert(html_text)

class RemoveStuffRenderer(MarkdownRenderer):
    # Overriding the image method to return an empty string
    def image(self, token, state):
        return ''

    def link(self, token, state):
        # Extract the URL from the token attributes
        url = token['attrs'].get('url', '')
        
        # Parse the URL to find the hostname (netloc)
        parsed = urlparse(url)
        
        if not parsed.netloc:
            return ""
            #return self.render_children(token, state)
        
        return super().link(token, state)
    
def remove_inline_images_from_markdown(text):
    renderer = RemoveStuffRenderer()
    markdown_parser = mistune.create_markdown(renderer=renderer)

    return  markdown_parser(text)
    
#def filter_out_images(md_text):
#    def is_not_image(line):
#        return not line.startswith("![SVG Image]")
#    return '\n'.join(list(filter(is_not_image, md_text.split('\n'))))

def process_file(fname):

    orig_file = pathlib.Path(fname)
    if not orig_file.exists():
        print(f"Error: file {fname} does not exist")
        return
   
    md_name = str(orig_file.with_suffix(".md"))
    print(f"Converting {fname} to {md_name}")

    with open(fname, 'r') as htm_file:
        html_text = htm_file.read()

        md_text = conv_to_markdown(html_text)
        md_text = remove_inline_images_from_markdown(md_text)

        with open(md_name, 'w') as ofile:
            ofile.write(md_text) 


def process_dir(dname):
    files = pathlib.Path(dname).glob('*.htm?')
    for file in files:
        if file.is_file():
            fname = str(file)
            process_file(fname)

def do_it():
    arg = parse_arguments()
    if arg.dirname:
        dir_full = str(pathlib.Path(arg.dirname).resolve())
        process_dir(dir_full) 
    if arg.fname:
        fname_full = str(pathlib.Path(arg.fname).resolve())
        process_file(fname_full) 

if __name__ == "__main__":        
    do_it()
