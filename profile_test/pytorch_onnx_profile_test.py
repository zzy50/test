import torch
import time


def test_torch():
    input = torch.rand(1, 128, 48, 48, 48, dtype=torch.float32, requires_grad=False).to('cuda')
    model = torch.nn.Upsample(scale_factor=2, mode='nearest').cuda()

    torch.set_grad_enabled(False)

    for _ in range(3): # warm up
        model(input)
    
    latency = []
    for _ in range(100):
        input = torch.rand(1, 128, 48, 48, 48, dtype=torch.float32, requires_grad=False).to('cuda') # input is in GPU
        torch.cuda.synchronize()
        start = time.time()
        output = model(input)
        torch.cuda.synchronize()
        end = time.time()
        latency.append(end-start)
    average_latency_in_ms = 1000 * sum(latency) / len(latency)
    print(f"Torch latency: {average_latency_in_ms:.2f} ms")


def export_onnx():
    input = torch.rand(1, 128, 48, 48, 48, dtype=torch.float32, requires_grad=False).to('cuda')
    model = torch.nn.Upsample(scale_factor=2, mode='nearest').cuda()
    torch.onnx.export(model, input, "upsample.onnx", input_names=["input"], output_names=["output"], opset_version=11)


def test_onnx():
    import onnxruntime
    import numpy as np
    options = onnxruntime.SessionOptions()
    session = onnxruntime.InferenceSession("upsample.onnx", options, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])

    input = torch.rand(1, 128, 48, 48, 48, dtype=torch.float32, requires_grad=False).to('cuda')
    input_tensor = input.contiguous()
    output_tensor = torch.empty((1, 128, 96, 96, 96), dtype=torch.float32, device='cuda:0').contiguous()

    binding = session.io_binding()
    binding.bind_input(
        name='input',
        device_type='cuda',
        device_id=0,
        element_type=np.float32,
        shape=tuple(input_tensor.shape),
        buffer_ptr=input_tensor.data_ptr(),
        )
    binding.bind_output(
        name='output',
        device_type='cuda',
        device_id=0,
        element_type=np.float32,
        shape=tuple(output_tensor.shape),
        buffer_ptr=output_tensor.data_ptr(),
    )

    for _ in range(3): # warm up
        session.run_with_iobinding(binding)

    ort_latency = []
    for _ in range(100):
        input = torch.rand(1, 128, 48, 48, 48, dtype=torch.float32, requires_grad=False).to('cuda') # input is in GPU
        input_tensor = input.contiguous()
        start = time.time()
        binding.bind_input(
                name='input',
                device_type='cuda',
                device_id=0,
                element_type=np.float32,
                shape=tuple(input_tensor.shape),
                buffer_ptr=input_tensor.data_ptr(),
                )
        session.run_with_iobinding(binding)
        end = time.time()
        ort_latency.append(end - start)

    average_latency_in_ms = 1000 * sum(ort_latency) / len(ort_latency)
    print(f"Ort Latency: {average_latency_in_ms:.2f} ms")
    
test_torch()
export_onnx()
test_onnx()