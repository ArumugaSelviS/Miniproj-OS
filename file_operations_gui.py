import streamlit as st
import os

# Simple user credentials (in real applications, use proper database and hashing)
USERS = {
    "Aru": "Aru04",
    "Afsan": "Afsan22"
}

# File operations
def create_file(filename):
    if os.path.exists(filename):
        return False
    with open(filename, 'w') as f:
        f.write("")
    return True

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + "\n")

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False

def list_files():
    return [f for f in os.listdir() if os.path.isfile(f)]

# Callback to update session state when input changes
def update_session_state(key):
    st.session_state[key] = st.session_state[f"input_{key}"]

# Custom CSS for styling
custom_css = """
<style>
/* General app styling */
body {
    background-color: #F5F7FA;
}

/* Main title */
h1 {
    color: #4B0082;
    text-align: center;
    font-family: 'Arial', sans-serif;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* Section headers */
h2 {
    color: #00CED1;
    font-family: 'Arial', sans-serif;
    border-bottom: 2px solid #FFD700;
    padding-bottom: 5px;
    margin-bottom: 20px;
}

/* Containers for sections */
.stApp > div > div > div > div {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Input fields */
.stTextInput > div > div > input {
    border: 2px solid #00CED1;
    border-radius: 5px;
    padding: 8px;
    transition: border-color 0.3s;
}
.stTextInput > div > div > input:focus {
    border-color: #4B0082;
    box-shadow: 0 0 5px rgba(75, 0, 130, 0.3);
}

/* Text area */
.stTextArea > div > div > textarea {
    border: 2px solid #00CED1;
    border-radius: 5px;
    padding: 8px;
}
.stTextArea > div > div > textarea:focus {
    border-color: #4B0082;
}

/* Buttons */
.stButton > button {
    background-color: #4B0082;
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-weight: bold;
    transition: background-color 0.3s;
}
.stButton > button:hover {
    background-color: #FFD700;
    color: #333333;
}

/* Success and error messages */
.stSuccess {
    background-color: #E6F3E6;
    color: #2E7D32;
    border-radius: 5px;
    padding: 10px;
}
.stError {
    background-color: #FFEBEE;
    color: #C62828;
    border-radius: 5px;
    padding: 10px;
}

/* File list */
.stMarkdown > div > p {
    color: #333333;
    font-family: 'Arial', sans-serif;
}

/* Radio buttons */
.stRadio > label {
    color: #333333;
    font-family: 'Arial', sans-serif;
}
.stRadio > div > label > div {
    background-color: #00CED1;
    border-radius: 5px;
}
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Login page
def login_page():
    st.title("Login to File Management System")
    st.markdown("Only Afsana and Arumuga Selvi can access this file")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔒 Secure Login", unsafe_allow_html=True)
        username = st.text_input("Username", value=st.session_state.get('username', ''))
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

# Main app
def main_app():
    st.title("📁 Personal File Management System")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.content_write = ""
        st.session_state.content_modify = ""
        st.rerun()

    # Create File
    with st.container():
        st.header("📝 Create File")
        filename_create = st.text_input(
            "Enter the filename to create:",
            value=st.session_state.get('filename_create', ''),
            key="input_filename_create",
            on_change=update_session_state,
            args=('filename_create',)
        )
        if st.button("Create File"):
            if filename_create:
                if create_file(filename_create):
                    st.success(f"File '{filename_create}' created successfully!")
                else:
                    st.error(f"File '{filename_create}' already exists! Please choose a different name.")
            else:
                st.error("Please enter a filename.")

    # Write to File
    with st.container():
        st.header("✍️ Write to File")
        filename_write = st.text_input(
            "Enter the filename to write to:",
            value=st.session_state.get('filename_write', ''),
            key="input_filename_write",
            on_change=update_session_state,
            args=('filename_write',)
        )
        content_write = st.text_area(
            "Enter content to write to the file:",
            value=st.session_state.get('content_write', ''),
            key="input_content_write",
            on_change=update_session_state,
            args=('content_write',)
        )
        
        if st.button("Write to File"):
            if filename_write:
                if content_write:
                    write_to_file(filename_write, content_write)
                    st.success(f"Content written to '{filename_write}' successfully!")
                    st.session_state.content_write = ''
                else:
                    st.error("Please enter content to write.")
            else:
                st.error("Please enter a filename.")

    # Read File
    with st.container():
        st.header("📖 Read File")
        filename_read = st.text_input(
            "Enter the filename to read:",
            value=st.session_state.get('filename_read', ''),
            key="input_filename_read",
            on_change=update_session_state,
            args=('filename_read',)
        )
        if st.button("Read File"):
            if os.path.exists(filename_read):
                file_content = read_file(filename_read)
                st.text_area("File Content:", file_content, height=300)
            else:
                st.error(f"File '{filename_read}' does not exist.")

    # Delete File
    with st.container():
        st.header("🗑️ Delete File")
        filename_delete = st.text_input(
            "Enter the filename to delete:",
            value=st.session_state.get('filename_delete', ''),
            key="input_filename_delete",
            on_change=update_session_state,
            args=('filename_delete',)
        )
        if st.button("Delete File"):
            if filename_delete:
                if delete_file(filename_delete):
                    st.success(f"File '{filename_delete}' deleted successfully!")
                else:
                    st.error(f"File '{filename_delete}' does not exist.")
            else:
                st.error("Please enter a filename.")

    # Modify File
    with st.container():
        st.header("✏️ Modify File")
        filename_modify = st.text_input(
            "Enter the filename to modify:",
            value=st.session_state.get('filename_modify', ''),
            key="input_filename_modify",
            on_change=update_session_state,
            args=('filename_modify',)
        )
        content_modify = st.text_area(
            "Enter content to add or modify:",
            value=st.session_state.get('content_modify', ''),
            key="input_content_modify",
            on_change=update_session_state,
            args=('content_modify',)
        )
        modify_option = st.radio("Choose an option:", ("Add Content", "Modify Content"))
        if st.button("Modify File"):
            if filename_modify:
                if modify_option == "Add Content":
                    write_to_file(filename_modify, content_modify)
                    st.success(f"Content added to '{filename_modify}' successfully!")
                elif modify_option == "Modify Content":
                    if os.path.exists(filename_modify):
                        with open(filename_modify, 'w') as f:
                            f.write(content_modify)
                        st.success(f"File '{filename_modify}' modified successfully!")
                    else:
                        st.error(f"File '{filename_modify}' does not exist. Please create it first.")
                st.session_state.content_modify = ''
            else:
                st.error("Please enter a filename.")

    # Show Files
    with st.container():
        st.header("📋 Show Files")
        files = list_files()
        if files:
            st.write("Files in the current directory:")
            for file in files:
                st.markdown(f"📄 **{file}**")
        else:
            st.write("No files found.")

    # Reset All Inputs Button
    with st.container():
        st.header("🔄 Reset Inputs")
        if st.button("Reset All Inputs"):
            st.session_state.filename_create = ''
            st.session_state.filename_write = ''
            st.session_state.filename_read = ''
            st.session_state.filename_delete = ''
            st.session_state.filename_modify = ''
            st.session_state.content_write = ''
            st.session_state.content_modify = ''
            st.success("All input fields have been reset!")
            st.rerun()

    # Debug Session State (Optional, for troubleshooting)
    with st.expander("🔍 Debug: View Session State"):
        st.write("Current Session State:", st.session_state)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.filename_create = ""
    st.session_state.filename_write = ""
    st.session_state.filename_read = ""
    st.session_state.filename_delete = ""
    st.session_state.filename_modify = ""
    st.session_state.content_write = ""
    st.session_state.content_modify = ""

# Render appropriate page based on login status
if not st.session_state.logged_in:
    login_page()
else:
    main_app()