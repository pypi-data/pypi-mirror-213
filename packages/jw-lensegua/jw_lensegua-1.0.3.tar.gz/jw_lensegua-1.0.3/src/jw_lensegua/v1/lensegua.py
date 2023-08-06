# core - sistema de reconocimiento
import json
from jw_lensegua.solutions import *
from jw_lensegua.results_model import *

class Jw_Lensegua:

    def __init__(self, data= None):
        self._data = data
        self._results = []

    def destroy(self):
        self._data = None
        self._results = []

    def set_model(self, data):
        self._data = data

    def get_model(self):
        return self._data

    def get_results(self):
        return self._results
        
    def recognition(self):
        try:
            if len(self._data['model_body']) > 0 and len(self._data['model_face']) > 0:
                if len(self._data['model_hand'][0]['index']) > 0 or len(self._data['model_hand'][1]['index']) > 0:
                    self.recog_A(model_input=self._data)
                    self.recog_B(model_input=self._data)
                    self.recog_C(model_input=self._data)
                    self.recog_D(model_input=self._data)
                    self.recog_E(model_input=self._data)
                    #self.recog_F(model_input=self._data)
                    self.recog_G(model_input=self._data)
                    self.recog_H(model_input=self._data)
                    self.recog_I(model_input=self._data)
                    #self.recog_J(model_input=self._data)
                    self.recog_K(model_input=self._data)
                    self.recog_L(model_input=self._data)
                    self.recog_M(model_input=self._data)
                    self.recog_N(model_input=self._data)
                    self.recog_ENIE(model_input=self._data)
                    self.recog_O(model_input=self._data)
                    self.recog_P(model_input=self._data)
                    self.recog_Q(model_input=self._data)
                    self.recog_R(model_input=self._data)
                    #self.recog_S(model_input=self._data)
                    self.recog_T(model_input=self._data)
                    self.recog_U(model_input=self._data)
                    self.recog_V(model_input=self._data)
                    self.recog_W(model_input=self._data)
                    self.recog_X(model_input=self._data)
                    self.recog_Y(model_input=self._data)
                    self.recog_Z(model_input=self._data)
        except Exception as e:
            return (model_object_result(value_result=None, Error=e))
    
    def get_resultscoincidence(self):
        results = self._results
        lista_coincidencias = list(filter(lambda a: a['rule_match'], results))
        return lista_coincidencias

    #reconocimiento de datos para "A"
    def recog_A(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_A(data=data_1)
            if result['rule_match'] == False:
                result = hand_A(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_A(data=data)
        if result != None: self._results.append(result)
        return result

    #reconocimiento de datos para "B"
    def recog_B(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_B(data=data_1)
            if result['rule_match'] == False:
                result = hand_B(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_B(data=data)
        if result != None: self._results.append(result)
        return result

    #reconocimiento de datos para "C"
    def recog_C(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_C(data=data_1)
            if result['rule_match'] == False:
                result = hand_C(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_C(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "D"
    def recog_D(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_D(data=data_1)
            if result['rule_match'] == False:
                result = hand_D(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_D(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "E"
    def recog_E(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_E(data=data_1)
            if result['rule_match'] == False:
                result = hand_E(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_E(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "F"
    def recog_F(self, model_input):
        result = None
        return result

    #reconocimiento de datos para "G"
    def recog_G(self, model_input):
        result = None
        result = hand_G(model_input=model_input)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "H"
    def recog_H(self, model_input):
        result = None
        result = hand_H(model_input=model_input)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "I"
    def recog_I(self, model_input):
        result = None
        result = hand_I(model_input=model_input)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "J"
    def recog_J(self, model_input):
        result = None
        return result

    #reconocimiento de datos para "K"
    def recog_K(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_K(data=data_1)
            if result['rule_match'] == False:
                result = hand_K(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_K(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "L"
    def recog_L(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_L(data=data_1)
            if result['rule_match'] == False:
                result = hand_L(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_L(data=data)
        if result != None:  self._results.append(result)
        return result
    
    #reconocimiento de datos para "M"
    def recog_M(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_M(data=data_1)
            if result['rule_match'] == False:
                result = hand_M(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_M(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "N"
    def recog_N(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_N(data=data_1)
            if result['rule_match'] == False:
                result = hand_N(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_N(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "ENIE"
    def recog_ENIE(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_ENIE(data=data_1, data1=data_2)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "O"
    def recog_O(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_O(data=data_1)
            if result['rule_match'] == False:
                result = hand_O(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_O(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "P"
    def recog_P(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_P(data=data_1)
            if result['rule_match'] == False:
                result = hand_P(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_P(data=data)
        if result != None:  self._results.append(result)
        return result
    
    #reconocimiento de datos para "Q"
    def recog_Q(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_Q(data=data_1, data1=data_2)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "R"
    def recog_R(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_R(data=data_1)
            if result['rule_match'] == False:
                result = hand_R(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_R(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "S"
    def recog_S(self, model_input):
        result = None
        return result

    #reconocimiento de datos para "T"
    def recog_T(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_T(data=data_1, face=model_input['model_face'], body=model_input['model_body'])
            if result['rule_match'] == False:
                result = hand_T(data=data_2, face=model_input['model_face'], body=model_input['model_body'])
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_T(data=data, face=model_input['model_face'], body=model_input['model_body'])
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "U"
    def recog_U(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_U(data=data_1)
            if result['rule_match'] == False:
                result = hand_U(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_U(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "V"
    def recog_V(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_V(data=data_1)
            if result['rule_match'] == False:
                result = hand_V(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_V(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "W"
    def recog_W(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_W(data=data_1)
            if result['rule_match'] == False:
                result = hand_W(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_W(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "X"
    def recog_X(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_X(data=data_1, data1=data_2)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "Y"
    def recog_Y(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_Y(data=data_1)
            if result['rule_match'] == False:
                result = hand_Y(data=data_2)
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            result = hand_Y(data=data)
        if result != None:  self._results.append(result)
        return result

    #reconocimiento de datos para "Z"
    def recog_Z(self, model_input):
        result = None
        if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
            data_1 = model_input['model_hand'][0]['index']
            data_2 = model_input['model_hand'][1]['index']
            result = hand_Z(hand=data_1, hand_direction=model_input['model_hand'][0]['position'], body=model_input['model_body'])
            if result['rule_match'] == False:
                result = hand_Z(hand=data_2, hand_direction=model_input['model_hand'][1]['position'], body=model_input['model_body'])
        else:
            data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
            hand_directions = model_input['model_hand'][0]['position'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['position']
            result = hand_Z(hand=data, hand_direction=hand_directions, body=model_input['model_body'])
        if result != None:  self._results.append(result)
        return result


###############################
"""
solution = Jw_Lensegua()

f = open('tests\\muestras_json\\B.json')
data = json.load(f)
print("---------------   ")
solution.set_model(data=data)
solution.recognition()
resultado_final = solution.get_resultscoincidence()
print(resultado_final)
print("---------------")
f.close()

VALUES = list("ABCDEGHIKLMNOPQRTUVWXYZ")
VALUES.append("ENIE")
VALUES.append("P1")
VALUES.append("Y1")
VALUES.append("Z1")
for idx, file in enumerate(VALUES):
    f = open('tests\\muestras_json\\'+file+'.json')
    data = json.load(f)
    print("---------------   "+ file)
    solution.set_model(data=data)
    solution.recognition()
    resultado_final = solution.get_resultscoincidence()
    print(resultado_final)
    solution.destroy()
    f.close()
"""