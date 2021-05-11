import os
from mmdet.apis import init_detector, inference_detector
from .utils import show_result


class Model:
    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
        self.config_file = os.path.join(root_dir, 'model_files', 'cascade_mask_rcnn_hrnetv2p_w32_20e.py')
        self.checkpoint_file = os.path.join(root_dir, 'model_files',
                                            'ICDAR.19.Track.B2.Modern.table.structure.recognition.v2.pth')
        self.model = None

    def build_model(self):
        self.model = init_detector(self.config_file, self.checkpoint_file, device='cpu')

    def predict(self, image_path):
        result = inference_detector(self.model, image_path)
        table_coords = show_result(image_path, result,
                                   ('Bordered', 'cell', 'Borderless'),
                                   score_thr=0.85, out_file='predicted.png')
        return table_coords


