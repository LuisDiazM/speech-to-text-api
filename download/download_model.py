from faster_whisper import download_model
import os
"""
sizes_availables:
tiny, tiny.en, base, base.en,
small, small.en, medium, medium.en, large-v1, large-v2, large-v3
"""
size_avaliable = "tiny"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'download','models')



if __name__ == "__main__":
    download_model(size_or_id=size_avaliable, output_dir=TEMPLATE_DIR)