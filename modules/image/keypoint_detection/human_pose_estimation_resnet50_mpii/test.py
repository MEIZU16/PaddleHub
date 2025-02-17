import os
import shutil
import unittest

import cv2
import requests
import paddlehub as hub


os.environ['CUDA_VISIBLE_DEVICES'] = '0'


class TestHubModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        img_url = 'https://ai-studio-static-online.cdn.bcebos.com/7799a8ccc5f6471b9d56fb6eff94f82a08b70ca2c7594d3f99877e366c0a2619'
        if not os.path.exists('tests'):
            os.makedirs('tests')
        response = requests.get(img_url)
        assert response.status_code == 200, 'Network Error.'
        with open('tests/test.jpg', 'wb') as f:
            f.write(response.content)
        cls.module = hub.Module(name="human_pose_estimation_resnet50_mpii")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('tests')
        shutil.rmtree('inference')
        shutil.rmtree('output_pose')

    def test_keypoint_detection1(self):
        results = self.module.keypoint_detection(
            paths=['tests/test.jpg']
        )
        kps = results[0]['data']
        self.assertIsInstance(kps, dict)

    def test_keypoint_detection2(self):
        results = self.module.keypoint_detection(
            images=[cv2.imread('tests/test.jpg')]
        )
        kps = results[0]['data']
        self.assertIsInstance(kps, dict)

    def test_keypoint_detection3(self):
        results = self.module.keypoint_detection(
            images=[cv2.imread('tests/test.jpg')],
            visualization=True
        )
        kps = results[0]['data']
        self.assertIsInstance(kps, dict)

    def test_keypoint_detection4(self):
        results = self.module.keypoint_detection(
            images=[cv2.imread('tests/test.jpg')],
            use_gpu=True
        )
        kps = results[0]['data']
        self.assertIsInstance(kps, dict)

    def test_keypoint_detection5(self):
        self.assertRaises(
            AssertionError,
            self.module.keypoint_detection,
            paths=['no.jpg']
        )

    def test_keypoint_detection6(self):
        self.assertRaises(
            AttributeError,
            self.module.keypoint_detection,
            images=['test.jpg']
        )

    def test_save_inference_model(self):
        self.module.save_inference_model('./inference/model')

        self.assertTrue(os.path.exists('./inference/model.pdmodel'))
        self.assertTrue(os.path.exists('./inference/model.pdiparams'))


if __name__ == "__main__":
    unittest.main()
