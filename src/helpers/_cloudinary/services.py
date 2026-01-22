

def get_cloudinary_image_obj(instance, 
                       field_name='image',
                       as_html=False,
                       width=1200):
    if not instance.image:
            return ""
    image_options = {
        "width": width
    }
    if as_html:
          return instance.image.image(**image_options)
    url =instance.image.build_url(**image_options)
    return url