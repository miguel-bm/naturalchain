import streamlit as st
from streamlit.components.v1 import html
from streamlit_chat import message
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header

from naturalchain.cli.main import StructuredChatAgent, get_agent

st.set_page_config(page_title="NaturalChain", page_icon="assets/logo.png")

if "agent" not in st.session_state:
    st.session_state["agent"] = get_agent(
        agent_type=StructuredChatAgent.full,
        verbose=True,
        model_name="gpt-3.5-turbo",
        temperature=0.0,
    )

# Sidebar contents
with st.sidebar:
    st.image("assets/logo.png", use_column_width=True)
    st.markdown(
        """
    ## About

    **NaturalChain** provides a <u>bridge</u> between them, allowing humans to interact with the blockchain using their natural language

    Interact with the **EVM ecosystem** using **natural language**

    - Write & Deploy Smart Contracts to any EVM chain
    - Query subgraphs from The Graph
    - Leverage the full JSON-RPC API

    And much more!

    [Github Page](https://github.com/miguel-bm/naturalchain)
    
    """,
        unsafe_allow_html=True,
    )
    add_vertical_space(5)

# Generate empty lists for generated and past.
## generated stores AI generated responses
if "generated" not in st.session_state:
    st.session_state["generated"] = ["Hi! I'm NaturalChain, how may I help you?"]
## past stores User's questions
if "past" not in st.session_state:
    st.session_state["past"] = ["Hi!"]

# Layout of input/response containers
older_messages_container = st.container()
colored_header(label="", description="", color_name="blue-30")
response_container = st.container()
input_container = st.container()


# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt: str):
    agent = st.session_state["agent"]
    response = agent.run(prompt)
    return response


user_input = st.session_state.get("input")

with older_messages_container:
    load_older_messages = st.button("Load older messages")

    if load_older_messages:
        st.session_state["max_messages"] += 5
    else:
        st.session_state["max_messages"] = 5


## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state["generated"]:
        num_messages = min(
            st.session_state["max_messages"], len(st.session_state["generated"])
        )
        for i in range(num_messages, 0, -1):
            message(st.session_state["past"][-i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][-i], key=str(i))

st.session_state["input"] = ""
## Applying the user input box
with input_container:
    user_input = get_text()
    if user_input:
        st.session_state["max_messages"] = 5

st.markdown(
    """
  <style>
    .css-13sdm1b.e16nr0p33 {
      margin-top: -75px;
    }
  </style>
""",
    unsafe_allow_html=True,
)
