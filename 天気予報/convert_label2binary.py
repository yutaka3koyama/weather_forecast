def convert_label2binary(group_type, label) :
    if group_type == 'cloud' :
        index = [0] * 3
        if label.startswith('cy') :
            index[0] = 1
        elif label.startswith('cf') :
            index[1] = 1
        elif label.startswith('cn'):
            index[2] = 1
    elif group_type == 'rain' :
        index = [0] * 3
        if label.endswith('ry') :
            index[0] = 1
        elif label.endswith('rf') :
            index[1] = 1
        elif label.endswith('rn'):
            index[2] = 1
    elif group_type == 'all' :
        index = [0] * 9
        if label == 'cyry' :
            index[0] = 1
        elif label == 'cyrf' :
            index[1] = 1
        elif label == 'cyrn' :
            index[2] = 1
        elif label == 'cfry' :
            index[3] = 1
        elif label == 'cfrf' :
            index[4] = 1
        elif label == 'cfrn' :
            index[5] = 1
        elif label == 'cnry' :
            index[6] = 1
        elif label == 'cnrf' :
            index[7] = 1
        elif label == 'cnrn' :
            index[8] = 1
    return index