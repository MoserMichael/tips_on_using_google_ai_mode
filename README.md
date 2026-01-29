# Google AI mode for privacy aware individuals

Google AI mode is a really great chat bot. It is giving great answers on both technical questions and questions of a general nature. I am frankly impressed by this milestone of engineering, working at such a huge scale.

- To access Google AI mode use the following url: `https://www.google.com/search?udm=50` [link](https://www.google.com/search?udm=50) - this will display the chat session in all locations, even in places where AI mode does not appear on the google search page.
- Google in AI mode uses the [Gemini language model](https://en.wikipedia.org/wiki/Google_Gemini), it is similar to what you get in [https://gemini.google.com](https://gemini.google.com), however there are differences:
    - AI mode is using [Query fan-out](https://blog.google/products-and-platforms/products/search/google-search-ai-mode-update/). This means that the chatbot derives its information from the results of a large number of regular google search queries. These queries are launched and analyzed by the chatbot, on the bases of the current chat session. 
    - In comparison with gemini: Google in AI mode is also more likely to cite tje sources for it's answers. This is quite important: a chatbot gives more accurate answers and is less likely to hallucinate, if it is working in such a manner.
    - The UI of AI mode does not keep a history of your chats, unlike what you get with gemini. So you can't easily return to a previous chat and continue it.

### Now where is the problem? 

I think the nature of your interactions with Google in AI mode is giving away quite a lot of information about you and your work. All this information is stored by the google empire and analyzed later on.

The result of this is that the platform will be able to get a better idea on who you are and what you do. Some people view this as an invasion of privacy.

The good thing: Google in AI mode can currently be used without being logged into aa google account. For example you can use it from a 'Private window' in firefox. This gives google less information on how to connect the dots. This project gives some advise how to do that.

Also: you can store your chat session as HTML files, here with this project you get a tool to export the chat session into markdown file. Markdown is a format that is very close to text where you can look at meaningful text!

### Cyberpunkies, lets' roll!

- General advise: use Firefox for privacy. Google Chrome has the 'incognito mode' feature, however it turns out that this is [not very incognito](https://www.nytimes.com/wirecutter/blog/incognito-mode-isnt-incognito/)

- To use google AI mode with Firefox:
    - press on the three dots on the right side of the toolbar
    - choose 'New Incognito Windows' from the menu.
    - now use the following URL to to access the AI mode `https://www.google.com/search?udm=50`

### Converting saved html sessions to markdown

You get a command line tool for converting the html file to markdown format. Now there are two ways to run that, as shell script that runs a docker container, or by running the script.

### running as a docker container

You need to have docker desktop installed and running on your laptop

Installation: 

- download the shell script from this link, 
- make the downloaded script executable `chmod +x run_llm.sh`

Usage:

- convert a single file `./run_llm.sh -f ~/Downloads/saved-chat-session.htm` this adds the file `~/Downloads/saved-chat-session.htm`
- convert all files in a given directory `./run_llm.sh -d  ~/directory-with-stored-sessions` 

### running the python script

Installation:

- Download the python script file conv.py
- create a virtual environment and install the required libaries
```
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install html-to-markdown
    pip3 install mistune
```

Usage:

- activate the virtual environment `source .venv/bin/activate`
- convert a single file `python conv.py -f ~/Downloads/saved-chat-session.htm` this adds the file `~/Downloads/saved-chat-session.htm`
- convert all files in a given directory `python conv.py -d  ~/directory-with-stored-sessions` 



U