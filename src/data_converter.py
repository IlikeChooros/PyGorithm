from NeuralNetwork import Data

class DataConverter:
    def prepare_data_txt(self, path: str):
        f = open(path,"r")
        data = f.readlines()
        f.close()
        training_inputs = []
        for i in range(len(data)):
            training_inputs.append(data[i].split())
        for i in range(len(training_inputs)):
            for j in range(len(training_inputs[i])):
                training_inputs[i][j] = float(training_inputs[i][j])
        
        return training_inputs

    def list_to_Data(self, data: list, inputs, outputs):
        
        ret = []
        for list in data:
            
            outputs_l = []
            inputs_l = []

            inputs_l += [list[i] for i in range(len(list)-outputs)]
            outputs_l += [list[i] for i in range(inputs, len(list))]

            ret.append(Data(inputs_l, outputs_l))

        return ret
    
