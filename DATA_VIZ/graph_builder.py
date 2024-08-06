from langgraph.graph import StateGraph
from DATA_VIZ.state_handlers import (
    search_proper_names, 
    search_variable_info, 
    search_table_info, 
    search_query_info,
    draw_agent,
    should_continue_search_proper_names,
    should_continue_search_variable_info,
    should_continue_search_table_info,
    should_continue_search_query_info,
    should_continue_draw_chart,
    SqlInfoState
)
from DATA_VIZ.tools import (
    search_proper_names_tool, 
    get_variable_details_tool, 
    get_relevant_table_schema_tool, 
    db_query_tool,
    create_tool_node_with_fallback,
    python_repl_tool
)


from langgraph.checkpoint.sqlite import SqliteSaver

def create_sql_graph():
    memory = SqliteSaver.from_conn_string(":memory:")

    graph_builder = StateGraph(SqlInfoState)

    graph_builder.add_node("search_proper_names", search_proper_names)

    graph_builder.add_node("search_variable_info", search_variable_info)

    graph_builder.add_node("search_table_info", search_table_info)

    graph_builder.add_node("search_query_info", search_query_info)
            
    graph_builder.add_node("draw_chart", draw_agent)


    graph_builder.add_node("search_proper_names_tool", create_tool_node_with_fallback([search_proper_names_tool]))

    graph_builder.add_node("get_variable_details_tool", create_tool_node_with_fallback([get_variable_details_tool]))

    graph_builder.add_node("get_relevant_table_schema_tool", create_tool_node_with_fallback([get_relevant_table_schema_tool]))

    graph_builder.add_node("db_query_tool", create_tool_node_with_fallback([db_query_tool]))



    graph_builder.add_conditional_edges(
        "search_proper_names",
        should_continue_search_proper_names,
    )
    graph_builder.add_conditional_edges(
        "search_variable_info",
        should_continue_search_variable_info,
    )
    graph_builder.add_conditional_edges(
        "search_table_info",
        should_continue_search_table_info,
    )
    graph_builder.add_conditional_edges(
        "search_query_info",
        should_continue_search_query_info,
    )


    graph_builder.add_edge("search_proper_names_tool", "search_proper_names")
    graph_builder.add_edge("get_variable_details_tool", "search_variable_info")
    graph_builder.add_edge("get_relevant_table_schema_tool", "search_table_info")
    graph_builder.add_edge("db_query_tool", "search_query_info")
    graph_builder.add_edge("draw_chart", "__end__")
    graph_builder.set_entry_point("search_proper_names")
    graph = graph_builder.compile(checkpointer=memory)
    return graph