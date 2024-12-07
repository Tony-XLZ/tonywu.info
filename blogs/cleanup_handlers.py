import re
import os
from django.core.files.storage import default_storage
from django_cleanup.signals import cleanup_pre_delete


def cleanup_empty_directories(base_path):
    """
    Recursively check and delete empty directories, starting from the deepest level
    """
    # Walk through the directory tree from bottom to top
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # If the directory is empty, delete it
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def cleanup_ckeditor_images(sender, instance, **kwargs):
    """
    Clean up images referenced in CKEditor content and remove empty directories
    """
    if hasattr(instance, 'content'):
        content = instance.content  # Replace with the actual rich text field name
        # Find all image paths, e.g., uploads/2024/12/07/image.jpg
        image_urls = re.findall(r'uploads/\d{4}/\d{2}/\d{2}/[^\s"]+', content)

        for image_url in image_urls:
            # Build the file path
            file_path = image_url
            if default_storage.exists(file_path):
                # Delete the file
                default_storage.delete(file_path)

        # Get the base directory for uploads, e.g., uploads/
        upload_base_path = os.path.join(default_storage.location, "uploads")
        cleanup_empty_directories(upload_base_path)


# Connect the signal
cleanup_pre_delete.connect(cleanup_ckeditor_images)
