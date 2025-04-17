"# Streamlit-Arabic-Books-Tracker" 
"# Streamlit-Arabic-Books-Tracker" 

# This Arabic Book Tracker application provides a complete CRUD (Create, Read, Update, Delete) solution for managing your book collection. Here's what it offers:
# Key Features:

Right-to-Left Interface: Fully supports Arabic language with RTL text direction
Modern UI: Clean design with card layout and color-coded statuses
Complete CRUD Operations:

Add new books with detailed information
View and filter your collection
Edit existing book details
Delete books with confirmation



# Main Components:

Dashboard: Shows statistics about your book collection
Book Entry Form: Captures comprehensive book details
Book Display: Lists books with filtering options
Book Cards: Visually appealing presentation of each book

# How to Use:

Choose an operation from the sidebar
For adding books: Fill in the required fields and click "إضافة الكتاب"
For viewing: Use the filters to find specific books
For editing: Select a book from the dropdown and modify its details
For deleting: Select a book, review its information, and confirm deletion

The app saves all data to a CSV file and provides feedback messages after each operation. The design is user-friendly with a consistent color scheme and intuitive navigation.


# Technical Details:

The app uses PIL (Python Imaging Library) to process uploaded images
Images are stored as files rather than in the database for better performance
Cover image references are stored in a new "صورة الغلاف" column in the CSV file
The application handles all image operations (save, update, delete) automatically

This implementation provides a complete solution for managing book covers while maintaining the RTL support and user-friendly interface of the original application.



pip install -r requirements.txt

# To run
streamlit run main2.py
