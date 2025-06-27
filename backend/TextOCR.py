from paddleocr import PaddleOCR
from flask import jsonify
import cv2
import tempfile
import os

# 初始化OCR引擎（使用中英文模型）
ocr = PaddleOCR(use_angle_cls=True, lang="ch",enable_mkldnn=False,
                det_model_dir='.paddleocr/whl/det',
    rec_model_dir='.paddleocr/whl/rec',
    cls_model_dir='.paddleocr/whl/cls')

class TextOCR:
    @staticmethod
    def preprocess_image(img):
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # 二值化
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # 降噪
        denoised = cv2.fastNlMeansDenoising(thresh, h=10)
        return denoised

    @staticmethod
    def ocr_processing(InputData):
        # 检查文件上传
        if 'file' not in InputData.files:
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400

        file = InputData.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'Empty filename'}), 400

        try:
            # 保存临时文件
            _, temp_path = tempfile.mkstemp()
            file.save(temp_path)

            # 读取并处理图片
            img = cv2.imread(temp_path)
            img = TextOCR.preprocess_image(img)

            # OCR识别
            result = ocr.ocr(img, cls=True)
            texts = [line[1][0] for line in result[0]] if result else []

            return jsonify({
                'status': 'success',
                'result': '\n'.join(texts),
                'filename': file.filename
            })

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        finally:
            # if os.path.exists(temp_path):
            #    os.remove(temp_path)
            pass
