import os
import unittest
import wallaroo.sdk as wl

class Test(unittest.TestCase):

    dirname = os.path.dirname(__file__)
    model_filename = os.path.join(dirname, '../../test_resources/keras_ccfraud.onnx')
    data_filename = os.path.join(dirname, '../../test_resources/tensor.json')

    def setUp(self):
        fitz = wl.Engine(host='localhost', debug=False)
        self.assertIsNotNone(fitz)

    def test_smoke(self):
        fitz = wl.Engine(host='localhost', debug=False)
        fitz.upload_model("2", "2", self.model_filename)

        tensor = { "tensor": [[1.0678324729342086, 0.21778102664937624, -1.7115145261843976, 0.6822857209662413,
                               1.0138553066742804, -0.43350000129006655, 0.7395859436561657, -0.28828395953577357,
                               -0.44726268795990787, 0.5146124987725894, 0.3791316964287545, 0.5190619748123175,
                               -0.4904593221655364, 1.1656456468728567, -0.9776307444180006, -0.6322198962519854,
                               -0.6891477694494687, 0.17833178574255615, 0.1397992467197424, -0.35542206494183326,
                               0.4394217876939808, 1.4588397511627804, -0.3886829614721505, 0.4353492889350186, 1.7420053483337175,
                            -0.4434654615252943, -0.15157478906219238, -0.26684517248765616, -1.4549617756124493]] }

        r1=fitz.http_inference_tensor(2, tensor)
        r2=fitz.http_inference_file(2, self.data_filename, show_result=False)
        self.assertIsNotNone(r1)

        # fitz.update_model_config(2, [tensor])

if __name__ == '__main__':
    unittest.main()
