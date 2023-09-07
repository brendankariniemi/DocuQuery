from caching import cache_data


def handle_upload(file):
    if file and file.filename:
        file_path = 'documents/' + file.filename
        try:
            file.save(file_path)
            cache_data('uploaded_file', file_path)
            return file_path, 0
        except Exception as e:
            return str(e), 400
    return None, 404
