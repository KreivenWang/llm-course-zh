from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM
from langchain.tools import tool # Example Tool

# 模拟公司产品和公司介绍的数据源
class TeslaDataSource:
    # 定义了LLM的Prompt Template
    CONTEXT_QA_TMPL = """
    根据以下提供的信息，回答用户的问题
    信息：{context}

    问题：{query}
    """
    CONTEXT_QA_PROMPT = PromptTemplate(
        input_variables=["query", "context"],
        template=CONTEXT_QA_TMPL,
    )

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    # 工具1：产品描述
    def find_product_description(self, product_name: str) -> str:
        """
        返回产品的描述和定价信息。
        """
        product_info = {
            "Model 3": "具有简洁、动感的外观设计，流线型车身和现代化前脸。定价23.19-33.19万",
            "Model Y": "在外观上与Model 3相似，但采用了更高的车身和更大的后备箱空间。定价26.39-36.39万",
            "Model X": "拥有独特的翅子门设计和更加大胆的外观风格。定价89.89-105.89万",
        }
        # 基于产品名称 => 产品描述
        return product_info.get(product_name, "没有找到这个产品")

    # 工具2：公司介绍
    def find_company_info(self, query: str) -> str:
        """
        返回公司介绍信息和车型。
        """
        context = """
        特斯拉最知名的产品是电动汽车，其中包括Model S、Model 3、Model X和Model Y等多款车型。
        特斯拉以其技术创新、高性能和领先的自动驾驶技术而闻名。公司不断推动自动驾驶技术的研发，并在车辆中引入了各种驾驶辅助功能，如自动紧急制动、自适应巡航控制和车道保持辅助等。
        """
        # prompt模板 = 上下文context + 用户的query
        prompt = self.CONTEXT_QA_PROMPT.format(query=query, context=context)
        # 使用LLM进行推理
        return self.llm.invoke(prompt)
