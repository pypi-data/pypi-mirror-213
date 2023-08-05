
# -*- coding: utf-8 -*-


from langchain.memory import ConversationBufferMemory

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from typing import Any, Dict, Optional



class LangChain:

    api_token: str
    conversation: ConversationChain
    llm: OpenAI

    template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

Human: {human_input}
Assistant:"""

    def __init__(self, api_token: Optional[str] = None, **kwargs,):
        self.api_token = api_token or None
        self.llm = OpenAI(openai_api_key=self.api_token, temperature=0, max_tokens=512)
        prompt = PromptTemplate(
            input_variables=["human_input"], 
            template=self.template
        )
        chatgpt_chain = LLMChain(
            llm=self.llm, 
            prompt=prompt, 
            verbose=True, 
            memory=ConversationBufferWindowMemory(k=2),
        )

        self.conversation =  chatgpt_chain

    def __call__(self, prompt: str, **kwargs) -> str:
        return self.conversation.predict(human_input=prompt)


