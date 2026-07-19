from langchain_core.messages import BaseMessage

from ai_agent.graph.state import GraphState


class GraphStateFactory:
    def create(
        self,
        messages: list[BaseMessage],
    ) -> GraphState:
        return GraphState(
            messages=messages,
        )
