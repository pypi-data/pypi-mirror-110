import onnx
from onnx2kerastl import onnx_to_keras


def main():
    onnx_file_path = "/Users/dorhar/PycharmProjects/treatment_recommendation 10.35.22/run_files/conv_model.onnx"

    # Load ONNX model
    onnx_model = onnx.load(onnx_file_path)

    # Call the converter (input - is the main model input name, can be different for your model)
    input_names = [input.name for input in onnx_model.graph.input]
    k_model = onnx_to_keras(onnx_model, input_names=input_names,
                            name_policy='renumerate')

    print("DONE")


if __name__ == '__main__':
    main()
