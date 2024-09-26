import streamlit as st

# Set the page title and favicon
st.set_page_config(page_title="IEC 61499 AI Services Platform", page_icon="🤖")

# Define a function to display the home page
def home_page():
    st.title("Welcome to IEC 61499 AI Services Platform")
    st.subheader("End-to-End AI Services for Your IEC 61499 Application Needs")
    st.write(
        """
        We offer a wide range of AI services tailored to help you innovate, optimize, and grow.
        Select a service below to learn more:
        """
    )

    # Display buttons for each AI service
    if st.button("AI-Powered Solution Q&A Assistant Service"):
        pass
    if st.button("Chat With Your IEC 61499 Application Generated Data"):
        pass
    if st.button("Dynamic Data Visualizer For Your IEC 61499 Application"):
        pass
    if st.button("AI Assistant for your IEC 61499 based Manufacturing MarketPlace"):
        pass
    if st.button("IEC 61499 Function Block Generator"):
        pass


# Main function to handle routing
def main():
    home_page()  # Default to home page

# Run the app
if __name__ == "__main__":
    main()
