import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import time
import json

# APIキーとエンドポイントは秘匿ファイルから読み込み
with open('02_secret.json') as f:
    secret = json.load(f)
subscription_key = secret['KEY']
endpoint = secret['ENDPOINT']

# AzureのAPIをたたく
computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key))

# AzureのAPIのうち、画像からタグ情報を取り出す処理


def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result_local.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

# AzureのAPIのうち、画像から物体の位置と名前を検出する処理


def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results_local = computervision_client.detect_objects_in_stream(
        local_image)
    objects = detect_objects_results_local.objects
    return objects


# Streamlitにより、Web画面へ出力
st.title('Recognize_Object_App')
# 画像アップロードの処理
uploaded_file = st.file_uploader('Choose an Image', type=['jpg', 'png'])

# 画像への矩形描画
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    # 描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50)
        text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x, y), (x+w, y+h)], fill=None,
                       outline='green', width=5)
        draw.rectangle([(x, y), (x+text_w, y+text_h)],
                       fill='green', outline='green', width=5)
        draw.text((x, y), caption, fill='white', font=font)

    st.image(img)

    # タグの表示
    st.markdown('**認識されたコンテンツタグ**')
    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    st.markdown(f'>{tags_name}')

"""
```python
import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import time
import json

#APIキーとエンドポイントは秘匿ファイルから読み込み
with open('02_secret.json') as f:
    secret = json.load(f)
subscription_key = secret['KEY']
endpoint = secret['ENDPOINT']

#AzureのAPIをたたく
computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key))

#AzureのAPIのうち、画像からタグ情報を取り出す処理
def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result_local.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name

#AzureのAPIのうち、画像から物体の位置と名前を検出する処理
def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results_local = computervision_client.detect_objects_in_stream(
        local_image)
    objects = detect_objects_results_local.objects
    return objects

#Streamlitにより、Web画面へ出力
st.title('Recognize_Object_App')
#画像アップロードの処理
uploaded_file = st.file_uploader('Choose an Image', type=['jpg', 'png'])

#画像への矩形描画
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    # 描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50)
        text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x, y), (x+w, y+h)], fill=None,
                       outline='green', width=5)
        draw.rectangle([(x, y), (x+text_w, y+text_h)],
                       fill='green', outline='green', width=5)
        draw.text((x, y), caption, fill='white', font=font)

    st.image(img)

    #タグの表示
    st.markdown('**認識されたコンテンツタグ**')
    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    st.markdown(f'>{tags_name}')
```
"""
