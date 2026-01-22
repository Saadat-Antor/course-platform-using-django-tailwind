from django.template.loader import get_template
from django.conf import settings

def get_cloudinary_image_obj(instance, 
                       field_name='image',
                       as_html=False,
                       width=1200):
    if not hasattr(instance, field_name):
          return ""
    image_obj = getattr(instance, field_name)
    if not image_obj:
            return ""
    image_options = {
        "width": width
    }
    if as_html:
          return image_obj.image(**image_options)
    url =image_obj.build_url(**image_options)
    return url


def get_cloudinary_video_obj(instance, 
                       field_name='video',
                       as_html=False,
                       sign_url=False,
                       width=None,
                       height=None,
                       fetch_format='auto',
                       quality='auto',
                       controls=True,
                       autoplay=True):
    if not hasattr(instance, field_name):
          return ""
    video_obj = getattr(instance, field_name)
    if not video_obj:
            return ""
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "controls": controls,
        "autoplay": autoplay
    }
    if width is not None:
        video_options['width'] = width
    if height is not None:
        video_options['crop'] = 'limit'

    url =video_obj.build_url(**video_options)
    
    if as_html:
          cloud_name = settings.CLOUDINARY_CLOUD_NAME
          template_name = "videos\\snippets\\embed.html"
          base_color = "#7851A9"
          tmpl = get_template(template_name)
          _html = tmpl.render({"video_url": url, 
                               "cloud_name": cloud_name,
                               "base_color": base_color})
          return _html
    return url