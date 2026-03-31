import argparse
from urllib.parse import quote
from seleniumbase import SB
from bs4 import BeautifulSoup
import json
import sys

def parse_cli():
    parser = argparse.ArgumentParser(description="A simple string-parsing script")

    parser.add_argument('-q', "--query", type=str, help="The text query to process", required=True)

    return parser.parse_args()

def show_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


def find_tags(otext, start_tag, end_tag):
    rpos = otext.rfind(start_tag)
    rpos_end = otext.rfind(end_tag)
    if rpos != -1 and rpos_end != -1:
        return otext[ rpos+len(start_tag) : rpos_end ]
    return ""


def extract_answer(query, otext):
    concise_a = find_tags(otext,'<concise_answer>', '</concise_answer>')
    full_a =  find_tags(otext,'<full_answer>', '</full_answer>')
    return { 'query': query, 'one_line': concise_a, 'full_answer': full_a}

def try_it():
    with open('txt.html','r') as infile:
        in_text = infile.read()
        otext = show_text(in_text)
        dump_it("txt.txt", otext)
        answer_map = extract_answer('lala',otext)
        print(json.dumps(answer_map, indent=4))

def run_query(question):

    prompt=f"""{question}. Write your complete answer in the following xml format: <answer><concise_answer>one line answer</concise_answer><full_answer>your full answer</full_answer></answer>"""

    query = f"https://google.com/search?udm=50&hl=en&q={quote(prompt)}"

   
    with SB(uc=True, use_chromium=True, headless=True) as sb:
        # Use 'uc_open_with_reconnect' for the most aggressive stealth
        sb.uc_open_with_reconnect(query, 4)

        # Wait for a human-like duration to avoid rate-limiting
        sb.sleep(2)

        html = sb.get_page_source()
        return html
    return ""

def dump_it(fname, text):
    with open(fname,'w') as ofile:
        ofile.write(text)

def do_it():
    args = parse_cli()
    in_html = run_query(args.query)
    
    #dump_it("txt.html", in_html)

    otext = show_text(in_html)
    
    #dump_it("txt.txt", otext)
    
    answer_map = extract_answer(args.query, otext)
    print(json.dumps(answer_map, indent=4))

if __name__ == "__main__":
    do_it()
