import numpy as np

import triton_python_backend_utils as pb_utils

CLASS_NAMES = ["violence", "accident", "normal"]

class TritonPythonModel:

    def execute(self, requests):
        responses = [] 
        for request in requests:
            raw_logits = pb_utils.get_input_tensor_by_name(request, "logits")
            logits = raw_logits.as_numpy() # 1, NUM_CLASS 
            print('-----------------------')
            print(logits.shape)
            pred = np.argmax(logits, axis=-1)
            label = [CLASS_NAMES[i] for i in pred]

            output_tensor = pb_utils.Tensor.from_numpy(
                "label", np.array(label, dtype=object).reshape(1)
            ) 

            inference_response = pb_utils.InferenceResponse(
                output_tensors=[output_tensor]
            )
            responses.append(inference_response)
        return responses