import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from PIL import Image
import io

# Set page configuration for RTL support
st.set_page_config(
    page_title="تطبيق متابعة الكتب",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for RTL support
st.markdown("""
<style>
    body {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
        color: #2c3e50;
    }
    .stButton button {
        float: right;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stTextInput, .stSelectbox, .stDateInput, .stTextarea {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        border: 1px solid #ced4da;
        border-radius: 5px;
        padding: 10px;
        transition: box-shadow 0.3s ease;
    }
    .stTextInput:focus, .stSelectbox:focus, .stDateInput:focus, .stTextarea:focus {
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    }
    h1, h2, h3, p {
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }
    .book-card {
        background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        display: flex;
        flex-direction: row-reverse;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
    }
    .book-cover {
        width: 120px;
        height: 180px;
        object-fit: cover;
        border-radius: 10px;
        margin-left: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    .book-cover:hover {
        transform: scale(1.05);
    }
    .book-details {
        flex: 1;
        color: #333;
    }
    .book-details h3 {
        font-size: 1.5rem;
        margin-bottom: 10px;
        color: #2c3e50;
    }
    .book-details p {
        margin: 5px 0;
        font-size: 1rem;
        color: #34495e;
    }
    .book-details .status {
        font-weight: bold;
        color: #27ae60;
    }
    .book-details .rating {
        color: #f39c12;
    }
    .no-cover {
        width: 120px;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #ecf0f1;
        border-radius: 10px;
        margin-left: 20px;
        color: #7f8c8d;
        text-align: center;
        font-size: 0.9rem;
    }
    .banner {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .banner h1 {
        text-align: center;
        margin-bottom: 10px;
        font-size: 2.5rem;
    }
    .banner p {
        text-align: center;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .book-emoji {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    .stats-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stats-container p {
        font-size: 1.1rem;
        color: #2c3e50;
    }
    .action-buttons button {
        margin-left: 5px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-size: 1rem;
        transition: background-color 0.3s ease;
    }
    .action-buttons button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# Create necessary directories
BOOKS_FOLDER = "books"
if not os.path.exists(BOOKS_FOLDER):
    os.makedirs(BOOKS_FOLDER)

# Default data file path
DATA_FILE = "books_data.csv"

# Function to load existing data or create new dataframe
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame({
            "عنوان": [],
            "مؤلف": [],
            "تصنيف": [],
            "تاريخ النشر": [],
            "عدد الصفحات": [],
            "الحالة": [],
            "التقييم": [],
            "ملاحظات": [],
            "تاريخ الإضافة": [],
            "صورة الغلاف": []  # New column for cover image filename
        })

# Function to save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Function to save uploaded cover image
def save_cover_image(uploaded_file, book_title):
    if uploaded_file is not None:
        # Create a safe filename based on book title
        filename = "".join(c for c in book_title if c.isalnum() or c in [' ', '_']).rstrip()
        filename = filename.replace(' ', '_')
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        
        # Save the image
        image_path = os.path.join(BOOKS_FOLDER, filename)
        
        # Process and save the image
        img = Image.open(uploaded_file)
        img.save(image_path)
        
        return filename
    return None

# Function to get image data for display
def get_image_data(image_filename):
    if image_filename and os.path.exists(os.path.join(BOOKS_FOLDER, image_filename)):
        with open(os.path.join(BOOKS_FOLDER, image_filename), "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Main app function
def main():
    # Load data
    df = load_data()
    
    # Display banner
    st.markdown(
        """
        <div class="banner">
            <span class="book-emoji">📚</span>
            <h1>تطبيق متابعة الكتب</h1>
            <p>إدارة مجموعة الكتب الخاصة بك بكل سهولة</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.image("D:\Streamlit Arabic Books Tracker\Books\logo.png", use_column_width=True)
        st.markdown("<h2 style='text-align: right;'>لوحة التحكم</h2>", unsafe_allow_html=True)
        
        # Display statistics
        
        st.markdown("<div class='stats-container'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: right;'>إحصائيات</h3>", unsafe_allow_html=True)
        
        if not df.empty:
            total_books = len(df)
            read_books = len(df[df["الحالة"] == "تمت القراءة"])
            reading_books = len(df[df["الحالة"] == "قيد القراءة"])
            unread_books = len(df[df["الحالة"] == "لم تتم القراءة بعد"])
            
            st.markdown(f"<p>إجمالي الكتب: {total_books}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>كتب تمت قراءتها: {read_books}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>كتب قيد القراءة: {reading_books}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>كتب لم تتم قراءتها: {unread_books}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>لا توجد بيانات بعد</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Operation selection
        operation = st.selectbox(
            "اختر العملية",
            ["عرض الكتب", "إضافة كتاب", "تعديل كتاب", "حذف كتاب"]
        )
    
    # Main content area based on selected operation
    if operation == "إضافة كتاب":
        add_book(df)
    elif operation == "عرض الكتب":
        view_books(df)
    elif operation == "تعديل كتاب":
        edit_book(df)
    elif operation == "حذف كتاب":
        delete_book(df)
        
# Add book function
def add_book(df):
    st.markdown("<h2>إضافة كتاب جديد</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("عنوان الكتاب")
        author = st.text_input("اسم المؤلف")
        category = st.selectbox("التصنيف", [
            "أدب", "تاريخ", "فلسفة", "علوم", "دين", 
            "سياسة", "اقتصاد", "تنمية بشرية", "سيرة ذاتية", "أخرى"
        ])
        pub_date = st.date_input("تاريخ النشر")
        # New field for cover image
        cover_image = st.file_uploader("صورة الغلاف", type=["jpg", "jpeg", "png"])
    
    with col2:
        pages = st.number_input("عدد الصفحات", min_value=1, value=100)
        status = st.selectbox("حالة القراءة", [
            "تمت القراءة", "قيد القراءة", "لم تتم القراءة بعد"
        ])
        rating = st.slider("التقييم", 1, 5, 3)
        notes = st.text_area("ملاحظات")
    
    # Display preview of uploaded image
    if cover_image:
        st.image(cover_image, width=150, caption="معاينة صورة الغلاف")
    
    if st.button("إضافة الكتاب"):
        if title and author:
            # Save cover image if uploaded
            cover_filename = save_cover_image(cover_image, title) if cover_image else None
            
            # Create new book record
            new_book = {
                "عنوان": title,
                "مؤلف": author,
                "تصنيف": category,
                "تاريخ النشر": pub_date.strftime("%Y-%m-%d"),
                "عدد الصفحات": pages,
                "الحالة": status,
                "التقييم": rating,
                "ملاحظات": notes,
                "تاريخ الإضافة": datetime.now().strftime("%Y-%m-%d"),
                "صورة الغلاف": cover_filename
            }
            
            # Add to dataframe
            df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
            save_data(df)
            
            st.markdown(
                """
                <div class="success-message">
                    تمت إضافة الكتاب بنجاح!
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="warning-message">
                    يرجى إدخال عنوان الكتاب واسم المؤلف على الأقل.
                </div>
                """, 
                unsafe_allow_html=True
            )

# View books function
def view_books(df):
    st.markdown("<h2>عرض الكتب</h2>", unsafe_allow_html=True)
    
    if df.empty:
        st.markdown(
            """
            <div class="warning-message">
                لا توجد كتب في قاعدة البيانات. يرجى إضافة كتب أولاً.
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_status = st.multiselect(
            "تصفية حسب الحالة",
            ["تمت القراءة", "قيد القراءة", "لم تتم القراءة بعد"],
            default=[]
        )
    
    with col2:
        categories = df["تصنيف"].unique().tolist()
        filter_category = st.multiselect(
            "تصفية حسب التصنيف",
            categories,
            default=[]
        )
    
    with col3:
        search_term = st.text_input("البحث في العناوين أو المؤلفين")
    
    # Apply filters
    filtered_df = df.copy()
    
    if filter_status:
        filtered_df = filtered_df[filtered_df["الحالة"].isin(filter_status)]
    
    if filter_category:
        filtered_df = filtered_df[filtered_df["تصنيف"].isin(filter_category)]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df["عنوان"].str.contains(search_term, case=False) | 
            filtered_df["مؤلف"].str.contains(search_term, case=False)
        ]
    
    # Display books as cards
    if filtered_df.empty:
        st.markdown(
            """
            <div class="warning-message">
                لا توجد نتائج تطابق معايير البحث.
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"<p>تم العثور على {len(filtered_df)} كتاب</p>", unsafe_allow_html=True)
        
        for i, (_, book) in enumerate(filtered_df.iterrows()):
            # Determine rating stars
            stars = "⭐" * int(book["التقييم"])
            
            # Determine status color
            status_color = {
                "تمت القراءة": "#28a745",
                "قيد القراءة": "#ffc107",
                "لم تتم القراءة بعد": "#6c757d"
            }
            
            # Cover image handling
            cover_img_html = ""
            if pd.notna(book.get("صورة الغلاف")) and book["صورة الغلاف"]:
                img_data = get_image_data(book["صورة الغلاف"])
                if img_data:
                    cover_img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="book-cover" alt="غلاف الكتاب">'
                else:
                    cover_img_html = '<div class="no-cover">لا توجد صورة</div>'
            else:
                cover_img_html = '<div class="no-cover">لا توجد صورة</div>'
            
            # Display book card
            st.markdown(
                f"""
                <div class="book-card">
                    {cover_img_html}
                    <div class="book-details">
                        <h3>{book["عنوان"]}</h3>
                        <p>المؤلف: {book["مؤلف"]}</p>
                        <p>التصنيف: {book["تصنيف"]}</p>
                        <p>تاريخ النشر: {book["تاريخ النشر"]}</p>
                        <p>عدد الصفحات: {book["عدد الصفحات"]}</p>
                        <p>الحالة: <span style="color: {status_color.get(book["الحالة"], "#000")};">{book["الحالة"]}</span></p>
                        <p>التقييم: {stars}</p>
                        <p>ملاحظات: {book["ملاحظات"]}</p>
                        <p><small>تاريخ الإضافة: {book["تاريخ الإضافة"]}</small></p>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )

# Edit book function
def edit_book(df):
    st.markdown("<h2>تعديل كتاب</h2>", unsafe_allow_html=True)
    
    if df.empty:
        st.markdown(
            """
            <div class="warning-message">
                لا توجد كتب في قاعدة البيانات. يرجى إضافة كتب أولاً.
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
    
    # Select book to edit
    book_titles = df["عنوان"].tolist()
    selected_book = st.selectbox("اختر الكتاب الذي تريد تعديله", book_titles)
    
    if selected_book:
        # Get index of selected book
        book_idx = df[df["عنوان"] == selected_book].index[0]
        book = df.iloc[book_idx]
        
        st.markdown("<h3>تعديل بيانات الكتاب</h3>", unsafe_allow_html=True)
        
        # Display current cover if exists
        current_cover = None
        if pd.notna(book.get("صورة الغلاف")) and book["صورة الغلاف"]:
            img_path = os.path.join(BOOKS_FOLDER, book["صورة الغلاف"])
            if os.path.exists(img_path):
                st.image(img_path, width=150, caption="صورة الغلاف الحالية")
                current_cover = book["صورة الغلاف"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("عنوان الكتاب", value=book["عنوان"])
            author = st.text_input("اسم المؤلف", value=book["مؤلف"])
            category = st.selectbox("التصنيف", [
                "أدب", "تاريخ", "فلسفة", "علوم", "دين", 
                "سياسة", "اقتصاد", "تنمية بشرية", "سيرة ذاتية", "أخرى"
            ], index=["أدب", "تاريخ", "فلسفة", "علوم", "دين", 
                    "سياسة", "اقتصاد", "تنمية بشرية", "سيرة ذاتية", "أخرى"].index(book["تصنيف"]) if book["تصنيف"] in ["أدب", "تاريخ", "فلسفة", "علوم", "دين", 
                    "سياسة", "اقتصاد", "تنمية بشرية", "سيرة ذاتية", "أخرى"] else 0)
            try:
                pub_date = st.date_input("تاريخ النشر", value=pd.to_datetime(book["تاريخ النشر"]))
            except:
                pub_date = st.date_input("تاريخ النشر")
            # Option to upload new cover
            new_cover = st.file_uploader("تغيير صورة الغلاف", type=["jpg", "jpeg", "png"])
        
        with col2:
            pages = st.number_input("عدد الصفحات", min_value=1, value=int(book["عدد الصفحات"]))
            status = st.selectbox("حالة القراءة", [
                "تمت القراءة", "قيد القراءة", "لم تتم القراءة بعد"
            ], index=["تمت القراءة", "قيد القراءة", "لم تتم القراءة بعد"].index(book["الحالة"]))
            rating = st.slider("التقييم", 1, 5, int(book["التقييم"]))
            notes = st.text_area("ملاحظات", value=book["ملاحظات"])
        
        # Preview new cover
        if new_cover:
            st.image(new_cover, width=150, caption="معاينة صورة الغلاف الجديدة")
        
        if st.button("حفظ التعديلات"):
            if title and author:
                # Handle cover image update
                cover_filename = current_cover
                if new_cover:
                    # Remove old cover if exists
                    if current_cover and os.path.exists(os.path.join(BOOKS_FOLDER, current_cover)):
                        try:
                            os.remove(os.path.join(BOOKS_FOLDER, current_cover))
                        except:
                            pass
                    # Save new cover
                    cover_filename = save_cover_image(new_cover, title)
                
                # Update book data
                df.at[book_idx, "عنوان"] = title
                df.at[book_idx, "مؤلف"] = author
                df.at[book_idx, "تصنيف"] = category
                df.at[book_idx, "تاريخ النشر"] = pub_date.strftime("%Y-%m-%d")
                df.at[book_idx, "عدد الصفحات"] = pages
                df.at[book_idx, "الحالة"] = status
                df.at[book_idx, "التقييم"] = rating
                df.at[book_idx, "ملاحظات"] = notes
                df.at[book_idx, "صورة الغلاف"] = cover_filename
                
                save_data(df)
                
                st.markdown(
                    """
                    <div class="success-message">
                        تم تحديث بيانات الكتاب بنجاح!
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="warning-message">
                        يرجى إدخال عنوان الكتاب واسم المؤلف على الأقل.
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

# Delete book function
def delete_book(df):
    st.markdown("<h2>حذف كتاب</h2>", unsafe_allow_html=True)
    
    if df.empty:
        st.markdown(
            """
            <div class="warning-message">
                لا توجد كتب في قاعدة البيانات. يرجى إضافة كتب أولاً.
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
    
    # Select book to delete
    book_titles = df["عنوان"].tolist()
    selected_book = st.selectbox("اختر الكتاب الذي تريد حذفه", book_titles)
    
    if selected_book:
        # Get book details
        book = df[df["عنوان"] == selected_book].iloc[0]
        
        # Display book details with cover if exists
        cover_html = ""
        if pd.notna(book.get("صورة الغلاف")) and book["صورة الغلاف"]:
            img_data = get_image_data(book["صورة الغلاف"])
            if img_data:
                cover_html = f'<img src="data:image/jpeg;base64,{img_data}" class="book-cover" alt="غلاف الكتاب">'
        
        st.markdown(
            f"""
            <div class="book-card">
                {cover_html if cover_html else '<div class="no-cover">لا توجد صورة</div>'}
                <div class="book-details">
                    <h3>{book["عنوان"]}</h3>
                    <p>المؤلف: {book["مؤلف"]}</p>
                    <p>التصنيف: {book["تصنيف"]}</p>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Confirm deletion
        st.markdown(
            """
            <div class="warning-message">
                هل أنت متأكد من أنك تريد حذف هذا الكتاب؟ لا يمكن التراجع عن هذا الإجراء.
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        if st.button("نعم، احذف هذا الكتاب"):
            # Remove cover image if exists
            if pd.notna(book.get("صورة الغلاف")) and book["صورة الغلاف"]:
                img_path = os.path.join(BOOKS_FOLDER, book["صورة الغلاف"])
                if os.path.exists(img_path):
                    try:
                        os.remove(img_path)
                    except:
                        pass
            
            # Remove book from dataframe
            df = df[df["عنوان"] != selected_book]
            save_data(df)
            
            st.markdown(
                """
                <div class="success-message">
                    تم حذف الكتاب بنجاح!
                </div>
                """, 
                unsafe_allow_html=True
            )

# Run the app
if __name__ == "__main__":
    main()