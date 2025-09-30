from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_gps_from_image(image_path):
    """
    Extract GPS coordinates from an image's EXIF data.
    Returns (latitude, longitude) as floats if available, else (None, None).
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if not exif_data:
            return None, None

        gps_info = {}
        for tag, value in exif_data.items():
            decoded_tag = TAGS.get(tag, tag)
            if decoded_tag == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]

        if not gps_info:
            return None, None

        # Helper to convert GPS coordinates
        def convert_to_degrees(coord):
            d, m, s = coord
            return d[0]/d[1] + m[0]/m[1]/60 + s[0]/s[1]/3600

        lat = convert_to_degrees(gps_info["GPSLatitude"])
        lon = convert_to_degrees(gps_info["GPSLongitude"])
        if gps_info.get("GPSLatitudeRef") != "N":
            lat = -lat
        if gps_info.get("GPSLongitudeRef") != "E":
            lon = -lon

        return lat, lon

    except Exception as e:
        # If any error occurs (no EXIF, wrong format), return None
        return None, None
