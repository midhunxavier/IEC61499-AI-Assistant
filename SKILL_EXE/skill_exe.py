from opcua import Client, ua
import uuid
import time
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage

current_state = {
    1: "IDLE",
    2: "STARTING",
    3: "EXECUTE",
    4: "COMPLETING",
    5: "COMPLETE",
    6: "RESETTING",
    7: "HOLDING",
    8: "HELD",
    9: "UNHOLDING",
    10: "SUSPENDING",
    11: "SUSPENDED",
    12: "UNSUSPENDING",
    13: "STOPPING",
    14: "STOPPED",
    15: "ABORTING",
    16: "ABORTED",
    17: "CLEARING"
    }
def opcua_write(url, namespace_idx, guid_str, value_to_write):
    client = Client(url)
    try:
        client.connect()
        node_guid = uuid.UUID(guid_str)  
        node = client.get_node(ua.NodeId(node_guid, namespace_idx))  
        dv = ua.DataValue()
        dv.Value = ua.Variant(value_to_write, ua.VariantType.Int16)  
        node.set_value(dv)

    except Exception as e:
        print(f"Error while writing: {e}")
    finally:
        client.disconnect()

def opcua_read(url, namespace_idx, guid_str):
    client = Client(url)
    try:
        client.connect()
        node_guid = uuid.UUID(guid_str) 
        node = client.get_node(ua.NodeId(node_guid, namespace_idx))  
        value = node.get_value()
        return value
        
    except Exception as e:
        print(f"Error while reading: {e}")
    finally:
        client.disconnect()

def opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str) -> str:
    opcua_write(url, namespace_idx, skill_cmd_guid_str, 1)
    print("-----STARTING------------")
    count=0
    while count<6:
        value = opcua_read(url, namespace_idx, current_state_guid_str)
        if value == 5:
            break
        print("-----Current State is "+ current_state[value])
        time.sleep(.25)   
        count+=1
        
    opcua_write(url, namespace_idx, skill_cmd_guid_str, 2)
    count=0
    while count<2:
        value = opcua_read(url, namespace_idx, current_state_guid_str)
        if value == 1:
            break
        print("-----Current State is "+ current_state[value])
        time.sleep(.25)   
        count+=1
    response = opcua_read(url, namespace_idx, response_guid_str)
    return response

def Move_To_Left_skill() -> str:
    """Move to left skill moves the rotating arm to its left side.
       This Skill associated with ROATATING ARM component.
    """
    url = "opc.tcp://B6426.ltuad.ltu.se:4840"  
    namespace_idx = 2  
    skill_cmd_guid_str = "38aa1c3f-ed71-7cdf-4efe-aa156299990d" 
    current_state_guid_str = "287a3f93-b164-eabe-1b9e-0666d73a7cac" 
    response_guid_str = "72320020-3684-b9fd-b4a4-54c91da20a18" 
    output = opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str)
    return output

def Move_To_Right_skill() -> str:
    """Move to right skill moves the rotating arm to its right side.
       This Skill associated with ROATATING ARM component.
    """
    url = "opc.tcp://B6426.ltuad.ltu.se:4840"  
    namespace_idx = 2  
    skill_cmd_guid_str = "e4202bc6-1190-33b6-5a90-36d4b3e33d89" 
    current_state_guid_str = "4adca34b-12a1-2b20-14a0-dc256d1c2154" 
    response_guid_str = "7872facf-6c74-c644-329d-cc1db038406e" 
    output = opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str)
    return output


def Pick_Workpiece_Skill() -> str:
    """Pick_workpiece_skill picks the workpiece. 
       This Skill associated with ROATATING ARM component.
    """
    url = "opc.tcp://B6426.ltuad.ltu.se:4840"  
    namespace_idx = 2  
    skill_cmd_guid_str = "bc268ffa-5afd-e2e0-bf0e-ef919d98ecf6" 
    current_state_guid_str = "6cb0ff45-8930-7114-4e5c-40ac396ef8f6" 
    response_guid_str = "4655fb1c-4903-7385-59c4-e68296162dc9" 
    output = opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str)
    return output

def Place_Workpiece_Skill() -> str:
    """Place_workpiece_skill drops the workpiece.
       This Skill associated with ROATATING ARM component.
    """
    url = "opc.tcp://B6426.ltuad.ltu.se:4840"  
    namespace_idx = 2  
    skill_cmd_guid_str = "70d5ee2c-aa3b-9ddd-8d40-568aefa88ba2" 
    current_state_guid_str = "62ac7163-8281-029f-56f1-a784f54382c7" 
    response_guid_str = "cf564f98-da09-2eab-a646-2980356c62ed" 
    output = opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str)
    return output

def Push_Workpiece_Skill() -> str:
    """Push_Workpiece_Skill moves the Workpiece from MAGAZINE.
       This Skill associated with MAGAZINE component.
    """
    url = "opc.tcp://B6426.ltuad.ltu.se:4840"  
    namespace_idx = 2  
    skill_cmd_guid_str = "ca6be633-6648-8c0e-07da-4e547a8d5023" 
    current_state_guid_str = "478d672d-69e7-c210-1005-89b9e3ada914" 
    response_guid_str = "bf89858a-1ab5-7c56-b8fe-78e64d0cc585" 
    output = opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str)
    return output


def Load_Magazine_Skill() -> str:
    """Load_Magazine_Skill loads the empty MAGAZINE with 6 workpieces.
       This Skill associated with MAGAZINE component.
    """
    url = "opc.tcp://B6426.ltuad.ltu.se:4840"  
    namespace_idx = 2  
    skill_cmd_guid_str = "eeb1ddd8-fdfb-221f-d06f-75041e79efce" 
    current_state_guid_str = "a7c86736-71ee-6b0a-fc18-4f3603eac3c1" 
    response_guid_str = "5454b450-97d0-25f7-ad5e-58d27231f4e1" 
    output = opcua_skill_executer(url, namespace_idx, skill_cmd_guid_str,current_state_guid_str,response_guid_str)
    return output

tools = [Move_To_Left_skill, Move_To_Right_skill, Pick_Workpiece_Skill, Place_Workpiece_Skill,Push_Workpiece_Skill,Load_Magazine_Skill]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)


sys_msg = SystemMessage(content=
"""
You are an assistant capable of controlling both a ROTATING ARM component and a STACKED MAGAZINE component in a factory, using a set of predefined skills.
The STACKED MAGAZINE is positioned to the left side of the ROTATING ARM component.

Task : Define the task based on the give requirement.

Plan of Action:
1. Plan and Description:
    - Plan and describe a sequence of skills required to complete this task, breaking down each step (e.g., push, load, pick, rotate, place, etc.).
    - Ensure the sequence respects the dependencies (e.g., the MAGAZINE pushes, the ARM picks, etc.).

2. Skill Execution:

    - Execute each skill one by one, while providing feedback after each step.
    - Adjust or refine the sequence based on output or challenges encountered during execution.

Additional Notes:

1. Initially, 6 workpieces are loaded inside the MAGAZINE.
2. The ROTATING ARM can only pick a workpiece once workpiece has been pushed from the MAGAZINE.
3. The MAGAZINE can only push a workpiece if the previous workpiece is placed on the right side of the ROTATING ARM.
""")

class MessagesState(MessagesState):
    myname: str
    
# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])], "myNmae": "midhun"}

def set_react_skill_graph():
    builder = StateGraph(MessagesState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile()

    return react_graph
