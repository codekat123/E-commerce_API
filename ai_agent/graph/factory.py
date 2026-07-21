from langchain_core.messages import BaseMessage

from ai_agent.graph.state import GraphState


class GraphStateFactory:
    def create(
        self,
        *,
        user,
        messages: list[BaseMessage],
    ) -> GraphState:
        return GraphState(
            user=user,
            messages=messages,
        )
