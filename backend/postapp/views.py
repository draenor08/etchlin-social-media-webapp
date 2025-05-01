# postapp/views.py
import os
import mysql.connector
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages  # for showing error/success messages

def create_post(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        text = request.POST.get('text', '')

        # Save image to the filesystem
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'posts'))
        filename = fs.save(image.name, image)
        image_path = os.path.join('posts', filename)  # Save relative path to DB

        try:
            # Connect to MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234@Bcd',
                database='etchlin_db'
            )
            cursor = conn.cursor()
            user_id = request.user.id  # assuming the user is logged in

            # Insert the post into the database
            query = "INSERT INTO post (user_id, image, text, created_at) VALUES (%s, %s, %s, NOW())"
            cursor.execute(query, (user_id, image_path, text))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            # Success message
            messages.success(request, "Post created successfully!")
            return redirect('some_success_page')  # Redirect to the appropriate page

        except mysql.connector.Error as err:
            # Handle database errors
            messages.error(request, f"Error: {err}")
            return redirect('error_page')  # Redirect to an error page or home

    return render(request, 'post_form.html')
