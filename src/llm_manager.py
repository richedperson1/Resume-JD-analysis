#^  Library importing
from langchain_openai import AzureChatOpenAI
import httpx
from dotenv import load_dotenv
import os
env_path = os.path.join(os.path.dirname(__file__),"./config/.env")
load_dotenv(env_path)

class openai_llm:
    """
    Custom OpenAI Large Language Model (LLM) interface class.
    """

    llm_list:dict = {}

    @classmethod
    def get_llm_instance(cls,**kwargs):
        """
        Retrieves an LLM instance by its deployment name.
        
        Args:
            model_name (str): The deployment name of the LLM instance.
        
        Returns:
            The LLM instance if it exists, otherwise a string indicating that the model was not loaded.
        """
        model_name = kwargs.get("model_name","gpt-4o")
        temperature = kwargs.get("temperature",0.2)
        if (model_name,temperature) in cls.llm_list:
            return cls.llm_list[(model_name,temperature)]
        else:
            initilize_model = cls.initilize_llm(model_name = model_name,temperature = temperature)
            if isinstance(initilize_model,str):
                return "Not able to load LLM"
            return initilize_model
        
    @classmethod    
    def initilize_llm(cls,**kwargs):
        """
        Initializes an LLM instance using the given deployment name.
        
        Args:
            deployment_name (str): The deployment name of the LLM instance.
        
        Returns:
            The initialized LLM instance if successful, otherwise a string indicating that the model was not loaded.
        """
        try:
            deployment_name = kwargs.get("model_name")
            temperature = kwargs.get("temperature")
            azure_gpt_model = AzureChatOpenAI(azure_deployment=deployment_name,
                                              streaming=True,
                                              temperature=temperature,
                            http_client=httpx.Client(verify=False))
            cls.llm_list[(deployment_name,temperature)] = azure_gpt_model
            print("model get loaded")
            return azure_gpt_model

        except Exception as err:
            print(f"Model {deployment_name} can't be loaded due to {err}")
            return f"Model {deployment_name} can't be loaded due to {err}"