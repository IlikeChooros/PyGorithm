class OpenData():
    def open_data(self,file_path):
        f = open(file_path,"r")
        data = f.readlines()
        f.close()
        training_inputs = []#[x,y,przynaleznosc]
        for i in range(len(data)):
            training_inputs.append(data[i].split())
        for i in range(len(training_inputs)):
            for j in range(len(training_inputs[i])):
                training_inputs[i][j] = float(training_inputs[i][j])
        return training_inputs
