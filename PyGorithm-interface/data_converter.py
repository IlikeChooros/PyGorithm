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
    
