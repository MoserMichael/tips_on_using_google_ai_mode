# Google AI mode for privacy aware individuals

Disclaimer: all these observations were made in early 2026. Now all of this is subject to change, in our fast-moving world.

Google AI mode is a really great chat bot. It is giving great answers on both technical questions and questions of a general nature. I am frankly impressed by this milestone of engineering, working at such a huge scale.

- To access Google AI mode use the following url: `https://www.google.com/search?udm=50` [link](https://www.google.com/search?udm=50) - this will display the chat window in all locations, even in places where AI mode does not appear as an option on the google search page.
- Additional query parameters `hl=en` if you want to force the UI language and language of the LLM answer to English. `https://www.google.com/search?udm=50&hl=en` [link](https://www.google.com/search?udm=50&hl=en)
 Google in AI mode uses the [Gemini language model](https://en.wikipedia.org/wiki/Google_Gemini), it is similar to what you get in [https://gemini.google.com](https://gemini.google.com), however there are differences:
    - AI mode is using [Query fan-out](https://blog.google/products-and-platforms/products/search/google-search-ai-mode-update/). This means that the chatbot derives its information from the results of a large number of regular google search queries. These queries are launched and analyzed by the chatbot, with the purpose of gathering information for answering questions. 
    - In comparison with gemini: Google in AI mode is also more likely to cite the sources for it's answers. This is quite important: a chatbot gives more accurate answers and is less likely to hallucinate, if it is working in such a manner. 
    - I like that AI mode has a more direct / less sycophantic style of communication, compared to Gemini. 
    - The UI of AI mode does not keep a history of your chats, unlike what you get with gemini. So you can't easily return to a previous chat and continue it.

Google in AI mode has a shorter context window, compared to google gemini. This means that AI mode is not the right tool to conduct a long chat session that tries to research a complex topic very deeply. If you try to conduct a long chat session with many questions and answer, then you wil notice that google in AI mode does not remember what it talked about earlier. However it is great for fact based questions and answers - exactly what you would expect from an intelligent search engine.  

### Now where is the problem? 

I think the nature of your interactions with Google in AI mode is giving away quite a lot of information about you and your work. All this information is stored by the google empire and analyzed later on.

The result: Google will be able to get a better idea on who you are and what you do. Some people view this as an invasion of privacy.

The good thing: Google in AI mode can currently be used without being logged into a google account. For example you can use it from a 'Private window' in firefox. This gives google less information on how to connect the dots. This project gives some advise how to do that.

Also: you can store your chat session as HTML files, here with this project you get a tool to export the chat session into markdown file. Markdown is a format that is very close to text where you can look at meaningful text!

### Cyberpunkies, let's roll!

- General advise: use Firefox. Google Chrome has the 'incognito mode' feature, however it turns out that this is [not very incognito](https://www.nytimes.com/wirecutter/blog/incognito-mode-isnt-incognito/)

- To use google AI mode with Firefox:
    - Open the file menu 
    - choose 'New Private Windows' from the menu.
    - now use the following URL to to access the AI mode `https://www.google.com/search?udm=50`
    - Remember that the chat session is gone, once you have closed the browser window. You can save the chat session as an html file, with the 'Save As' option in the 'File' menu.

### Converting saved html sessions to markdown

You get a command line tool for converting the html file to markdown format. I think it is important to keep notes in a textual format, as that is the only way to search through the notes. HML has a very complicated structure, where most of the volume is about the formatting of the text. Tou can't quite 'touch' the text that it includes.

Now Here you have two ways to run the html to markdown transformation script - as shell script that runs a docker container, or by running the python script.

What does the html to markdown converter do? 

The script inserts a marker, to distinguish the question from the answer. Is also removes links to google services and it is removing images, so you get your text only, and links to the cited sources.
images.

### Running as a docker container

You need to have docker desktop installed and running on your laptop

Installation: 

- download the shell script from this link [link to script](https://raw.githubusercontent.com/MoserMichael/tips_on_using_google_ai_mode/refs/heads/main/run_llm.sh)
- make the downloaded script executable `chmod +x run_llm.sh`

Usage:

- convert a single file `./run_llm.sh -f ~/Downloads/saved-chat-session.htm` this adds the file `~/Downloads/saved-chat-session.htm`
- convert all files in a given directory `./run_llm.sh -d  ~/directory-with-stored-sessions` 

### Running the python script

Installation:

- Download the python script file conv.py [link to python script](https://raw.githubusercontent.com/MoserMichael/tips_on_using_google_ai_mode/refs/heads/main/conv.py)
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


-----

### Now a digression

I somehow got convinced, that privacy isn't a luxury - it's a basic necessity.

Look at the song ['Like a Rolling Stone'](https://www.youtube.com/watch?v=IwOfCgkyEj0) by Bob Dylan

I am probably misinterpreting the whole thing; Still: I think it is recalling the story of a downfall: 

At first there is the attempt to negotiate: 

```
He's not selling any alibis
As you stare into the vacuum of his eyes
And say do you want to make a deal?
```

Then comes the realization of an inevitable outcome

```
Ain't it hard when you discovered that
He really wasn't where it's at
After he took from you everything he could steal
```

Next you are down and out, and with that the realization that 'you've got no secrets to conceal'

```
When you ain't got nothing, you got nothing to lose
You're invisible now, you've got no secrets to conceal

How does it feel, ah how does it feel?
To be on your own, with no direction home
Like a complete unknown, like a rolling stone
```

Here is the [full text](https://www.bobdylan.com/songs/rolling-stone/)