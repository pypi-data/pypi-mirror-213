import requests
import json
import logging
import timeit



class InternetModule:
    def __init__(self, bot) -> None:
        self.bot = bot

    def get_prompt_wrapper_for_query(self, prompt):
        prompt_wrapper = f'This is a prompt from a user to a chatbot: "{prompt}". Respond with "none" if it is directed at the chatbot or cannot be answered by an internet search. Otherwise, respond with a possible search query to a search engine. Do not write any additional text. Make it as minimal as possible'
        return prompt_wrapper

    def ask_using_internet(self, prompt, role="user", convo_id="search", temperature=0, internet_search_depth=3):
        output, query_time = self._time_function(
            lambda: self._ask_using_internet(prompt, role, convo_id, temperature, internet_search_depth),
        )
        output["query_time"] = query_time
        return output

    def _ask_using_internet(self, prompt, role="user", convo_id="search", temperature=0, internet_search_depth=3):
        output = {}  # Initialize an empty dictionary to store output

        bot = self.bot

        prompt_wrapped = self.get_prompt_wrapper_for_query(prompt)
        query = bot.ask(prompt_wrapped, convo_id="search", temperature=1)
        output["query"] = query
        search_results = '{"results": "No search results"}'
        if query != "none":
            def get_search_results():
                nonlocal search_results
                resp = requests.post(
                    url="https://ddg-api.herokuapp.com/search",
                    json={"query": query, "limit": internet_search_depth},
                    timeout=10,
                )
                resp.encoding = "utf-8" if resp.encoding is None else resp.encoding
                search_results = resp.text

            search_time = self._time_function(get_search_results)

            try:
                logging.info(search_results)  # Print search_results to see the data
                output["search_results"] = json.loads(search_results)
                output["search_time"] = search_time
                bot.add_to_conversation(
                    f"Search results:{search_results}",
                    "system",
                    convo_id="default",
                )
                output["response"] = bot.ask(prompt, "user", convo_id="default")  # Append output to dictionary
            except json.decoder.JSONDecodeError as e:
                logging.error("Error parsing JSON data:", e)
            except StopIteration as e:
                logging.error("StopIteration:", e)
        else:
            output["response"] = self.ask_default(prompt, role, convo_id, temperature)

        return output

    def ask_default(self, prompt, role="user", convo_id="default", temperature=0):
        response, default_time = self._time_function(
            lambda: self.bot.ask(prompt, role=role, convo_id=convo_id, temperature=temperature)
        )
        return {"response": response, "default_time": default_time}

    def _time_function(self, func):
        start_time = timeit.default_timer()
        result = func()
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        return result, elapsed_time