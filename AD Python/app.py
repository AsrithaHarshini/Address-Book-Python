import streamlit as st
import pandas as pd
from storage import Storage

def main():
    st.set_page_config(page_title="Address Book Pro", page_icon="📇", layout="wide")

    # Custom CSS for premium look
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            border-radius: 20px;
            background-color: #4CAF50;
            color: white;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
        }
        .contact-card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📇 Address Book Pro")
    st.markdown("---")

    storage = Storage()

    # Sidebar for add and search
    with st.sidebar:
        st.header("Search & Actions")
        search_query = st.text_input("🔍 Search by Name or Context", placeholder="e.g. John or 'met at cafe'")
        
        st.markdown("---")
        st.header("➕ Add New Contact")
        with st.form("add_contact_form", clear_on_submit=True):
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone Number")
            new_email = st.text_input("Email Address")
            new_info = st.text_area("Information / Context")
            submit_button = st.form_submit_button("Save Contact")

            if submit_button:
                if new_name:
                    storage.add_contact(new_name, new_phone, new_email, new_info)
                    st.success(f"Contact '{new_name}' saved successfully!")
                else:
                    st.error("Name is required.")

    # Main area
    if search_query:
        results = storage.search_contacts(search_query)
        st.subheader(f"Search Results for '{search_query}'")
    else:
        results = storage.get_all_contacts()
        st.subheader("All Contacts")

    if not results.empty:
        # Display as a clean table
        st.dataframe(results, use_container_width=True, hide_index=True)
        
        # Grid View / Contact Cards
        st.markdown("### Contact Details")
        for idx, row in results.iterrows():
            with st.expander(f"👤 {row['Name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**📞 Phone:** {row['Phone']}")
                    st.write(f"**📧 Email:** {row['Email']}")
                with col2:
                    st.write(f"**📝 Information:**")
                    st.write(row['Information'])
                
                if st.button(f"Delete {row['Name']}", key=f"del_{idx}"):
                    storage.delete_contact(idx)
                    st.rerun()
    else:
        st.info("No contacts found. Add some starting in the sidebar!")

    # Export functionality
    st.markdown("---")
    if st.button("📥 Export to JSON"):
        json_data = results.to_json(orient="records", indent=4)
        st.download_button(
            label="Download JSON File",
            data=json_data,
            file_name="address_book_export.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
