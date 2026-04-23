# Google AI mode for privacy aware individuals

<!--
Somehow related link: you can check out my gist on running [Claude locally on the Mac](https://gist.github.com/MoserMichael/8e6dd03acf910b7c4e8f1f51734a94d1)
//-->

Disclaimer: all these observations were made in early 2026. Now all of this is subject to change, in our fast-moving world.

Google AI mode is a really great chat bot. It is giving great answers on both technical questions and questions of a general nature. I am frankly impressed by this milestone of engineering, working at such a huge scale.

Now some google accounts or some locations _don't_ display the option of google ai mode, this guide explains, which google URL parameters will force this feature to appear, and how to customize it via the url parameters.

- To access Google AI mode use the following url: `https://www.google.com/search?udm=50` [link](https://www.google.com/search?udm=50) - this will display the chat window in all locations, even in places where AI mode does not appear as an option on the google search page.
- Additional query parameters `hl=en` if you want to force the UI language and language of the LLM answer to English. `https://www.google.com/search?udm=50&hl=en` [link](https://www.google.com/search?udm=50&hl=en)
- Google ai pro mode. The UI has a pro mode switch, this adds the `arv=1` parameters. Now the full URL for google AI mode, in english and pro mode is `https://www.google.com/search?udm=50&hl=en&arv=1` [link](https://www.google.com/search?udm=50&hl=en&arv=1) 'pro' mode seems to think longer. I am not sure it always returns better results. Mileage may vary.
- Other dorky url parameters: Switching between 'fast' and 'pro' mode will add additional parameters to the url. Note that both versions have common url parameters `aep=1` `ntc=1` `fbs=` - without value. I like to keep my url's short, with minimal URL parameters (the reason: If you have something essential like login session id, then you would probably send this information via http post parameters, and not via url parameter...) 
    - fast mode full url: `https://www.google.com/search?aep=1&ntc=1&fbs=&udm=50`
    - pro mode full url:  `https://www.google.com/search?aep=1&ntc=1&fbs=&udm=50&arv=1`

- while being logged into a google account: `https://myactivity.google.com/myactivity?product=83` - gives you the history of your past discussions with Google AI mode. 

## what is going on here?

 Google in AI mode uses a model from the [Gemini language model](https://en.wikipedia.org/wiki/Google_Gemini), it is similar to what you get in [https://gemini.google.com](https://gemini.google.com), however there are differences:

- AI mode is using [Query fan-out](https://blog.google/products-and-platforms/products/search/google-search-ai-mode-update/). This means that the chatbot derives its information from the results of a large number of regular google search queries. These queries are launched and analyzed by the chatbot, with the purpose of gathering information for answering questions. 
- The query Fan-out process seems to be based on US Patent [Generating query variants using a trained generative model](https://patents.google.com/patent/US11663201B2/en) - says [searchengineland](https://searchengineland.com/guide/query-fan-out). Here: 
    - A 'Controller engine' agent is maintaining the conversation with the client as well as formulating the general question / determining if he answer is of sufficient quality, and if the quality is not sufficient then ask additional questions.
    - A 'Variant engine' is an agent that is reformulating the original question into multiple simple search queries, and forwarding them to an automated search tool
    - 'Search tool' is performing the parallel search & retrieval of the internet queries, which includes reading the text of the resource returned by the search. 
    - Some component needs to sum up the result of the search queries, so that the 'Controller engine' will be able to produce an answer. not clear if that is a separate agent or the 'Controller engine' agent.
- In comparison with gemini: Google in AI mode is also more likely to cite the sources for it's answers. This is quite important: a chatbot gives more accurate answers and is less likely to hallucinate, if it is working in such a manner. 
- I like that AI mode has a more direct / less sycophantic style of communication, compared to Gemini (somehow this got worse, i n recent months...) 

Google in AI mode has a shorter context window, compared to google gemini. This means that AI mode is not the right tool to conduct a long chat session that tries to research a complex topic very deeply. If you try to conduct a long chat session with many questions and answer, then you will notice that google in AI mode does not remember what it talked about earlier. However it is great for fact based questions and answers - exactly what you would expect from an intelligent search engine.  

Another disadvantage: you can't set your own system prompt with google ai mode. It might be, that query fan-out is requiring a specialized system prompt.

There is actually a git repository with leaked system prompts. It lists the following [system prompt for Google AI mode](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Google/google-search-ai-mode.md)

This seems to be the prompt of he customer facing 'Controller engine', as that is the agent exposed directly to the user.

The prompt has some general advice on using the search tool, image search tool and python evaluation environment.

-----
"""
**General rules for using the search tool:**
- **Prefer simpler queries with the search tool:** the tool is meant to provide data for simple queries.
- Complex questions should be broken down into a series of simpler queries. Do not simply forward the complex query to the tool. 
- Prefer starting with the most useful and diverse set of queries first.
- You do not need to use the search tool to identify the user query, search tool will provide you the results of the user query automatically. """
-----

The first two items indicate, that breaking down of the question into several easier internet search queries is done by the main 'Controller engine' agent, and not by a separate 'Variant engine'. 

As well as guidelines on style 

-----
You are an authentic, adaptive collaborator. 

Your goal is to address the user's true intent with insightful, yet clear and concise responses—like a helpful peer, not a rigid lecturer. Subtly adapt your tone, energy, and humor to the user's style. Use simple, everyday words unless the topic requires technical terms. Be succinct. If the query refers to a single fact, respond directly. Do not use ancillary facts from context to formulate a response.
-----

and guidelines on how to approach the task of answering the question


-----
"""
**Always analyze the full conversation history before responding to the latest user query.** Your primary task is to identify and understand the relationship between the user's most recent query and the preceding turns of the conversation.

1. **Identify context:** Thoroughly examine the previous messages to establish the key topics, entities, and any specific items discussed.
2. **Find the link:** Determine if the latest query directly relates to or builds upon the established conversational context.
3. **Focused response:**
   - If a clear topical connection exists: Your response needs to be focused on addressing the latest query within the specific context established in the conversation history. Do not introduce or discuss topics, products, or variations outside this established context.
   - If no clear connection exists: Address the latest query directly and independently.

Your response should be consistent, relevant, and directly address the user's need as informed by the ongoing conversation. End your full response with a single, proactive follow-up that either proposes a specific way to proceed or requests a critical detail to advance the conversation. Use markdown **bolding** on key terms to make it scannable.
"""
-----

Now the search tools is the component that is sending the regular internet search requests, and which is reading the responses. This component is the real enigma here. There remain questions:


- Is there an additional component for breaking up the question into simpler queries? The leaked prompt seems to indicate that this is not the case here.
- how many search results are processed for each query?
- Are the search results summed up by another LLM instance, before they get passed on the main LLM instance? This makes sense: the context of an LLM window is limited, it has to maintain the conversation with the user and figure out the intent of the current question, with relation to previous questions. It would make sense to separate summing up of search results into a different agent.
- to what extent are additional queries dispatched, based on the result of the initial internet search?

## Alternative options:

The brave search engine also has a similar chat bot in query fan-out mode. 

See link [https://search.brave.com/ask?q=&source=llmSuggest](https://search.brave.com/ask?q=&source=llmSuggest)

Also I have started to use regular brave search [https://search.brave.com/](https://search.brave.com/) - its sometimes a close competition for google, if you ask me! 

--

Other chat agents like ChatGTP or DeepSeek all seem to implement some variant of query fan-out, as described in the previous section. 

The improvement in accuracy and relevance of AI based systems seem to be related to the introduction of agentic workflows. With an agentic workflows, the original task is broken up into a pipeline of steps, where each step is run by a specialized language model instance with its own context window. This improves the focus of each sub-components on its particular task.

Query fan-out is a very good example for such a workflow, presumably.

## Now where is the problem? 

I think the nature of your interactions with Google in AI mode is giving away quite a lot of information about you and your work. All this information is stored by the google empire and analyzed later on.

The result: Google will be able to get a better idea on who you are and what you do. Some people view this as an invasion of privacy.

The good thing: Google in AI mode can currently be used without being logged into a google account. For example you can use it from a 'Private window' in firefox. This gives google less information on how to connect the dots. This project gives some advise how to do that.

Also: you can store your chat session as HTML files, here with this project you get a tool to export the chat session into markdown file. Markdown is a format that is very close to text where you can look at meaningful text!

## Cyberpunkies, let's roll!

- General advise: use Firefox. Google Chrome has the 'incognito mode' feature, however it turns out that this is [not very incognito](https://www.nytimes.com/wirecutter/blog/incognito-mode-isnt-incognito/)

 (Why do they allow access to gemini in incognito mode? Now maybe they are counting on fingerprinting, so as to identify the customer by means of fingerprinting. Maybe it is time for me to learn more about fingerprinting techniques...)

- To use google AI mode with Firefox:
    - Open the file menu 
    - choose 'New Private Windows' from the menu.
    - now use the following URL to to access the AI mode `https://www.google.com/search?udm=50`
    - Remember that the chat session is gone, once you have closed the browser window. You can save the chat session as an html file, with the 'Save As' option in the 'File' menu.


## Command line tool for asking single questions


```
./ask_google_aimode.py -q 'meaning on life, the universe and everything'
```

Will ask a question via chromium browser and presents you with a json formatted output. This script does not depend on any scraping services, if it works.
(all you need for this is chromium browser, selenium base and beautiful soup4 python packages)

Warning: This program works a couple of time, then google decides that the same ip address is generating unusual traffic and starts a re-captcha. BeautifulSoup4 with Selenium have limited ability to solve re-captcha challenges.

All such web scraping efforts break at some point, it's a cat and mouse game. You will need ip address randomization for such a trick, otherwise re-captchas will stop it.

Also the trick to avoid browser scraping: the prompt of the script asks for an xml formatted response, and searches for the text in the xml response.

## Now a digression

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

Next you are down and out, and with that the realization that 'you've got no secrets to conceal'.

How as I understand it: You are essentially transparent, once the experienced counterpart knows everything about you - and with full knowledge comes full power and full leverage over your small world.

```
When you ain't got nothing, you got nothing to lose
You're invisible now, you've got no secrets to conceal

How does it feel, ah how does it feel?
To be on your own, with no direction home
Like a complete unknown, like a rolling stone
```

In this interpretation _privacy_ means something bigger, it's a prerequisite for _agency_ - the ability to act on your own.

Here is the [full text](https://www.bobdylan.com/songs/rolling-stone/)
