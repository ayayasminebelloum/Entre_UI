import streamlit as st
from PIL import Image
import qrcode
from datetime import datetime
from io import BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder

# Function to change font color and background color
st.markdown(
    """
    <style>
    .font {
        font-family: 'sans-serif';
        color: #778A35;
    }
    .stApp {
        background-color: #D1E2C4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to generate QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert PIL Image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    return img_bytes

# Function to send an email (mock function for now)
def send_email(email):
    # In a real-world scenario, you would integrate an email service here
    st.write(f"Sending email to {email}...")

# Define navigation options
menu = ["Home", "Past Events", "Subscriptions"]
choice = st.sidebar.selectbox("Menu", menu)

# Define the Home page
if choice == "Home":
    st.title("Welcome to Cooking Classes for University Students", anchor="home")
    st.image("https://github.com/ayayasminebelloum/Entre_UI/raw/main/logo.png")
    st.write("""
    **Your Gateway to Affordable and Healthy Meal Preparation Skills!**
    
    We offer a service-based solution with the help of a software platform which provides online cooking classes as well as in-person classes designed for university students. Choose from various options based on your availability and budget.
    """, unsafe_allow_html=True)

# Define the Past Events page
elif choice == "Past Events":
    st.title("Past Events")
    st.write("Here are some videos and photos from our past in-person classes.", unsafe_allow_html=True)
    
    # Placeholder content - replace with actual videos/photos
    st.title("This was one event we had hosted at one of the team member's house")
    st.image("https://github.com/ayayasminebelloum/Entre_UI/raw/main/Image1.jpeg", width=300)
    st.image("https://github.com/ayayasminebelloum/Entre_UI/raw/main/Image2.jpeg", width=300)
    st.image("https://github.com/ayayasminebelloum/Entre_UI/raw/main/Image3.jpeg", width=300)
    st.title("This was an uploaded video of a pilot run, we had done")
    st.video("WhatsApp Video 2024-05-22 at 19.39.34.mp4", format="video/mp4", start_time=0)

# Define the Subscriptions page
elif choice == "Subscriptions":
    st.title("Subscriptions")
    st.write("Choose the subscription plan that suits you best:", unsafe_allow_html=True)

    if "subscription" not in st.session_state:
        st.subheader("Basic Subscription")
        st.write("3 meals per week for 10 euros")
        if st.button("Choose Basic"):
            st.session_state.subscription = "Basic"
            st.experimental_rerun()

        st.subheader("Premium Subscription")
        st.write("5 meals per week for 15 euros")
        if st.button("Choose Premium"):
            st.session_state.subscription = "Premium"
            st.experimental_rerun()

        st.subheader("In-Person Classes")
        st.write("In-person classes for 50 euros")
        if st.button("Choose In-Person"):
            st.session_state.subscription = "In-Person"
            st.experimental_rerun()

# Handle the Basic and Premium subscription date and time selection
if "subscription" in st.session_state and st.session_state.subscription in ["Basic", "Premium"]:
    st.title(f"{st.session_state.subscription} Subscription")
    st.write("Please choose a date and time for your classes:", unsafe_allow_html=True)

    # Datepicker for date selection
    selected_date = st.date_input("Select a date", datetime.now())

    if selected_date:
        st.write(f"Selected Date: {selected_date}")
        time_options = ["10:00 AM", "2:00 PM", "6:00 PM"]
        selected_time = st.selectbox("Choose a time", time_options)

        if st.button("Confirm"):
            st.session_state.confirmed = True
            st.session_state.date = selected_date
            st.session_state.time = selected_time
            st.experimental_rerun()

if "confirmed" in st.session_state and st.session_state.confirmed:
    st.title("Confirmation")
    st.write(f"Thank you for subscribing to the {st.session_state.subscription} plan.")
    st.write(f"Your class is scheduled for {st.session_state.date} at {st.session_state.time}.", unsafe_allow_html=True)

    # Generate and display QR code
    qr_data = f"Subscription: {st.session_state.subscription}\nDate: {st.session_state.date}\nTime: {st.session_state.time}"
    qr_img_bytes = generate_qr_code(qr_data)
    st.image(qr_img_bytes)

    if st.button("Back to Subscriptions"):
        st.session_state.pop("confirmed")
        st.session_state.pop("subscription")
        st.experimental_rerun()

# Handle the in-person subscription email collection
if "subscription" in st.session_state and st.session_state.subscription == "In-Person":
    st.title("In-Person Subscription")
    st.write("Please enter your email to get notified about future events.", unsafe_allow_html=True)
    
    email = st.text_input("Enter your email address:")
    if st.button("Submit Email"):
        if email:
            send_email(email)
            st.success(f"Thank you for subscribing, {email}!")
            if st.button("Back to Subscriptions"):
                st.session_state.pop("subscription")
                st.experimental_rerun()
