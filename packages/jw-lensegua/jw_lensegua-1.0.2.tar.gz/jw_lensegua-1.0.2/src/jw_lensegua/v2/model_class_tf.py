import abc
import pandas as pd
import numpy as np
import model_kmean_tf2 as mk

## interface models

class Imodel:
    @abc.abstractmethod
    def get_result(self, data) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_model_movement(self) -> object:
        raise NotImplementedError

class IHands:
    @abc.abstractmethod
    def get_model(self) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def get_model_movement(self) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def make_model_diff(self):
        raise NotImplementedError
    

## train model

class TrainModel:
    def __init__(self, label="", data=[], hands_relation=False, face_relation=False, body_relation=False, move_relation=False):
        self._label = label
        self._data = data
        self._body_relation = body_relation
        self._face_relation = face_relation
        self._hand_relation = hands_relation
        self._move_relation = move_relation
        self.__model_evaluation = []
        self.__data_model = []

    def getConfiguration(self):
        return {
            'label': self._label,
            'hands_relation': self._hand_relation,
            'face_relation': self._face_relation,
            'body_relation': self._body_relation,
            'move_relation': self._move_relation
        }
    
    def isMoveRelation(self):
        return self._move_relation

    def getModel_Evaluation(self):
        return [
            self.__model_evaluation     ###model evaluation normal
        ]
    
    def getModel_Train(self):
        if not (self._move_relation):
            #individual relation - def data by group
            try:
                self.__data_model = [
                    [],[],[],[],[], #1-5
                    [],[],[],[],[], #6-10
                    [],[],[],[],[], #11-15
                    [],[],[],[],[], #16-20
                    [],[],[],[]     #21-23
                ] 
                
                for val in self._data:
                    test = HandModel(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=self._face_relation, body_relation=self._body_relation)
                    value_model = test.get_model()
                    for i in range(len(value_model)):
                        if len(value_model[i])>0:
                            self. __data_model[i].append(value_model[i])
            except Exception as e:
                print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
                self.__data_model = []

    def getModel_TrainMov_pre(self):
        try:
            data_tmp = []
            for i in range(len(self._data)):
                for j in range(len(self._data[i])):
                    if len(data_tmp) < (j+1):
                        data_tmp.append([])
                    data_tmp[j].append(self._data[i][j])
            return data_tmp
        except Exception as e:
                print("Error Ocurrido [Train model Mov], Mensaje: {0}".format(str(e)))
                return []

    def getModel_TrainMov(self):
        try:
            self.__data_model = []
            datos = self.getModel_TrainMov_pre()

            for j in range(len(datos)):
                self.__data_model.append([
                    [],[],[],[],[], #1-5
                    [],[],[],[],[], #6-10
                    [],[],[],[],[], #11-15
                    [],[],[],[],[], #16-20
                    [],[],[],[]     #21-23
                ])
                for i in range(len(datos[j])):
                    val = datos[j][i]
                    test = HandModel(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=self._face_relation, body_relation=self._body_relation)
                    value_model = test.get_model()
                    for k in range(len(value_model)):
                        if len(value_model[k])>0:
                            self. __data_model[j][k].append(value_model[k])

        except Exception as e:
                print("Error Ocurrido [Train model Mov], Mensaje: {0}".format(str(e)))
                self.__data_model = []


    def Train_modelsMov(self):
        try:
            self.getModel_TrainMov()
            self.__model_evaluation = []

            if len(self.__data_model)>0:

                for g in range(len(self.__data_model)):
                    value_model = self.__data_model[g]
                    model_evaluation_tmp = []
                    
                    for h in range(24):
                        if len(value_model[h])>0:
                            #recuperation data - transform model pandas - transpose matrix
                            value_add = []
                            data = value_model[h]
                            for j in range(len(data[0])):
                                tmp = []
                                for vals in data:
                                    for k in range(len(vals)):
                                        if j==k:
                                            tmp.append(vals[k])
                                value_add.append(tmp)
                            
                            #transformation data
                            df = pd.DataFrame(value_add)
                            df_real = df.transpose()
                            KmeansModel = []
                            for i in range(len(df_real.columns)):
                                data_Train = np.array(df_real[i].values.tolist())
                                km_tmp = None
                                if (len(df_real.columns) > len(df_real)):
                                    if self._move_relation == False and self._face_relation == False and self._body_relation == False:
                                        km_tmp = mk.KMeansNov_2(n_clusters=len(df_real)) #model_Evaluation n_cluster by columns recognized
                                    else:
                                        km_tmp = mk.KMeansMov_2(n_clusters=len(df_real)) #model_Evaluation n_cluster by columns recognized
                                else:
                                    if self._move_relation == False and self._face_relation == False and self._body_relation == False:
                                        km_tmp = mk.KMeansNov_2(n_clusters=len(df_real.columns)) #model_Evaluation n_cluster by columns recognized
                                    else:
                                        km_tmp = mk.KMeansMov_2(n_clusters=len(df_real.columns)) #model_Evaluation n_cluster by columns recognized
                                    
                                km_tmp.fit(data_Train)
                                KmeansModel.append(km_tmp) ##define model_by column

                            model_evaluation_tmp.append(KmeansModel)  
                    
                    if len(model_evaluation_tmp)>0: self.__model_evaluation.append(model_evaluation_tmp)
        except Exception as e:
            print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
            self.__model_evaluation = []

    def Train_models(self):
        try:
            self.getModel_Train()
            self.__model_evaluation = []

            if len(self.__data_model)>0:
                value_model = self.__data_model
                
                for h in range(24):
                    if len(value_model[h])>0:
                        #recuperation data - transform model pandas - transpose matrix
                        value_add = []
                        data = value_model[h]
                        for j in range(len(data[0])):
                            tmp = []
                            for vals in data:
                                for k in range(len(vals)):
                                    if j==k:
                                        tmp.append(vals[k])
                            value_add.append(tmp)
                        
                        #transformation data
                        df = pd.DataFrame(value_add)
                        df_real = df.transpose()
                        KmeansModel = []
                        for i in range(len(df_real.columns)):
                            data_Train = np.array(df_real[i].values.tolist())
                            km_tmp = None
                            if (len(df_real.columns) > len(df_real)):
                                if self._move_relation == False and self._face_relation == False and self._body_relation == False:
                                    km_tmp = mk.KMeansNov_2(n_clusters=len(df_real)) #model_Evaluation n_cluster by columns recognized
                                else:
                                    km_tmp = mk.KMeansMov_2(n_clusters=len(df_real)) #model_Evaluation n_cluster by columns recognized
                            else:
                                if self._move_relation == False and self._face_relation == False and self._body_relation == False:
                                    km_tmp = mk.KMeansNov_2(n_clusters=len(df_real.columns)) #model_Evaluation n_cluster by columns recognized
                                else:
                                    km_tmp = mk.KMeansMov_2(n_clusters=len(df_real.columns)) #model_Evaluation n_cluster by columns recognized
                                
                            km_tmp.fit(data_Train)
                            KmeansModel.append(km_tmp) ##define model_by column
                            
                        self.__model_evaluation.append(KmeansModel)

        except Exception as e:
            print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
            self.__model_evaluation = []

## hand model

class HandModel(IHands):
    
    def __init__(self, hand_Left, hand_Right,points_body, face_relation=False, body_relation=False):
        self._hand_Left = hand_Left
        self._hand_Right = hand_Right
        self._points_body = points_body
        self._face_relation= face_relation
        self._body_relation = body_relation
        ### hands_difference
        self._points_hand_Right_diffX = []
        self._points_hand_Right_diffY = []
        self._points_hand_Right_diffZ = []
        self._points_hand_Left_diffX = []
        self._points_hand_Left_diffY = []
        self._points_hand_Left_diffZ = []
        ## body difference
        self._points_body_diffX = []
        self._points_body_diffY = []
        self._points_body_diffZ = []
        ## hands_body relation
        self._points_body_relation_diffX = []
        self._points_body_relation_diffY = []
        self._points_body_relation_diffZ = []
        ## hands_face relation
        self._points_face_relation_diffXLeft = []
        self._points_face_relation_diffYLeft = []
        self._points_face_relation_diffZLeft = []
        self._points_face_relation_diffXRight = []
        self._points_face_relation_diffYRight = []
        self._points_face_relation_diffZRight = []
        ## body_face relation
        self._points_body_face_relation_diffXLeft = []
        self._points_body_face_relation_diffYLeft = []
        self._points_body_face_relation_diffZLeft = []
        self._points_body_face_relation_diffXRight = []
        self._points_body_face_relation_diffYRight = []
        self._points_body_face_relation_diffZRight = []
        #model_Exec
        try:
            self.make_model_diff()
        except Exception as e:
            print("Error Ocurrido [Hand model], Mensaje: {0}".format(str(e)))

    def get_model(self):
        return [
            ## hands_difference
            self._points_hand_Right_diffX,#0
            self._points_hand_Right_diffY,#1
            self._points_hand_Right_diffZ,#2
            self._points_hand_Left_diffX,#3
            self._points_hand_Left_diffY,#4
            self._points_hand_Left_diffZ,#5
            ## body difference
            self._points_body_diffX,#6
            self._points_body_diffY,#7
            self._points_body_diffZ,#8
            ## hands_body relation
            self._points_body_relation_diffX,#9
            self._points_body_relation_diffY,#10
            self._points_body_relation_diffZ,#11
            ## hands_face relation
            self._points_face_relation_diffXRight,#12
            self._points_face_relation_diffYRight,#13
            self._points_face_relation_diffZRight,#14
            self._points_face_relation_diffXLeft,#15
            self._points_face_relation_diffYLeft,#16
            self._points_face_relation_diffZLeft,#17
            ## body_face relation - verify 
            self._points_body_face_relation_diffXRight,#18
            self._points_body_face_relation_diffYRight,#19
            self._points_body_face_relation_diffZRight,#20
            self._points_body_face_relation_diffXLeft,#21
            self._points_body_face_relation_diffYLeft,#22
            self._points_body_face_relation_diffZLeft#23
        ]
        
    def make_model_diff(self):
        ## hands
        if len(self._hand_Right) > 0:
            hands_x = list(map(lambda a: (a['transform_x']), self._hand_Right))
            hands_y = list(map(lambda a: (a['transform_y']), self._hand_Right))
            hands_z = list(map(lambda a: (a['transform_z']), self._hand_Right))
            
            self._points_hand_Right_diffX = [
                [4  ,(hands_x[4]-hands_x[3])],   [3  ,(hands_x[3]-hands_x[2])],   [2  ,(hands_x[2]-hands_x[1])],
                [8  ,(hands_x[8]-hands_x[7])],   [7  ,(hands_x[7]-hands_x[6])],   [6  ,(hands_x[6]-hands_x[5])],
                [12 ,(hands_x[12]-hands_x[11])], [11 ,(hands_x[11]-hands_x[10])], [10 ,(hands_x[10]-hands_x[9])],
                [16 ,(hands_x[16]-hands_x[15])], [15 ,(hands_x[15]-hands_x[14])], [14 ,(hands_x[14]-hands_x[13])],
                [20 ,(hands_x[20]-hands_x[19])], [19 ,(hands_x[19]-hands_x[18])], [18 ,(hands_x[18]-hands_x[17])],
                [1  ,(hands_x[1]-hands_x[0])],   [5  ,(hands_x[5]-hands_x[0])],   [9  ,(hands_x[9]-hands_x[0])],    [13 ,(hands_x[13]-hands_x[0])],  [17 ,(hands_x[17]-hands_x[0])],
                [4  ,(hands_x[4]-hands_x[8])],   [8  ,(hands_x[8]-hands_x[12])],  [12 ,(hands_x[12]-hands_x[16])],  [16 ,(hands_x[16]-hands_x[20])],
                [3  ,(hands_x[3]-hands_x[7])],   [7  ,(hands_x[7]-hands_x[11])],  [11 ,(hands_x[11]-hands_x[15])],  [15 ,(hands_x[15]-hands_x[19])],
                [2  ,(hands_x[2]-hands_x[6])],   [6  ,(hands_x[6]-hands_x[10])],  [10 ,(hands_x[10]-hands_x[14])],  [14 ,(hands_x[14]-hands_x[18])],
                [1  ,(hands_x[1]-hands_x[5])],   [5  ,(hands_x[5]-hands_x[9])],   [9  ,(hands_x[9]-hands_x[13])],   [13 ,(hands_x[13]-hands_x[17])]
            ]
            self._points_hand_Right_diffX = [[x[1],x[0]] for x in self._points_hand_Right_diffX]
            self._points_hand_Right_diffY = [
                [4  ,(hands_y[4]-hands_y[3])],   [3  ,(hands_y[3]-hands_y[2])],   [2  ,(hands_y[2]-hands_y[1])],
                [8  ,(hands_y[8]-hands_y[7])],   [7  ,(hands_y[7]-hands_y[6])],   [6  ,(hands_y[6]-hands_y[5])],
                [12 ,(hands_y[12]-hands_y[11])], [11 ,(hands_y[11]-hands_y[10])], [10 ,(hands_y[10]-hands_y[9])],
                [16 ,(hands_y[16]-hands_y[15])], [15 ,(hands_y[15]-hands_y[14])], [14 ,(hands_y[14]-hands_y[13])],
                [20 ,(hands_y[20]-hands_y[19])], [19 ,(hands_y[19]-hands_y[18])], [18 ,(hands_y[18]-hands_y[17])],
                [1  ,(hands_y[1]-hands_y[0])],   [5  ,(hands_y[5]-hands_y[0])],   [9  ,(hands_y[9]-hands_y[0])],    [13 ,(hands_y[13]-hands_y[0])],  [17 ,(hands_y[17]-hands_y[0])],
                [4  ,(hands_y[4]-hands_y[8])],   [8  ,(hands_y[8]-hands_y[12])],  [12 ,(hands_y[12]-hands_y[16])],  [16 ,(hands_y[16]-hands_y[20])],
                [3  ,(hands_y[3]-hands_y[7])],   [7  ,(hands_y[7]-hands_y[11])],  [11 ,(hands_y[11]-hands_y[15])],  [15 ,(hands_y[15]-hands_y[19])],
                [2  ,(hands_y[2]-hands_y[6])],   [6  ,(hands_y[6]-hands_y[10])],  [10 ,(hands_y[10]-hands_y[14])],  [14 ,(hands_y[14]-hands_y[18])],
                [1  ,(hands_y[1]-hands_y[5])],   [5  ,(hands_y[5]-hands_y[9])],   [9  ,(hands_y[9]-hands_y[13])],   [13 ,(hands_y[13]-hands_y[17])]
            ]
            self._points_hand_Right_diffY = [[x[1],x[0]] for x in self._points_hand_Right_diffY]
            self._points_hand_Right_diffZ = [
                [4  ,(hands_z[4]-hands_z[3])],   [3  ,(hands_z[3]-hands_z[2])],   [2  ,(hands_z[2]-hands_z[1])],
                [8  ,(hands_z[8]-hands_z[7])],   [7  ,(hands_z[7]-hands_z[6])],   [6  ,(hands_z[6]-hands_z[5])],
                [12 ,(hands_z[12]-hands_z[11])], [11 ,(hands_z[11]-hands_z[10])], [10 ,(hands_z[10]-hands_z[9])],
                [16 ,(hands_z[16]-hands_z[15])], [15 ,(hands_z[15]-hands_z[14])], [14 ,(hands_z[14]-hands_z[13])],
                [20 ,(hands_z[20]-hands_z[19])], [19 ,(hands_z[19]-hands_z[18])], [18 ,(hands_z[18]-hands_z[17])],
                [1  ,(hands_z[1]-hands_z[0])],   [5  ,(hands_z[5]-hands_z[0])],   [9  ,(hands_z[9]-hands_z[0])],    [13 ,(hands_z[13]-hands_z[0])],  [17 ,(hands_z[17]-hands_z[0])],
                [4  ,(hands_z[4]-hands_z[8])],   [8  ,(hands_z[8]-hands_z[12])],  [12 ,(hands_z[12]-hands_z[16])],  [16 ,(hands_z[16]-hands_z[20])],
                [3  ,(hands_z[3]-hands_z[7])],   [7  ,(hands_z[7]-hands_z[11])],  [11 ,(hands_z[11]-hands_z[15])],  [15 ,(hands_z[15]-hands_z[19])],
                [2  ,(hands_z[2]-hands_z[6])],   [6  ,(hands_z[6]-hands_z[10])],  [10 ,(hands_z[10]-hands_z[14])],  [14 ,(hands_z[14]-hands_z[18])],
                [1  ,(hands_z[1]-hands_z[5])],   [5  ,(hands_z[5]-hands_z[9])],   [9  ,(hands_z[9]-hands_z[13])],   [13 ,(hands_z[13]-hands_z[17])]
            ]
            self._points_hand_Right_diffZ = [[x[1],x[0]] for x in self._points_hand_Right_diffZ]

        if len(self._hand_Left) > 0:

            hands_x = list(map(lambda a: (a['transform_x']), self._hand_Left))
            hands_y = list(map(lambda a: (a['transform_y']), self._hand_Left))
            hands_z = list(map(lambda a: (a['transform_z']), self._hand_Left))
            
            self._points_hand_Left_diffX = [
                [4  ,(hands_x[4]-hands_x[3])],   [3  ,(hands_x[3]-hands_x[2])],   [2  ,(hands_x[2]-hands_x[1])],
                [8  ,(hands_x[8]-hands_x[7])],   [7  ,(hands_x[7]-hands_x[6])],   [6  ,(hands_x[6]-hands_x[5])],
                [12 ,(hands_x[12]-hands_x[11])], [11 ,(hands_x[11]-hands_x[10])], [10 ,(hands_x[10]-hands_x[9])],
                [16 ,(hands_x[16]-hands_x[15])], [15 ,(hands_x[15]-hands_x[14])], [14 ,(hands_x[14]-hands_x[13])],
                [20 ,(hands_x[20]-hands_x[19])], [19 ,(hands_x[19]-hands_x[18])], [18 ,(hands_x[18]-hands_x[17])],
                [1  ,(hands_x[1]-hands_x[0])],   [5  ,(hands_x[5]-hands_x[0])],   [9  ,(hands_x[9]-hands_x[0])],    [13 ,(hands_x[13]-hands_x[0])],  [17 ,(hands_x[17]-hands_x[0])],
                [4  ,(hands_x[4]-hands_x[8])],   [8  ,(hands_x[8]-hands_x[12])],  [12 ,(hands_x[12]-hands_x[16])],  [16 ,(hands_x[16]-hands_x[20])],
                [3  ,(hands_x[3]-hands_x[7])],   [7  ,(hands_x[7]-hands_x[11])],  [11 ,(hands_x[11]-hands_x[15])],  [15 ,(hands_x[15]-hands_x[19])],
                [2  ,(hands_x[2]-hands_x[6])],   [6  ,(hands_x[6]-hands_x[10])],  [10 ,(hands_x[10]-hands_x[14])],  [14 ,(hands_x[14]-hands_x[18])],
                [1  ,(hands_x[1]-hands_x[5])],   [5  ,(hands_x[5]-hands_x[9])],   [9  ,(hands_x[9]-hands_x[13])],   [13 ,(hands_x[13]-hands_x[17])]
            ]
            self._points_hand_Left_diffX = [[x[1],x[0]] for x in self._points_hand_Left_diffX]
            self._points_hand_Left_diffY = [
                [4  ,(hands_y[4]-hands_y[3])],   [3  ,(hands_y[3]-hands_y[2])],   [2  ,(hands_y[2]-hands_y[1])],
                [8  ,(hands_y[8]-hands_y[7])],   [7  ,(hands_y[7]-hands_y[6])],   [6  ,(hands_y[6]-hands_y[5])],
                [12 ,(hands_y[12]-hands_y[11])], [11 ,(hands_y[11]-hands_y[10])], [10 ,(hands_y[10]-hands_y[9])],
                [16 ,(hands_y[16]-hands_y[15])], [15 ,(hands_y[15]-hands_y[14])], [14 ,(hands_y[14]-hands_y[13])],
                [20 ,(hands_y[20]-hands_y[19])], [19 ,(hands_y[19]-hands_y[18])], [18 ,(hands_y[18]-hands_y[17])],
                [1  ,(hands_y[1]-hands_y[0])],   [5  ,(hands_y[5]-hands_y[0])],   [9  ,(hands_y[9]-hands_y[0])],    [13 ,(hands_y[13]-hands_y[0])],  [17 ,(hands_y[17]-hands_y[0])],
                [4  ,(hands_y[4]-hands_y[8])],   [8  ,(hands_y[8]-hands_y[12])],  [12 ,(hands_y[12]-hands_y[16])],  [16 ,(hands_y[16]-hands_y[20])],
                [3  ,(hands_y[3]-hands_y[7])],   [7  ,(hands_y[7]-hands_y[11])],  [11 ,(hands_y[11]-hands_y[15])],  [15 ,(hands_y[15]-hands_y[19])],
                [2  ,(hands_y[2]-hands_y[6])],   [6  ,(hands_y[6]-hands_y[10])],  [10 ,(hands_y[10]-hands_y[14])],  [14 ,(hands_y[14]-hands_y[18])],
                [1  ,(hands_y[1]-hands_y[5])],   [5  ,(hands_y[5]-hands_y[9])],   [9  ,(hands_y[9]-hands_y[13])],   [13 ,(hands_y[13]-hands_y[17])]
            ]
            self._points_hand_Left_diffY = [[x[1],x[0]] for x in self._points_hand_Left_diffY]
            self._points_hand_Left_diffZ = [
                [4  ,(hands_z[4]-hands_z[3])],   [3  ,(hands_z[3]-hands_z[2])],   [2  ,(hands_z[2]-hands_z[1])],
                [8  ,(hands_z[8]-hands_z[7])],   [7  ,(hands_z[7]-hands_z[6])],   [6  ,(hands_z[6]-hands_z[5])],
                [12 ,(hands_z[12]-hands_z[11])], [11 ,(hands_z[11]-hands_z[10])], [10 ,(hands_z[10]-hands_z[9])],
                [16 ,(hands_z[16]-hands_z[15])], [15 ,(hands_z[15]-hands_z[14])], [14 ,(hands_z[14]-hands_z[13])],
                [20 ,(hands_z[20]-hands_z[19])], [19 ,(hands_z[19]-hands_z[18])], [18 ,(hands_z[18]-hands_z[17])],
                [1  ,(hands_z[1]-hands_z[0])],   [5  ,(hands_z[5]-hands_z[0])],   [9  ,(hands_z[9]-hands_z[0])],    [13 ,(hands_z[13]-hands_z[0])],  [17 ,(hands_z[17]-hands_z[0])],
                [4  ,(hands_z[4]-hands_z[8])],   [8  ,(hands_z[8]-hands_z[12])],  [12 ,(hands_z[12]-hands_z[16])],  [16 ,(hands_z[16]-hands_z[20])],
                [3  ,(hands_z[3]-hands_z[7])],   [7  ,(hands_z[7]-hands_z[11])],  [11 ,(hands_z[11]-hands_z[15])],  [15 ,(hands_z[15]-hands_z[19])],
                [2  ,(hands_z[2]-hands_z[6])],   [6  ,(hands_z[6]-hands_z[10])],  [10 ,(hands_z[10]-hands_z[14])],  [14 ,(hands_z[14]-hands_z[18])],
                [1  ,(hands_z[1]-hands_z[5])],   [5  ,(hands_z[5]-hands_z[9])],   [9  ,(hands_z[9]-hands_z[13])],   [13 ,(hands_z[13]-hands_z[17])]
            ]
            self._points_hand_Left_diffZ = [[x[1],x[0]] for x in self._points_hand_Left_diffZ]

        if self._body_relation and len(self._points_body)>0:

            body_x = list(map(lambda a: (a['transform_x']), self._points_body))
            body_y = list(map(lambda a: (a['transform_y']), self._points_body))
            body_z = list(map(lambda a: (a['transform_z']), self._points_body))

            ## relation into same hands
            
            self._points_body_diffX = [
                [16, (body_x[16]-body_x[14])], [16, (body_x[16]-body_x[12])], [14, (body_x[14]-body_x[12])],
                [15, (body_x[15]-body_x[13])], [15, (body_x[15]-body_x[11])], [13, (body_x[13]-body_x[11])]
            ]
            self._points_body_diffX = [[x[1],x[0]] for x in self._points_body_diffX]
            self._points_body_diffY = [
                [16, (body_y[16]-body_y[14])], [16, (body_y[16]-body_y[12])], [14, (body_y[14]-body_y[12])],
                [15, (body_y[15]-body_y[13])], [15, (body_y[15]-body_y[11])], [13, (body_y[13]-body_y[11])]
            ]
            self._points_body_diffY = [[x[1],x[0]] for x in self._points_body_diffY]
            self._points_body_diffZ = [
                [16, (body_z[16]-body_z[14])], [16, (body_z[16]-body_z[12])], [14, (body_z[14]-body_z[12])],
                [15, (body_z[15]-body_z[13])], [15, (body_z[15]-body_z[11])], [13, (body_z[13]-body_z[11])]
            ]
            self._points_body_diffZ = [[x[1],x[0]] for x in self._points_body_diffZ]

            ## relation into differents hands
            self._points_body_relation_diffX = [
                [16, (body_x[16]-body_x[15])], [12, (body_x[12]-body_x[11])], [14, (body_x[14]-body_x[13])],
                [15, (body_x[15]-body_x[16])], [11, (body_x[11]-body_x[12])], [13, (body_x[13]-body_x[14])]
            ]
            self._points_body_relation_diffX = [[x[1],x[0]] for x in self._points_body_relation_diffX]
            self._points_body_relation_diffY = [
                [16, (body_y[16]-body_y[15])], [12, (body_y[12]-body_y[11])], [14, (body_y[14]-body_y[13])],
                [15, (body_y[15]-body_y[16])], [11, (body_y[11]-body_y[12])], [13, (body_y[13]-body_y[14])]
            ]
            self._points_body_relation_diffY = [[x[1],x[0]] for x in self._points_body_relation_diffY]
            self._points_body_relation_diffZ = [
                [16, (body_z[16]-body_z[15])], [12, (body_z[12]-body_z[11])], [14, (body_z[14]-body_z[13])],
                [15, (body_z[15]-body_z[16])], [11, (body_z[11]-body_z[12])], [13, (body_z[13]-body_z[14])]
            ]
            self._points_body_relation_diffZ = [[x[1],x[0]] for x in self._points_body_relation_diffZ]

        if (self._body_relation and self._face_relation) and len(self._points_body)>0:

            body_x = list(map(lambda a: (a['transform_x']), self._points_body))
            body_y = list(map(lambda a: (a['transform_y']), self._points_body))
            body_z = list(map(lambda a: (a['transform_z']), self._points_body))

            self._points_face_relation_diffXLeft = [
                [15, (body_x[15]-body_x[8])],  [15, (body_x[15]-body_x[7])], [15, (body_x[15]-body_x[0])],
                [15, (body_x[15]-body_x[10])], [15, (body_x[15]-body_x[9])], [15, (body_x[15]-body_x[5])],
                [15, (body_x[15]-body_x[2])]
            ]
            self._points_face_relation_diffXLeft = [[x[1],x[0]] for x in self._points_face_relation_diffXLeft]
            self._points_face_relation_diffXRight = [
                [16, (body_x[16]-body_x[8])],  [16, (body_x[16]-body_x[7])], [16, (body_x[16]-body_x[0])],
                [16, (body_x[16]-body_x[10])], [16, (body_x[16]-body_x[9])], [16, (body_x[16]-body_x[5])],
                [16, (body_x[16]-body_x[2])]
            ]
            self._points_face_relation_diffXRight = [[x[1],x[0]] for x in self._points_face_relation_diffXRight]
            self._points_face_relation_diffYLeft = [
                [15, (body_y[15]-body_y[8])],  [15, (body_y[15]-body_y[7])], [15, (body_y[15]-body_y[0])],
                [15, (body_y[15]-body_y[10])], [15, (body_y[15]-body_y[9])], [15, (body_y[15]-body_y[5])],
                [15, (body_y[15]-body_y[2])]
            ]
            self._points_face_relation_diffYLeft = [[x[1],x[0]] for x in self._points_face_relation_diffYLeft]
            self._points_face_relation_diffYRight = [
                [16, (body_y[16]-body_y[8])],  [16, (body_y[16]-body_y[7])], [16, (body_y[16]-body_y[0])],
                [16, (body_y[16]-body_y[10])], [16, (body_y[16]-body_y[9])], [16, (body_y[16]-body_y[5])],
                [16, (body_y[16]-body_y[2])]
            ]
            self._points_face_relation_diffYRight = [[x[1],x[0]] for x in self._points_face_relation_diffYRight]
            self._points_face_relation_diffZLeft = [
                [15, (body_z[15]-body_z[8])],  [15, (body_z[15]-body_z[7])], [15, (body_z[15]-body_z[0])],
                [15, (body_z[15]-body_z[10])], [15, (body_z[15]-body_z[9])], [15, (body_z[15]-body_z[5])],
                [15, (body_z[15]-body_z[2])]
            ]
            self._points_face_relation_diffZLeft = [[x[1],x[0]] for x in self._points_face_relation_diffZLeft]
            self._points_face_relation_diffZRight = [
                [16, (body_z[16]-body_z[8])],  [16, (body_z[16]-body_z[7])], [16, (body_z[16]-body_z[0])],
                [16, (body_z[16]-body_z[10])], [16, (body_z[16]-body_z[9])], [16, (body_z[16]-body_z[5])],
                [16, (body_z[16]-body_z[2])]
            ]
            self._points_face_relation_diffZRight = [[x[1],x[0]] for x in self._points_face_relation_diffZRight]
        
        if (self._face_relation) and len(self._points_body)>0:

            #Left Hand
            handsL_x = list(map(lambda a: (a['transform_x']), self._hand_Left))
            handsL_y = list(map(lambda a: (a['transform_y']), self._hand_Left))
            handsL_z = list(map(lambda a: (a['transform_z']), self._hand_Left))
            #Right Hand
            handsR_x = list(map(lambda a: (a['transform_x']), self._hand_Right))
            handsR_y = list(map(lambda a: (a['transform_y']), self._hand_Right))
            handsR_z = list(map(lambda a: (a['transform_z']), self._hand_Right))
            #Body
            body_x = list(map(lambda a: (a['transform_x']), self._points_body))
            body_y = list(map(lambda a: (a['transform_y']), self._points_body))
            body_z = list(map(lambda a: (a['transform_z']), self._points_body))
            
            if (len(self._hand_Left))>0:
                ## Left Hand
                self._points_body_face_relation_diffXLeft = [
                    #thumb 
                    [4, (handsL_x[4]-body_x[5])],   [4, (handsL_x[4]-body_x[2])],   [4, (handsL_x[4]-body_x[0])],   [4, (handsL_x[4]-body_x[8])],   [4, (handsL_x[4]-body_x[7])],   [4, (handsL_x[4]-body_x[10])],   [4, (handsL_x[4]-body_x[9])],
                    [3, (handsL_x[3]-body_x[5])],   [3, (handsL_x[3]-body_x[2])],   [3, (handsL_x[3]-body_x[0])],   [3, (handsL_x[3]-body_x[8])],   [3, (handsL_x[3]-body_x[7])],   [3, (handsL_x[3]-body_x[10])],   [3, (handsL_x[3]-body_x[9])],
                    [2, (handsL_x[2]-body_x[5])],   [2, (handsL_x[2]-body_x[2])],   [2, (handsL_x[2]-body_x[0])],   [2, (handsL_x[2]-body_x[8])],   [2, (handsL_x[2]-body_x[7])],   [2, (handsL_x[2]-body_x[10])],   [2, (handsL_x[2]-body_x[9])],
                    [1, (handsL_x[1]-body_x[5])],   [1, (handsL_x[1]-body_x[2])],   [1, (handsL_x[1]-body_x[0])],   [1, (handsL_x[1]-body_x[8])],   [1, (handsL_x[1]-body_x[7])],   [1, (handsL_x[1]-body_x[10])],   [1, (handsL_x[1]-body_x[9])],
                    #wirst
                    [0, (handsL_x[0]-body_x[5])],   [0, (handsL_x[0]-body_x[2])],   [0, (handsL_x[0]-body_x[0])],   [0, (handsL_x[0]-body_x[8])],   [0, (handsL_x[0]-body_x[7])],   [0, (handsL_x[0]-body_x[10])],   [0, (handsL_x[0]-body_x[9])],
                    #index
                    [8, (handsL_x[8]-body_x[5])],   [8, (handsL_x[8]-body_x[2])],   [8, (handsL_x[8]-body_x[0])],   [8, (handsL_x[8]-body_x[8])],   [8, (handsL_x[8]-body_x[7])],   [8, (handsL_x[8]-body_x[10])],   [8, (handsL_x[8]-body_x[9])],
                    [7, (handsL_x[7]-body_x[5])],   [7, (handsL_x[7]-body_x[2])],   [7, (handsL_x[7]-body_x[0])],   [7, (handsL_x[7]-body_x[8])],   [7, (handsL_x[7]-body_x[7])],   [7, (handsL_x[7]-body_x[10])],   [7, (handsL_x[7]-body_x[9])],
                    [6, (handsL_x[6]-body_x[5])],   [6, (handsL_x[6]-body_x[2])],   [6, (handsL_x[6]-body_x[0])],   [6, (handsL_x[6]-body_x[8])],   [6, (handsL_x[6]-body_x[7])],   [6, (handsL_x[6]-body_x[10])],   [6, (handsL_x[6]-body_x[9])],
                    [5, (handsL_x[5]-body_x[5])],   [5, (handsL_x[5]-body_x[2])],   [5, (handsL_x[5]-body_x[0])],   [5, (handsL_x[5]-body_x[8])],   [5, (handsL_x[5]-body_x[7])],   [5, (handsL_x[5]-body_x[10])],   [5, (handsL_x[5]-body_x[9])],
                    #middle
                    [12, (handsL_x[12]-body_x[5])],   [12, (handsL_x[12]-body_x[2])],   [12, (handsL_x[12]-body_x[0])],   [12, (handsL_x[12]-body_x[8])],   [12, (handsL_x[12]-body_x[7])],   [12, (handsL_x[12]-body_x[10])],   [12, (handsL_x[12]-body_x[9])],
                    [11, (handsL_x[11]-body_x[5])],   [11, (handsL_x[11]-body_x[2])],   [11, (handsL_x[11]-body_x[0])],   [11, (handsL_x[11]-body_x[8])],   [11, (handsL_x[11]-body_x[7])],   [11, (handsL_x[11]-body_x[10])],   [11, (handsL_x[11]-body_x[9])],
                    [10, (handsL_x[10]-body_x[5])],   [10, (handsL_x[10]-body_x[2])],   [10, (handsL_x[10]-body_x[0])],   [10, (handsL_x[10]-body_x[8])],   [10, (handsL_x[10]-body_x[7])],   [10, (handsL_x[10]-body_x[10])],   [10, (handsL_x[10]-body_x[9])],
                    [9, (handsL_x[9]-body_x[5])],     [9, (handsL_x[9]-body_x[2])],     [9, (handsL_x[9]-body_x[0])],     [9, (handsL_x[9]-body_x[8])],     [9, (handsL_x[9]-body_x[7])],     [9, (handsL_x[9]-body_x[10])],     [9, (handsL_x[9]-body_x[9])],
                    #ring
                    [16, (handsL_x[16]-body_x[5])],   [16, (handsL_x[16]-body_x[2])],   [16, (handsL_x[16]-body_x[0])],   [16, (handsL_x[16]-body_x[8])],   [16, (handsL_x[16]-body_x[7])],   [16, (handsL_x[16]-body_x[10])],   [16, (handsL_x[16]-body_x[9])],
                    [15, (handsL_x[15]-body_x[5])],   [15, (handsL_x[15]-body_x[2])],   [15, (handsL_x[15]-body_x[0])],   [15, (handsL_x[15]-body_x[8])],   [15, (handsL_x[15]-body_x[7])],   [15, (handsL_x[15]-body_x[10])],   [15, (handsL_x[15]-body_x[9])],
                    [14, (handsL_x[14]-body_x[5])],   [14, (handsL_x[14]-body_x[2])],   [14, (handsL_x[14]-body_x[0])],   [14, (handsL_x[14]-body_x[8])],   [14, (handsL_x[14]-body_x[7])],   [14, (handsL_x[14]-body_x[10])],   [14, (handsL_x[14]-body_x[9])],
                    [13, (handsL_x[13]-body_x[5])],   [13, (handsL_x[13]-body_x[2])],   [13, (handsL_x[13]-body_x[0])],   [13, (handsL_x[13]-body_x[8])],   [13, (handsL_x[13]-body_x[7])],   [13, (handsL_x[13]-body_x[10])],   [13, (handsL_x[13]-body_x[9])],
                #pinky
                    [20, (handsL_x[20]-body_x[5])],   [20, (handsL_x[20]-body_x[2])],   [20, (handsL_x[20]-body_x[0])],   [20, (handsL_x[20]-body_x[8])],   [20, (handsL_x[20]-body_x[7])],   [20, (handsL_x[20]-body_x[10])],   [20, (handsL_x[20]-body_x[9])],
                    [19, (handsL_x[19]-body_x[5])],   [19, (handsL_x[19]-body_x[2])],   [19, (handsL_x[19]-body_x[0])],   [19, (handsL_x[19]-body_x[8])],   [19, (handsL_x[19]-body_x[7])],   [19, (handsL_x[19]-body_x[10])],   [19, (handsL_x[19]-body_x[9])],
                    [18, (handsL_x[18]-body_x[5])],   [18, (handsL_x[18]-body_x[2])],   [18, (handsL_x[18]-body_x[0])],   [18, (handsL_x[18]-body_x[8])],   [18, (handsL_x[18]-body_x[7])],   [18, (handsL_x[18]-body_x[10])],   [18, (handsL_x[18]-body_x[9])],
                    [17, (handsL_x[17]-body_x[5])],   [17, (handsL_x[17]-body_x[2])],   [17, (handsL_x[17]-body_x[0])],   [17, (handsL_x[17]-body_x[8])],   [17, (handsL_x[17]-body_x[7])],   [17, (handsL_x[17]-body_x[10])],   [17, (handsL_x[17]-body_x[9])]
                ]
                self._points_body_face_relation_diffXLeft = [[x[1],x[0]] for x in self._points_body_face_relation_diffXLeft]
                self._points_body_face_relation_diffYLeft = [
                    #thumb 
                    [4, (handsL_y[4]-body_y[5])],   [4, (handsL_y[4]-body_y[2])],   [4, (handsL_y[4]-body_y[0])],   [4, (handsL_y[4]-body_y[8])],   [4, (handsL_y[4]-body_y[7])],   [4, (handsL_y[4]-body_y[10])],   [4, (handsL_y[4]-body_y[9])],
                    [3, (handsL_y[3]-body_y[5])],   [3, (handsL_y[3]-body_y[2])],   [3, (handsL_y[3]-body_y[0])],   [3, (handsL_y[3]-body_y[8])],   [3, (handsL_y[3]-body_y[7])],   [3, (handsL_y[3]-body_y[10])],   [3, (handsL_y[3]-body_y[9])],
                    [2, (handsL_y[2]-body_y[5])],   [2, (handsL_y[2]-body_y[2])],   [2, (handsL_y[2]-body_y[0])],   [2, (handsL_y[2]-body_y[8])],   [2, (handsL_y[2]-body_y[7])],   [2, (handsL_y[2]-body_y[10])],   [2, (handsL_y[2]-body_y[9])],
                    [1, (handsL_y[1]-body_y[5])],   [1, (handsL_y[1]-body_y[2])],   [1, (handsL_y[1]-body_y[0])],   [1, (handsL_y[1]-body_y[8])],   [1, (handsL_y[1]-body_y[7])],   [1, (handsL_y[1]-body_y[10])],   [1, (handsL_y[1]-body_y[9])],
                    #wirst
                    [0, (handsL_y[0]-body_y[5])],   [0, (handsL_y[0]-body_y[2])],   [0, (handsL_y[0]-body_y[0])],   [0, (handsL_y[0]-body_y[8])],   [0, (handsL_y[0]-body_y[7])],   [0, (handsL_y[0]-body_y[10])],   [0, (handsL_y[0]-body_y[9])],
                    #index
                    [8, (handsL_y[8]-body_y[5])],   [8, (handsL_y[8]-body_y[2])],   [8, (handsL_y[8]-body_y[0])],   [8, (handsL_y[8]-body_y[8])],   [8, (handsL_y[8]-body_y[7])],   [8, (handsL_y[8]-body_y[10])],   [8, (handsL_y[8]-body_y[9])],
                    [7, (handsL_y[7]-body_y[5])],   [7, (handsL_y[7]-body_y[2])],   [7, (handsL_y[7]-body_y[0])],   [7, (handsL_y[7]-body_y[8])],   [7, (handsL_y[7]-body_y[7])],   [7, (handsL_y[7]-body_y[10])],   [7, (handsL_y[7]-body_y[9])],
                    [6, (handsL_y[6]-body_y[5])],   [6, (handsL_y[6]-body_y[2])],   [6, (handsL_y[6]-body_y[0])],   [6, (handsL_y[6]-body_y[8])],   [6, (handsL_y[6]-body_y[7])],   [6, (handsL_y[6]-body_y[10])],   [6, (handsL_y[6]-body_y[9])],
                    [5, (handsL_y[5]-body_y[5])],   [5, (handsL_y[5]-body_y[2])],   [5, (handsL_y[5]-body_y[0])],   [5, (handsL_y[5]-body_y[8])],   [5, (handsL_y[5]-body_y[7])],   [5, (handsL_y[5]-body_y[10])],   [5, (handsL_y[5]-body_y[9])],
                    #middle
                    [12, (handsL_y[12]-body_y[5])],   [12, (handsL_y[12]-body_y[2])],   [12, (handsL_y[12]-body_y[0])],   [12, (handsL_y[12]-body_y[8])],   [12, (handsL_y[12]-body_y[7])],   [12, (handsL_y[12]-body_y[10])],   [12, (handsL_y[12]-body_y[9])],
                    [11, (handsL_y[11]-body_y[5])],   [11, (handsL_y[11]-body_y[2])],   [11, (handsL_y[11]-body_y[0])],   [11, (handsL_y[11]-body_y[8])],   [11, (handsL_y[11]-body_y[7])],   [11, (handsL_y[11]-body_y[10])],   [11, (handsL_y[11]-body_y[9])],
                    [10, (handsL_y[10]-body_y[5])],   [10, (handsL_y[10]-body_y[2])],   [10, (handsL_y[10]-body_y[0])],   [10, (handsL_y[10]-body_y[8])],   [10, (handsL_y[10]-body_y[7])],   [10, (handsL_y[10]-body_y[10])],   [10, (handsL_y[10]-body_y[9])],
                    [9, (handsL_y[9]-body_y[5])],     [9, (handsL_y[9]-body_y[2])],     [9, (handsL_y[9]-body_y[0])],     [9, (handsL_y[9]-body_y[8])],     [9, (handsL_y[9]-body_y[7])],     [9, (handsL_y[9]-body_y[10])],     [9, (handsL_y[9]-body_y[9])],
                    #ring
                    [16, (handsL_y[16]-body_y[5])],   [16, (handsL_y[16]-body_y[2])],   [16, (handsL_y[16]-body_y[0])],   [16, (handsL_y[16]-body_y[8])],   [16, (handsL_y[16]-body_y[7])],   [16, (handsL_y[16]-body_y[10])],   [16, (handsL_y[16]-body_y[9])],
                    [15, (handsL_y[15]-body_y[5])],   [15, (handsL_y[15]-body_y[2])],   [15, (handsL_y[15]-body_y[0])],   [15, (handsL_y[15]-body_y[8])],   [15, (handsL_y[15]-body_y[7])],   [15, (handsL_y[15]-body_y[10])],   [15, (handsL_y[15]-body_y[9])],
                    [14, (handsL_y[14]-body_y[5])],   [14, (handsL_y[14]-body_y[2])],   [14, (handsL_y[14]-body_y[0])],   [14, (handsL_y[14]-body_y[8])],   [14, (handsL_y[14]-body_y[7])],   [14, (handsL_y[14]-body_y[10])],   [14, (handsL_y[14]-body_y[9])],
                    [13, (handsL_y[13]-body_y[5])],   [13, (handsL_y[13]-body_y[2])],   [13, (handsL_y[13]-body_y[0])],   [13, (handsL_y[13]-body_y[8])],   [13, (handsL_y[13]-body_y[7])],   [13, (handsL_y[13]-body_y[10])],   [13, (handsL_y[13]-body_y[9])],
                #pinky
                    [20, (handsL_y[20]-body_y[5])],   [20, (handsL_y[20]-body_y[2])],   [20, (handsL_y[20]-body_y[0])],   [20, (handsL_y[20]-body_y[8])],   [20, (handsL_y[20]-body_y[7])],   [20, (handsL_y[20]-body_y[10])],   [20, (handsL_y[20]-body_y[9])],
                    [19, (handsL_y[19]-body_y[5])],   [19, (handsL_y[19]-body_y[2])],   [19, (handsL_y[19]-body_y[0])],   [19, (handsL_y[19]-body_y[8])],   [19, (handsL_y[19]-body_y[7])],   [19, (handsL_y[19]-body_y[10])],   [19, (handsL_y[19]-body_y[9])],
                    [18, (handsL_y[18]-body_y[5])],   [18, (handsL_y[18]-body_y[2])],   [18, (handsL_y[18]-body_y[0])],   [18, (handsL_y[18]-body_y[8])],   [18, (handsL_y[18]-body_y[7])],   [18, (handsL_y[18]-body_y[10])],   [18, (handsL_y[18]-body_y[9])],
                    [17, (handsL_y[17]-body_y[5])],   [17, (handsL_y[17]-body_y[2])],   [17, (handsL_y[17]-body_y[0])],   [17, (handsL_y[17]-body_y[8])],   [17, (handsL_y[17]-body_y[7])],   [17, (handsL_y[17]-body_y[10])],   [17, (handsL_y[17]-body_y[9])]
                ]
                self._points_body_face_relation_diffYLeft = [[x[1],x[0]] for x in self._points_body_face_relation_diffYLeft]
                self._points_body_face_relation_diffZLeft = [
                    #thumb 
                    [4, (handsL_z[4]-body_z[5])],   [4, (handsL_z[4]-body_z[2])],   [4, (handsL_z[4]-body_z[0])],   [4, (handsL_z[4]-body_z[8])],   [4, (handsL_z[4]-body_z[7])],   [4, (handsL_z[4]-body_z[10])],   [4, (handsL_z[4]-body_z[9])],
                    [3, (handsL_z[3]-body_z[5])],   [3, (handsL_z[3]-body_z[2])],   [3, (handsL_z[3]-body_z[0])],   [3, (handsL_z[3]-body_z[8])],   [3, (handsL_z[3]-body_z[7])],   [3, (handsL_z[3]-body_z[10])],   [3, (handsL_z[3]-body_z[9])],
                    [2, (handsL_z[2]-body_z[5])],   [2, (handsL_z[2]-body_z[2])],   [2, (handsL_z[2]-body_z[0])],   [2, (handsL_z[2]-body_z[8])],   [2, (handsL_z[2]-body_z[7])],   [2, (handsL_z[2]-body_z[10])],   [2, (handsL_z[2]-body_z[9])],
                    [1, (handsL_z[1]-body_z[5])],   [1, (handsL_z[1]-body_z[2])],   [1, (handsL_z[1]-body_z[0])],   [1, (handsL_z[1]-body_z[8])],   [1, (handsL_z[1]-body_z[7])],   [1, (handsL_z[1]-body_z[10])],   [1, (handsL_z[1]-body_z[9])],
                    #wirst
                    [0, (handsL_z[0]-body_z[5])],   [0, (handsL_z[0]-body_z[2])],   [0, (handsL_z[0]-body_z[0])],   [0, (handsL_z[0]-body_z[8])],   [0, (handsL_z[0]-body_z[7])],   [0, (handsL_z[0]-body_z[10])],   [0, (handsL_z[0]-body_z[9])],
                    #index
                    [8, (handsL_z[8]-body_z[5])],   [8, (handsL_z[8]-body_z[2])],   [8, (handsL_z[8]-body_z[0])],   [8, (handsL_z[8]-body_z[8])],   [8, (handsL_z[8]-body_z[7])],   [8, (handsL_z[8]-body_z[10])],   [8, (handsL_z[8]-body_z[9])],
                    [7, (handsL_z[7]-body_z[5])],   [7, (handsL_z[7]-body_z[2])],   [7, (handsL_z[7]-body_z[0])],   [7, (handsL_z[7]-body_z[8])],   [7, (handsL_z[7]-body_z[7])],   [7, (handsL_z[7]-body_z[10])],   [7, (handsL_z[7]-body_z[9])],
                    [6, (handsL_z[6]-body_z[5])],   [6, (handsL_z[6]-body_z[2])],   [6, (handsL_z[6]-body_z[0])],   [6, (handsL_z[6]-body_z[8])],   [6, (handsL_z[6]-body_z[7])],   [6, (handsL_z[6]-body_z[10])],   [6, (handsL_z[6]-body_z[9])],
                    [5, (handsL_z[5]-body_z[5])],   [5, (handsL_z[5]-body_z[2])],   [5, (handsL_z[5]-body_z[0])],   [5, (handsL_z[5]-body_z[8])],   [5, (handsL_z[5]-body_z[7])],   [5, (handsL_z[5]-body_z[10])],   [5, (handsL_z[5]-body_z[9])],
                    #middle
                    [12, (handsL_z[12]-body_z[5])],   [12, (handsL_z[12]-body_z[2])],   [12, (handsL_z[12]-body_z[0])],   [12, (handsL_z[12]-body_z[8])],   [12, (handsL_z[12]-body_z[7])],   [12, (handsL_z[12]-body_z[10])],   [12, (handsL_z[12]-body_z[9])],
                    [11, (handsL_z[11]-body_z[5])],   [11, (handsL_z[11]-body_z[2])],   [11, (handsL_z[11]-body_z[0])],   [11, (handsL_z[11]-body_z[8])],   [11, (handsL_z[11]-body_z[7])],   [11, (handsL_z[11]-body_z[10])],   [11, (handsL_z[11]-body_z[9])],
                    [10, (handsL_z[10]-body_z[5])],   [10, (handsL_z[10]-body_z[2])],   [10, (handsL_z[10]-body_z[0])],   [10, (handsL_z[10]-body_z[8])],   [10, (handsL_z[10]-body_z[7])],   [10, (handsL_z[10]-body_z[10])],   [10, (handsL_z[10]-body_z[9])],
                    [9, (handsL_z[9]-body_z[5])],     [9, (handsL_z[9]-body_z[2])],     [9, (handsL_z[9]-body_z[0])],     [9, (handsL_z[9]-body_z[8])],     [9, (handsL_z[9]-body_z[7])],     [9, (handsL_z[9]-body_z[10])],     [9, (handsL_z[9]-body_z[9])],
                    #ring
                    [16, (handsL_z[16]-body_z[5])],   [16, (handsL_z[16]-body_z[2])],   [16, (handsL_z[16]-body_z[0])],   [16, (handsL_z[16]-body_z[8])],   [16, (handsL_z[16]-body_z[7])],   [16, (handsL_z[16]-body_z[10])],   [16, (handsL_z[16]-body_z[9])],
                    [15, (handsL_z[15]-body_z[5])],   [15, (handsL_z[15]-body_z[2])],   [15, (handsL_z[15]-body_z[0])],   [15, (handsL_z[15]-body_z[8])],   [15, (handsL_z[15]-body_z[7])],   [15, (handsL_z[15]-body_z[10])],   [15, (handsL_z[15]-body_z[9])],
                    [14, (handsL_z[14]-body_z[5])],   [14, (handsL_z[14]-body_z[2])],   [14, (handsL_z[14]-body_z[0])],   [14, (handsL_z[14]-body_z[8])],   [14, (handsL_z[14]-body_z[7])],   [14, (handsL_z[14]-body_z[10])],   [14, (handsL_z[14]-body_z[9])],
                    [13, (handsL_z[13]-body_z[5])],   [13, (handsL_z[13]-body_z[2])],   [13, (handsL_z[13]-body_z[0])],   [13, (handsL_z[13]-body_z[8])],   [13, (handsL_z[13]-body_z[7])],   [13, (handsL_z[13]-body_z[10])],   [13, (handsL_z[13]-body_z[9])],
                #pinky
                    [20, (handsL_z[20]-body_z[5])],   [20, (handsL_z[20]-body_z[2])],   [20, (handsL_z[20]-body_z[0])],   [20, (handsL_z[20]-body_z[8])],   [20, (handsL_z[20]-body_z[7])],   [20, (handsL_z[20]-body_z[10])],   [20, (handsL_z[20]-body_z[9])],
                    [19, (handsL_z[19]-body_z[5])],   [19, (handsL_z[19]-body_z[2])],   [19, (handsL_z[19]-body_z[0])],   [19, (handsL_z[19]-body_z[8])],   [19, (handsL_z[19]-body_z[7])],   [19, (handsL_z[19]-body_z[10])],   [19, (handsL_z[19]-body_z[9])],
                    [18, (handsL_z[18]-body_z[5])],   [18, (handsL_z[18]-body_z[2])],   [18, (handsL_z[18]-body_z[0])],   [18, (handsL_z[18]-body_z[8])],   [18, (handsL_z[18]-body_z[7])],   [18, (handsL_z[18]-body_z[10])],   [18, (handsL_z[18]-body_z[9])],
                    [17, (handsL_z[17]-body_z[5])],   [17, (handsL_z[17]-body_z[2])],   [17, (handsL_z[17]-body_z[0])],   [17, (handsL_z[17]-body_z[8])],   [17, (handsL_z[17]-body_z[7])],   [17, (handsL_z[17]-body_z[10])],   [17, (handsL_z[17]-body_z[9])]
                ]
                self._points_body_face_relation_diffZLeft = [[x[1],x[0]] for x in self._points_body_face_relation_diffZLeft]
            
            ## Right Hand
            if len(self._hand_Right)>0:
                self._points_body_face_relation_diffXRight = [
                    #thumb 
                    [4, (handsR_x[4]-body_x[5])],   [4, (handsR_x[4]-body_x[2])],   [4, (handsR_x[4]-body_x[0])],   [4, (handsR_x[4]-body_x[8])],   [4, (handsR_x[4]-body_x[7])],   [4, (handsR_x[4]-body_x[10])],   [4, (handsR_x[4]-body_x[9])],
                    [3, (handsR_x[3]-body_x[5])],   [3, (handsR_x[3]-body_x[2])],   [3, (handsR_x[3]-body_x[0])],   [3, (handsR_x[3]-body_x[8])],   [3, (handsR_x[3]-body_x[7])],   [3, (handsR_x[3]-body_x[10])],   [3, (handsR_x[3]-body_x[9])],
                    [2, (handsR_x[2]-body_x[5])],   [2, (handsR_x[2]-body_x[2])],   [2, (handsR_x[2]-body_x[0])],   [2, (handsR_x[2]-body_x[8])],   [2, (handsR_x[2]-body_x[7])],   [2, (handsR_x[2]-body_x[10])],   [2, (handsR_x[2]-body_x[9])],
                    [1, (handsR_x[1]-body_x[5])],   [1, (handsR_x[1]-body_x[2])],   [1, (handsR_x[1]-body_x[0])],   [1, (handsR_x[1]-body_x[8])],   [1, (handsR_x[1]-body_x[7])],   [1, (handsR_x[1]-body_x[10])],   [1, (handsR_x[1]-body_x[9])],
                    #wirst
                    [0, (handsR_x[0]-body_x[5])],   [0, (handsR_x[0]-body_x[2])],   [0, (handsR_x[0]-body_x[0])],   [0, (handsR_x[0]-body_x[8])],   [0, (handsR_x[0]-body_x[7])],   [0, (handsR_x[0]-body_x[10])],   [0, (handsR_x[0]-body_x[9])],
                    #index
                    [8, (handsR_x[8]-body_x[5])],   [8, (handsR_x[8]-body_x[2])],   [8, (handsR_x[8]-body_x[0])],   [8, (handsR_x[8]-body_x[8])],   [8, (handsR_x[8]-body_x[7])],   [8, (handsR_x[8]-body_x[10])],   [8, (handsR_x[8]-body_x[9])],
                    [7, (handsR_x[7]-body_x[5])],   [7, (handsR_x[7]-body_x[2])],   [7, (handsR_x[7]-body_x[0])],   [7, (handsR_x[7]-body_x[8])],   [7, (handsR_x[7]-body_x[7])],   [7, (handsR_x[7]-body_x[10])],   [7, (handsR_x[7]-body_x[9])],
                    [6, (handsR_x[6]-body_x[5])],   [6, (handsR_x[6]-body_x[2])],   [6, (handsR_x[6]-body_x[0])],   [6, (handsR_x[6]-body_x[8])],   [6, (handsR_x[6]-body_x[7])],   [6, (handsR_x[6]-body_x[10])],   [6, (handsR_x[6]-body_x[9])],
                    [5, (handsR_x[5]-body_x[5])],   [5, (handsR_x[5]-body_x[2])],   [5, (handsR_x[5]-body_x[0])],   [5, (handsR_x[5]-body_x[8])],   [5, (handsR_x[5]-body_x[7])],   [5, (handsR_x[5]-body_x[10])],   [5, (handsR_x[5]-body_x[9])],
                    #middle
                    [12, (handsR_x[12]-body_x[5])],   [12, (handsR_x[12]-body_x[2])],   [12, (handsR_x[12]-body_x[0])],   [12, (handsR_x[12]-body_x[8])],   [12, (handsR_x[12]-body_x[7])],   [12, (handsR_x[12]-body_x[10])],   [12, (handsR_x[12]-body_x[9])],
                    [11, (handsR_x[11]-body_x[5])],   [11, (handsR_x[11]-body_x[2])],   [11, (handsR_x[11]-body_x[0])],   [11, (handsR_x[11]-body_x[8])],   [11, (handsR_x[11]-body_x[7])],   [11, (handsR_x[11]-body_x[10])],   [11, (handsR_x[11]-body_x[9])],
                    [10, (handsR_x[10]-body_x[5])],   [10, (handsR_x[10]-body_x[2])],   [10, (handsR_x[10]-body_x[0])],   [10, (handsR_x[10]-body_x[8])],   [10, (handsR_x[10]-body_x[7])],   [10, (handsR_x[10]-body_x[10])],   [10, (handsR_x[10]-body_x[9])],
                    [9,  (handsR_x[9]-body_x[5])],    [9, (handsR_x[9]-body_x[2])],     [9,  (handsR_x[9]-body_x[0])],    [9,  (handsR_x[9]-body_x[8])],    [9, (handsR_x[9]-body_x[7])],     [9,  (handsR_x[9]-body_x[10])],    [9,  (handsR_x[9]-body_x[9])],
                    #ring
                    [16, (handsR_x[16]-body_x[5])],   [16, (handsR_x[16]-body_x[2])],   [16, (handsR_x[16]-body_x[0])],   [16, (handsR_x[16]-body_x[8])],   [16, (handsR_x[16]-body_x[7])],   [16, (handsR_x[16]-body_x[10])],   [16, (handsR_x[16]-body_x[9])],
                    [15, (handsR_x[15]-body_x[5])],   [15, (handsR_x[15]-body_x[2])],   [15, (handsR_x[15]-body_x[0])],   [15, (handsR_x[15]-body_x[8])],   [15, (handsR_x[15]-body_x[7])],   [15, (handsR_x[15]-body_x[10])],   [15, (handsR_x[15]-body_x[9])],
                    [14, (handsR_x[14]-body_x[5])],   [14, (handsR_x[14]-body_x[2])],   [14, (handsR_x[14]-body_x[0])],   [14, (handsR_x[14]-body_x[8])],   [14, (handsR_x[14]-body_x[7])],   [14, (handsR_x[14]-body_x[10])],   [14, (handsR_x[14]-body_x[9])],
                    [13, (handsR_x[13]-body_x[5])],   [13, (handsR_x[13]-body_x[2])],   [13, (handsR_x[13]-body_x[0])],   [13, (handsR_x[13]-body_x[8])],   [13, (handsR_x[13]-body_x[7])],   [13, (handsR_x[13]-body_x[10])],   [13, (handsR_x[13]-body_x[9])],
                #pinky
                    [20, (handsR_x[20]-body_x[5])],   [20, (handsR_x[20]-body_x[2])],   [20, (handsR_x[20]-body_x[0])],   [20, (handsR_x[20]-body_x[8])],   [20, (handsR_x[20]-body_x[7])],   [20, (handsR_x[20]-body_x[10])],   [20, (handsR_x[20]-body_x[9])],
                    [19, (handsR_x[19]-body_x[5])],   [19, (handsR_x[19]-body_x[2])],   [19, (handsR_x[19]-body_x[0])],   [19, (handsR_x[19]-body_x[8])],   [19, (handsR_x[19]-body_x[7])],   [19, (handsR_x[19]-body_x[10])],   [19, (handsR_x[19]-body_x[9])],
                    [18, (handsR_x[18]-body_x[5])],   [18, (handsR_x[18]-body_x[2])],   [18, (handsR_x[18]-body_x[0])],   [18, (handsR_x[18]-body_x[8])],   [18, (handsR_x[18]-body_x[7])],   [18, (handsR_x[18]-body_x[10])],   [18, (handsR_x[18]-body_x[9])],
                    [17, (handsR_x[17]-body_x[5])],   [17, (handsR_x[17]-body_x[2])],   [17, (handsR_x[17]-body_x[0])],   [17, (handsR_x[17]-body_x[8])],   [17, (handsR_x[17]-body_x[7])],   [17, (handsR_x[17]-body_x[10])],   [17, (handsR_x[17]-body_x[9])]
                ]
                self._points_body_face_relation_diffXRight = [[x[1],x[0]] for x in self._points_body_face_relation_diffXRight]
                self._points_body_face_relation_diffYRight = [
                    #thumb 
                    [4, (handsR_y[4]-body_y[5])],   [4, (handsR_y[4]-body_y[2])],   [4, (handsR_y[4]-body_y[0])],   [4, (handsR_y[4]-body_y[8])],   [4, (handsR_y[4]-body_y[7])],   [4, (handsR_y[4]-body_y[10])],   [4, (handsR_y[4]-body_y[9])],
                    [3, (handsR_y[3]-body_y[5])],   [3, (handsR_y[3]-body_y[2])],   [3, (handsR_y[3]-body_y[0])],   [3, (handsR_y[3]-body_y[8])],   [3, (handsR_y[3]-body_y[7])],   [3, (handsR_y[3]-body_y[10])],   [3, (handsR_y[3]-body_y[9])],
                    [2, (handsR_y[2]-body_y[5])],   [2, (handsR_y[2]-body_y[2])],   [2, (handsR_y[2]-body_y[0])],   [2, (handsR_y[2]-body_y[8])],   [2, (handsR_y[2]-body_y[7])],   [2, (handsR_y[2]-body_y[10])],   [2, (handsR_y[2]-body_y[9])],
                    [1, (handsR_y[1]-body_y[5])],   [1, (handsR_y[1]-body_y[2])],   [1, (handsR_y[1]-body_y[0])],   [1, (handsR_y[1]-body_y[8])],   [1, (handsR_y[1]-body_y[7])],   [1, (handsR_y[1]-body_y[10])],   [1, (handsR_y[1]-body_y[9])],
                    #wirst
                    [0, (handsR_y[0]-body_y[5])],   [0, (handsR_y[0]-body_y[2])],   [0, (handsR_y[0]-body_y[0])],   [0, (handsR_y[0]-body_y[8])],   [0, (handsR_y[0]-body_y[7])],   [0, (handsR_y[0]-body_y[10])],   [0, (handsR_y[0]-body_y[9])],
                    #index
                    [8, (handsR_y[8]-body_y[5])],   [8, (handsR_y[8]-body_y[2])],   [8, (handsR_y[8]-body_y[0])],   [8, (handsR_y[8]-body_y[8])],   [8, (handsR_y[8]-body_y[7])],   [8, (handsR_y[8]-body_y[10])],   [8, (handsR_y[8]-body_y[9])],
                    [7, (handsR_y[7]-body_y[5])],   [7, (handsR_y[7]-body_y[2])],   [7, (handsR_y[7]-body_y[0])],   [7, (handsR_y[7]-body_y[8])],   [7, (handsR_y[7]-body_y[7])],   [7, (handsR_y[7]-body_y[10])],   [7, (handsR_y[7]-body_y[9])],
                    [6, (handsR_y[6]-body_y[5])],   [6, (handsR_y[6]-body_y[2])],   [6, (handsR_y[6]-body_y[0])],   [6, (handsR_y[6]-body_y[8])],   [6, (handsR_y[6]-body_y[7])],   [6, (handsR_y[6]-body_y[10])],   [6, (handsR_y[6]-body_y[9])],
                    [5, (handsR_y[5]-body_y[5])],   [5, (handsR_y[5]-body_y[2])],   [5, (handsR_y[5]-body_y[0])],   [5, (handsR_y[5]-body_y[8])],   [5, (handsR_y[5]-body_y[7])],   [5, (handsR_y[5]-body_y[10])],   [5, (handsR_y[5]-body_y[9])],
                    #middle
                    [12, (handsR_y[12]-body_y[5])],   [12, (handsR_y[12]-body_y[2])],   [12, (handsR_y[12]-body_y[0])],   [12, (handsR_y[12]-body_y[8])],   [12, (handsR_y[12]-body_y[7])],   [12, (handsR_y[12]-body_y[10])],   [12, (handsR_y[12]-body_y[9])],
                    [11, (handsR_y[11]-body_y[5])],   [11, (handsR_y[11]-body_y[2])],   [11, (handsR_y[11]-body_y[0])],   [11, (handsR_y[11]-body_y[8])],   [11, (handsR_y[11]-body_y[7])],   [11, (handsR_y[11]-body_y[10])],   [11, (handsR_y[11]-body_y[9])],
                    [10, (handsR_y[10]-body_y[5])],   [10, (handsR_y[10]-body_y[2])],   [10, (handsR_y[10]-body_y[0])],   [10, (handsR_y[10]-body_y[8])],   [10, (handsR_y[10]-body_y[7])],   [10, (handsR_y[10]-body_y[10])],   [10, (handsR_y[10]-body_y[9])],
                    [9, (handsR_y[9]-body_y[5])],     [9, (handsR_y[9]-body_y[2])],     [9, (handsR_y[9]-body_y[0])],     [9, (handsR_y[9]-body_y[8])],     [9, (handsR_y[9]-body_y[7])],     [9, (handsR_y[9]-body_y[10])],     [9, (handsR_y[9]-body_y[9])],
                    #ring
                    [16, (handsR_y[16]-body_y[5])],   [16, (handsR_y[16]-body_y[2])],   [16, (handsR_y[16]-body_y[0])],   [16, (handsR_y[16]-body_y[8])],   [16, (handsR_y[16]-body_y[7])],   [16, (handsR_y[16]-body_y[10])],   [16, (handsR_y[16]-body_y[9])],
                    [15, (handsR_y[15]-body_y[5])],   [15, (handsR_y[15]-body_y[2])],   [15, (handsR_y[15]-body_y[0])],   [15, (handsR_y[15]-body_y[8])],   [15, (handsR_y[15]-body_y[7])],   [15, (handsR_y[15]-body_y[10])],   [15, (handsR_y[15]-body_y[9])],
                    [14, (handsR_y[14]-body_y[5])],   [14, (handsR_y[14]-body_y[2])],   [14, (handsR_y[14]-body_y[0])],   [14, (handsR_y[14]-body_y[8])],   [14, (handsR_y[14]-body_y[7])],   [14, (handsR_y[14]-body_y[10])],   [14, (handsR_y[14]-body_y[9])],
                    [13, (handsR_y[13]-body_y[5])],   [13, (handsR_y[13]-body_y[2])],   [13, (handsR_y[13]-body_y[0])],   [13, (handsR_y[13]-body_y[8])],   [13, (handsR_y[13]-body_y[7])],   [13, (handsR_y[13]-body_y[10])],   [13, (handsR_y[13]-body_y[9])],
                #pinky
                    [20, (handsR_y[20]-body_y[5])],   [20, (handsR_y[20]-body_y[2])],   [20, (handsR_y[20]-body_y[0])],   [20, (handsR_y[20]-body_y[8])],   [20, (handsR_y[20]-body_y[7])],   [20, (handsR_y[20]-body_y[10])],   [20, (handsR_y[20]-body_y[9])],
                    [19, (handsR_y[19]-body_y[5])],   [19, (handsR_y[19]-body_y[2])],   [19, (handsR_y[19]-body_y[0])],   [19, (handsR_y[19]-body_y[8])],   [19, (handsR_y[19]-body_y[7])],   [19, (handsR_y[19]-body_y[10])],   [19, (handsR_y[19]-body_y[9])],
                    [18, (handsR_y[18]-body_y[5])],   [18, (handsR_y[18]-body_y[2])],   [18, (handsR_y[18]-body_y[0])],   [18, (handsR_y[18]-body_y[8])],   [18, (handsR_y[18]-body_y[7])],   [18, (handsR_y[18]-body_y[10])],   [18, (handsR_y[18]-body_y[9])],
                    [17, (handsR_y[17]-body_y[5])],   [17, (handsR_y[17]-body_y[2])],   [17, (handsR_y[17]-body_y[0])],   [17, (handsR_y[17]-body_y[8])],   [17, (handsR_y[17]-body_y[7])],   [17, (handsR_y[17]-body_y[10])],   [17, (handsR_y[17]-body_y[9])]
                ]
                self._points_body_face_relation_diffYRight = [[x[1],x[0]] for x in self._points_body_face_relation_diffYRight]
                self._points_body_face_relation_diffZRight = [
                    #thumb 
                    [4, (handsR_z[4]-body_z[5])],   [4, (handsR_z[4]-body_z[2])],   [4, (handsR_z[4]-body_z[0])],   [4, (handsR_z[4]-body_z[8])],   [4, (handsR_z[4]-body_z[7])],   [4, (handsR_z[4]-body_z[10])],   [4, (handsR_z[4]-body_z[9])],
                    [3, (handsR_z[3]-body_z[5])],   [3, (handsR_z[3]-body_z[2])],   [3, (handsR_z[3]-body_z[0])],   [3, (handsR_z[3]-body_z[8])],   [3, (handsR_z[3]-body_z[7])],   [3, (handsR_z[3]-body_z[10])],   [3, (handsR_z[3]-body_z[9])],
                    [2, (handsR_z[2]-body_z[5])],   [2, (handsR_z[2]-body_z[2])],   [2, (handsR_z[2]-body_z[0])],   [2, (handsR_z[2]-body_z[8])],   [2, (handsR_z[2]-body_z[7])],   [2, (handsR_z[2]-body_z[10])],   [2, (handsR_z[2]-body_z[9])],
                    [1, (handsR_z[1]-body_z[5])],   [1, (handsR_z[1]-body_z[2])],   [1, (handsR_z[1]-body_z[0])],   [1, (handsR_z[1]-body_z[8])],   [1, (handsR_z[1]-body_z[7])],   [1, (handsR_z[1]-body_z[10])],   [1, (handsR_z[1]-body_z[9])],
                    #wirst
                    [0, (handsR_z[0]-body_z[5])],   [0, (handsR_z[0]-body_z[2])],   [0, (handsR_z[0]-body_z[0])],   [0, (handsR_z[0]-body_z[8])],   [0, (handsR_z[0]-body_z[7])],   [0, (handsR_z[0]-body_z[10])],   [0, (handsR_z[0]-body_z[9])],
                    #index
                    [8, (handsR_z[8]-body_z[5])],   [8, (handsR_z[8]-body_z[2])],   [8, (handsR_z[8]-body_z[0])],   [8, (handsR_z[8]-body_z[8])],   [8, (handsR_z[8]-body_z[7])],   [8, (handsR_z[8]-body_z[10])],   [8, (handsR_z[8]-body_z[9])],
                    [7, (handsR_z[7]-body_z[5])],   [7, (handsR_z[7]-body_z[2])],   [7, (handsR_z[7]-body_z[0])],   [7, (handsR_z[7]-body_z[8])],   [7, (handsR_z[7]-body_z[7])],   [7, (handsR_z[7]-body_z[10])],   [7, (handsR_z[7]-body_z[9])],
                    [6, (handsR_z[6]-body_z[5])],   [6, (handsR_z[6]-body_z[2])],   [6, (handsR_z[6]-body_z[0])],   [6, (handsR_z[6]-body_z[8])],   [6, (handsR_z[6]-body_z[7])],   [6, (handsR_z[6]-body_z[10])],   [6, (handsR_z[6]-body_z[9])],
                    [5, (handsR_z[5]-body_z[5])],   [5, (handsR_z[5]-body_z[2])],   [5, (handsR_z[5]-body_z[0])],   [5, (handsR_z[5]-body_z[8])],   [5, (handsR_z[5]-body_z[7])],   [5, (handsR_z[5]-body_z[10])],   [5, (handsR_z[5]-body_z[9])],
                    #middle
                    [12, (handsR_z[12]-body_z[5])],   [12, (handsR_z[12]-body_z[2])],   [12, (handsR_z[12]-body_z[0])],   [12, (handsR_z[12]-body_z[8])],   [12, (handsR_z[12]-body_z[7])],   [12, (handsR_z[12]-body_z[10])],   [12, (handsR_z[12]-body_z[9])],
                    [11, (handsR_z[11]-body_z[5])],   [11, (handsR_z[11]-body_z[2])],   [11, (handsR_z[11]-body_z[0])],   [11, (handsR_z[11]-body_z[8])],   [11, (handsR_z[11]-body_z[7])],   [11, (handsR_z[11]-body_z[10])],   [11, (handsR_z[11]-body_z[9])],
                    [10, (handsR_z[10]-body_z[5])],   [10, (handsR_z[10]-body_z[2])],   [10, (handsR_z[10]-body_z[0])],   [10, (handsR_z[10]-body_z[8])],   [10, (handsR_z[10]-body_z[7])],   [10, (handsR_z[10]-body_z[10])],   [10, (handsR_z[10]-body_z[9])],
                    [9, (handsR_z[9]-body_z[5])],     [9, (handsR_z[9]-body_z[2])],     [9, (handsR_z[9]-body_z[0])],     [9, (handsR_z[9]-body_z[8])],     [9, (handsR_z[9]-body_z[7])],     [9, (handsR_z[9]-body_z[10])],     [9, (handsR_z[9]-body_z[9])],
                    #ring
                    [16, (handsR_z[16]-body_z[5])],   [16, (handsR_z[16]-body_z[2])],   [16, (handsR_z[16]-body_z[0])],   [16, (handsR_z[16]-body_z[8])],   [16, (handsR_z[16]-body_z[7])],   [16, (handsR_z[16]-body_z[10])],   [16, (handsR_z[16]-body_z[9])],
                    [15, (handsR_z[15]-body_z[5])],   [15, (handsR_z[15]-body_z[2])],   [15, (handsR_z[15]-body_z[0])],   [15, (handsR_z[15]-body_z[8])],   [15, (handsR_z[15]-body_z[7])],   [15, (handsR_z[15]-body_z[10])],   [15, (handsR_z[15]-body_z[9])],
                    [14, (handsR_z[14]-body_z[5])],   [14, (handsR_z[14]-body_z[2])],   [14, (handsR_z[14]-body_z[0])],   [14, (handsR_z[14]-body_z[8])],   [14, (handsR_z[14]-body_z[7])],   [14, (handsR_z[14]-body_z[10])],   [14, (handsR_z[14]-body_z[9])],
                    [13, (handsR_z[13]-body_z[5])],   [13, (handsR_z[13]-body_z[2])],   [13, (handsR_z[13]-body_z[0])],   [13, (handsR_z[13]-body_z[8])],   [13, (handsR_z[13]-body_z[7])],   [13, (handsR_z[13]-body_z[10])],   [13, (handsR_z[13]-body_z[9])],
                #pinky
                    [20, (handsR_z[20]-body_z[5])],   [20, (handsR_z[20]-body_z[2])],   [20, (handsR_z[20]-body_z[0])],   [20, (handsR_z[20]-body_z[8])],   [20, (handsR_z[20]-body_z[7])],   [20, (handsR_z[20]-body_z[10])],   [20, (handsR_z[20]-body_z[9])],
                    [19, (handsR_z[19]-body_z[5])],   [19, (handsR_z[19]-body_z[2])],   [19, (handsR_z[19]-body_z[0])],   [19, (handsR_z[19]-body_z[8])],   [19, (handsR_z[19]-body_z[7])],   [19, (handsR_z[19]-body_z[10])],   [19, (handsR_z[19]-body_z[9])],
                    [18, (handsR_z[18]-body_z[5])],   [18, (handsR_z[18]-body_z[2])],   [18, (handsR_z[18]-body_z[0])],   [18, (handsR_z[18]-body_z[8])],   [18, (handsR_z[18]-body_z[7])],   [18, (handsR_z[18]-body_z[10])],   [18, (handsR_z[18]-body_z[9])],
                    [17, (handsR_z[17]-body_z[5])],   [17, (handsR_z[17]-body_z[2])],   [17, (handsR_z[17]-body_z[0])],   [17, (handsR_z[17]-body_z[8])],   [17, (handsR_z[17]-body_z[7])],   [17, (handsR_z[17]-body_z[10])],   [17, (handsR_z[17]-body_z[9])]
                ]
                self._points_body_face_relation_diffZRight = [[x[1],x[0]] for x in self._points_body_face_relation_diffZRight]

## model static - one movement core

class Model(Imodel):

    def __init__(self, hands_relation=False, face_relation=False, body_relation=False, move_relation=False, label="", ModelsEvaluation= []):
        self._body_relation = body_relation
        self._face_relation = face_relation
        self._hand_relation = hands_relation
        self._move_relation = move_relation
        self._label = label
        self._model_evaluation = ModelsEvaluation
        self._confidence = 0.55
        self._confidence_results = 0

    def get_result(self, data):
        try:
            if len(data)>0:
                results = False
                self._confidence_results = 0
                ##evaluation_model
                if self._face_relation == False and self._body_relation == False:
                    results = self.__model_hand(data)          

                elif self._face_relation:
                    results = self.__model_face_relation(data)

                elif self._body_relation:

                    results_hand = self.__model_hand(data)
                    confidence1 = self._confidence_results
                    self._confidence_results = 0

                    results_body = self.__model_body_relation(data)
                    confidence2 = self._confidence_results
                    results = results_hand and results_body

                    self._confidence_results = (confidence1+confidence2+0.2)/2
                
                ##results_recog
                return  {
                    "hand_value": self._label,
                    "rule_match": results,
                    "message": "Resultado obtenido exitosamente",
                    "confidence": self._confidence_results
                }
            else:
                return  {
                    "hand_value": self._label,
                    "rule_match": False,
                    "message": "",
                    "confidence": 0
                }
        except Exception as e:
            print("Error Ocurrido [Model Exec], Mensaje: {0}".format(str(e)))
            return  {
                "hand_value": self._label,
                "rule_match": False,
                "message": str(e),
                "confidence": 0
            }

    def __model_face_relation(self, data_value=[]):
        """
            Evalua los puntos de interseccion entre donde se consideran los puntos principales de la cara
            ojos, boca, nariz
        """
        if len(self._model_evaluation) < 1: return False
        value = True
        for val in data_value:

            value = True

            _results_hand_Right = []
            _results_hand_Left = []
            _results_face_Right = []
            _results_face_Left = []

            __value_data = HandModel(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=self._face_relation, body_relation=self._body_relation)
            data_models = __value_data.get_model()
        
            if self._hand_relation and (len(val['model_hand_Left'])>0 and len(val['model_hand_Right'])>0):
                ##### Evaluation Hands
                #0 Right X
                    df = pd.DataFrame([data_models[0]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[0]) < 1: break;
                        Kera_Model = self._model_evaluation[0][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Right.append(sum(results)/len(results))
                
                #1 Right Y
                    df = pd.DataFrame([data_models[1]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[1]) < 1: break;
                        Kera_Model = self._model_evaluation[1][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Right.append(sum(results)/len(results))
                
                #2 Right Z
                    df = pd.DataFrame([data_models[2]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[2]) < 1: break;
                        Kera_Model = self._model_evaluation[2][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Right.append(sum(results)/len(results))
                    
                #0 Left X
                    df = pd.DataFrame([data_models[3]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[3]) < 1: break;
                        Kera_Model = self._model_evaluation[3][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Left.append(sum(results)/len(results))
                
                #1 Left Y
                    df = pd.DataFrame([data_models[4]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[4]) < 1: break;
                        Kera_Model = self._model_evaluation[4][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Left.append(sum(results)/len(results))

                #2 Left Z
                    df = pd.DataFrame([data_models[5]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[5]) < 1: break;
                        Kera_Model = self._model_evaluation[5][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Left.append(sum(results)/len(results))

                    
                ##### Evaluation Face
                #0 Right X - Face
                    df = pd.DataFrame([data_models[18]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[6]) < 1: break;
                        Kera_Model = self._model_evaluation[6][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_face_Right.append(sum(results)/len(results))
                
                #1 Right Y - Face
                    df = pd.DataFrame([data_models[19]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[7]) < 1: break;
                        Kera_Model = self._model_evaluation[7][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_face_Right.append(sum(results)/len(results))
                
                #2 Right Z - Face
                    df = pd.DataFrame([data_models[20]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[8]) < 1: break;
                        Kera_Model = self._model_evaluation[8][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_face_Right.append(sum(results)/len(results))
                    
                #0 Left X - Face
                    df = pd.DataFrame([data_models[21]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[9]) < 1: break;
                        Kera_Model = self._model_evaluation[9][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_face_Left.append(sum(results)/len(results))
                
                #1 Left Y - Face
                    df = pd.DataFrame([data_models[22]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[10]) < 1: break;
                        Kera_Model = self._model_evaluation[10][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_face_Left.append(sum(results)/len(results))

                #2 Left Z - Face
                    df = pd.DataFrame([data_models[23]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[11]) < 1: break;
                        Kera_Model = self._model_evaluation[11][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_face_Left.append(sum(results)/len(results))
            elif not self._hand_relation and not (len(val['model_hand_Right'])>0 and len(val['model_hand_Left'])>0):
                if (len(val['model_hand_Right'])>0):
                    ##### Evaluation Hands
                    #0 Right X
                        df = pd.DataFrame([data_models[0]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[0]) < 1: break;
                            Kera_Model = self._model_evaluation[0][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_hand_Right.append(sum(results)/len(results))
                    
                    #1 Right Y
                        df = pd.DataFrame([data_models[1]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[1]) < 1: break;
                            Kera_Model = self._model_evaluation[1][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_hand_Right.append(sum(results)/len(results))
                    
                    #2 Right Z
                        df = pd.DataFrame([data_models[2]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[2]) < 1: break;
                            Kera_Model = self._model_evaluation[2][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_hand_Right.append(sum(results)/len(results))
                        
                                    
                    ##### Evaluation Face
                    #0 Right X - Face
                        df = pd.DataFrame([data_models[18]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[3]) < 1: break;
                            Kera_Model = self._model_evaluation[3][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_face_Right.append(sum(results)/len(results))
                    
                    #1 Right Y - Face
                        df = pd.DataFrame([data_models[19]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[4]) < 1: break;
                            Kera_Model = self._model_evaluation[4][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_face_Right.append(sum(results)/len(results))
                    
                    #2 Right Z - Face
                        df = pd.DataFrame([data_models[20]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[5]) < 1: break;
                            Kera_Model = self._model_evaluation[5][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_face_Right.append(sum(results)/len(results))          
                elif (len(val['model_hand_Left'])>0):
                    ##### Evaluation Hands
                    
                    #0 Left X
                        df = pd.DataFrame([data_models[3]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[0]) < 1: break;
                            Kera_Model = self._model_evaluation[0][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_hand_Left.append(sum(results)/len(results))
                    
                    #1 Left Y
                        df = pd.DataFrame([data_models[4]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[1]) < 1: break;
                            Kera_Model = self._model_evaluation[1][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_hand_Left.append(sum(results)/len(results))

                    #2 Left Z
                        df = pd.DataFrame([data_models[5]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[2]) < 1: break;
                            Kera_Model = self._model_evaluation[2][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_hand_Left.append(sum(results)/len(results))

                        
                    ##### Evaluation Face                
                    #0 Left X - Face
                        df = pd.DataFrame([data_models[21]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[3]) < 1: break;
                            Kera_Model = self._model_evaluation[3][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_face_Left.append(sum(results)/len(results))
                    
                    #1 Left Y - Face
                        df = pd.DataFrame([data_models[22]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[4]) < 1: break;
                            Kera_Model = self._model_evaluation[4][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_face_Left.append(sum(results)/len(results))

                    #2 Left Z - Face
                        df = pd.DataFrame([data_models[23]])
                        results = []
                        for i in range(len(df.columns)):
                            data_Predict = np.array(df[i].values.tolist())
                            if len(self._model_evaluation[5]) < 1: break;
                            Kera_Model = self._model_evaluation[5][i]
                            y_pred = Kera_Model.predict(data_Predict)
                            results.append(y_pred[0])
                        if len(results)>0:
                            _results_face_Left.append(sum(results)/len(results))    

            #### Evaluation results
            results_hand = []
            results_face = []
            results = []
            confidence = []

            if self._hand_relation:
                results_tmpRight = ([x >= (self._confidence-0.15) for x in _results_hand_Right])
                results_tmpLeft  = ([x >= (self._confidence-0.15) for x in _results_hand_Left])
                results_hand = results_tmpRight + results_tmpLeft
                confidence = _results_hand_Right + _results_hand_Left
            elif not self._hand_relation:
                if len(_results_hand_Right) == 3:
                    results_hand = ([x >= self._confidence for x in _results_hand_Right])
                    confidence = _results_hand_Right
                elif len(_results_hand_Left) == 3:
                    results_hand = ([x >= self._confidence for x in _results_hand_Left])
                    confidence = _results_hand_Left

            if len(_results_face_Right) == 3:
                results_face = ([x >= (self._confidence-0.15) for x in _results_face_Right])
                confidence = confidence + _results_face_Right
            elif len(_results_face_Left) == 3:
                results_face = ([x >= (self._confidence-0.15) for x in _results_face_Left])
                confidence = confidence + _results_face_Left

            if len(confidence)>0:
                self._confidence_results = sum(confidence)/len(confidence)
                    
            results = results_face
            for values in results:
                a1 = np.array(values)
                value = value and (a1 == True).all()

            results = results_hand
            for values in results:
                a1 = np.array(values)
                value = value and (a1 == True).all()

            if confidence == 0:
                value = False

        return value

    def __model_hand(self, data_value=[]):
        """
            Evalua los puntos de interseccion de las manos especificas, para reconocer unicamente movimiento de mano
        """

        if len(self._model_evaluation) < 1: return False
        value = False
        for val in data_value:
            value = True

            _results_hand_Right = []
            _results_hand_Left = []

            __value_data = HandModel(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=self._face_relation, body_relation=self._body_relation)
            data_models = __value_data.get_model()
        
            ##### Evaluation Hands
            if self._hand_relation and (len(val['model_hand_Left'])>0 and len(val['model_hand_Right'])>0):
                #0 Right X
                df = pd.DataFrame([data_models[0]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[0]) < 1: break;
                    Kera_Model = self._model_evaluation[0][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_hand_Right.append(sum(results)/len(results))
            
                #1 Right Y
                df = pd.DataFrame([data_models[1]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[1]) < 1: break;
                    Kera_Model = self._model_evaluation[1][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_hand_Right.append(sum(results)/len(results))
            
                #2 Right Z
                df = pd.DataFrame([data_models[2]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[2]) < 1: break;
                    Kera_Model = self._model_evaluation[2][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_hand_Right.append(sum(results)/len(results))
                
                #0 Left X
                df = pd.DataFrame([data_models[3]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[3]) < 1: break;
                    Kera_Model = self._model_evaluation[3][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_hand_Left.append(sum(results)/len(results))
            
                #1 Left Y
                df = pd.DataFrame([data_models[4]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[4]) < 1: break;
                    Kera_Model = self._model_evaluation[4][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_hand_Left.append(sum(results)/len(results))

                #2 Left Z
                df = pd.DataFrame([data_models[5]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[5]) < 1: break;
                    Kera_Model = self._model_evaluation[5][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_hand_Left.append(sum(results)/len(results))
            elif not self._hand_relation and not (len(val['model_hand_Right'])>0 and len(val['model_hand_Left'])>0):
                if len(val['model_hand_Right'])>0:
                    #0 Right X
                    df = pd.DataFrame([data_models[0]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[0]) < 1: break;
                        Kera_Model = self._model_evaluation[0][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Right.append(sum(results)/len(results))
                
                    #1 Right Y
                    df = pd.DataFrame([data_models[1]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[1]) < 1: break;
                        Kera_Model = self._model_evaluation[1][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Right.append(sum(results)/len(results))
                
                    #2 Right Z
                    df = pd.DataFrame([data_models[2]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[2]) < 1: break;
                        Kera_Model = self._model_evaluation[2][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Right.append(sum(results)/len(results))      
                elif len(val['model_hand_Left'])>0:
                    #0 Left X
                    df = pd.DataFrame([data_models[3]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[0]) < 1: break;
                        Kera_Model = self._model_evaluation[0][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Left.append(sum(results)/len(results))
                    #1 Left Y
                    df = pd.DataFrame([data_models[4]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[1]) < 1: break;
                        Kera_Model = self._model_evaluation[1][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Left.append(sum(results)/len(results))

                    #2 Left Z
                    df = pd.DataFrame([data_models[5]])
                    results = []
                    for i in range(len(df.columns)):
                        data_Predict = np.array(df[i].values.tolist())
                        if len(self._model_evaluation[2]) < 1: break;
                        Kera_Model = self._model_evaluation[2][i]
                        y_pred = Kera_Model.predict(data_Predict)
                        results.append(y_pred[0])
                    if len(results)>0:
                        _results_hand_Left.append(sum(results)/len(results))

            #### Evaluation results
            confidence = []
            results = []
            if self._hand_relation:
                if len(_results_hand_Right)>0 and len(_results_hand_Left)>0:
                    results_tmpRight = ([x >= (self._confidence+0.10) for x in _results_hand_Right])
                    results_tmpLeft  = ([x >= (self._confidence+0.10) for x in _results_hand_Left])
                    results = results_tmpRight + results_tmpLeft
                    confidence = _results_hand_Right + _results_hand_Left
                else:
                    results = [False]
            elif not self._hand_relation:
                if len(_results_hand_Right) == 3:
                    results = ([x >= (self._confidence+0.10) for x in _results_hand_Right])
                    confidence = _results_hand_Right
                elif len(_results_hand_Left) == 3:
                    results = ([x >= (self._confidence+0.10) for x in _results_hand_Left])
                    confidence = _results_hand_Left

            if len(confidence)>0:
                self._confidence_results = sum(confidence)/len(confidence)
            
            for values in results:
                a1 = np.array(values)
                value = value and (a1 == True).all()

            if confidence==0:
                value = False

        return value

    def __model_body_relation(self, data_value=[]):
        """
            Evalua los puntos en los que se determina los brazos entre el mismo, relacion hombro, codo, mano
        """
        if len(self._model_evaluation) < 1: return False
        value = True
        for val in data_value:

            value = True

            _results_body1 = []
            _results_body2 = []

            __value_data = HandModel(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=self._face_relation, body_relation=self._body_relation)
            data_models = __value_data.get_model()
        
            ##### Evaluation body
            if self._hand_relation:
                #0 body X
                df = pd.DataFrame([data_models[6]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[6]) < 1: break;
                    Kera_Model = self._model_evaluation[6][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body1.append(sum(results)/len(results))
            
                #1 body Y
                df = pd.DataFrame([data_models[7]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[7]) < 1: break;
                    Kera_Model = self._model_evaluation[7][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body1.append(sum(results)/len(results))
            
                #2 body Z
                """
                df = pd.DataFrame([data_models[8]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[8]) < 1: break;
                    Kera_Model = self._model_evaluation[8][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body1.append(sum(results)/len(results))
                """

                #0 body X
                df = pd.DataFrame([data_models[9]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[9]) < 1: break;
                    Kera_Model = self._model_evaluation[9][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body2.append(sum(results)/len(results))
            
                #1 body Y
                df = pd.DataFrame([data_models[10]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[10]) < 1: break;
                    Kera_Model = self._model_evaluation[10][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body2.append(sum(results)/len(results))
            
                #2 body Z
                """
                df = pd.DataFrame([data_models[11]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[11]) < 1: break;
                    Kera_Model = self._model_evaluation[11][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body2.append(sum(results)/len(results))
                """ 
            elif not self._hand_relation:
                #0 body X
                df = pd.DataFrame([data_models[6]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[3]) < 1: break;
                    Kera_Model = self._model_evaluation[3][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body1.append(sum(results)/len(results))
            
                #1 body Y
                df = pd.DataFrame([data_models[7]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[4]) < 1: break;
                    Kera_Model = self._model_evaluation[4][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body1.append(sum(results)/len(results))
            
                #2 body Z
                """
                df = pd.DataFrame([data_models[8]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[5]) < 1: break;
                    Kera_Model = self._model_evaluation[5][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body1.append(sum(results)/len(results)) 
                """  

                #0 body X
                df = pd.DataFrame([data_models[9]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[6]) < 1: break;
                    Kera_Model = self._model_evaluation[6][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body2.append(sum(results)/len(results))
            
                #1 body Y
                df = pd.DataFrame([data_models[10]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[7]) < 1: break;
                    Kera_Model = self._model_evaluation[7][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body2.append(sum(results)/len(results))
            
                #2 body Z
                """
                df = pd.DataFrame([data_models[11]])
                results = []
                for i in range(len(df.columns)):
                    data_Predict = np.array(df[i].values.tolist())
                    if len(self._model_evaluation[8]) < 1: break;
                    Kera_Model = self._model_evaluation[8][i]
                    y_pred = Kera_Model.predict(data_Predict)
                    results.append(y_pred[0])
                if len(results)>0:
                    _results_body2.append(sum(results)/len(results))   
                """          
        
            
            #### Evaluation results
            results1 = []
            results2 = []
            value1_tmp = False
            value2_tmp = False
            confidence = []
            if len(_results_body1) >0:
                results = ([x >= self._confidence for x in _results_body1])
                confidence = confidence + _results_body1

            if len(_results_body2) >0:
                results = ([x >= self._confidence for x in _results_body2])
                confidence = confidence + _results_body2

            for values in results1:
                a1 = np.array(values)
                value1_tmp = value1_tmp and (a1 == True).all()

            for values in results2:
                a1 = np.array(values)
                value2_tmp = value2_tmp and (a1 == True).all()

            value = value1_tmp or value2_tmp

            if len(confidence)>0:
                self._confidence_results = (sum(confidence)+0.2)/len(confidence)
            else:
                value = False

        return value


## model handLink - movement core

class HandLink(Imodel):

    def __init__(self, pos, value: Model, next_1: any = None, next_2: any = None, last=False):
        self._pos = pos
        self._value = value
        self._last = last
        self.next_1 = next_1 #izquierdo
        self.next_2 = next_2 #derecho

    def setNext1(self, value: Model):
        self.next_1 = value

    def setNext2(self, value: Model):
        self.next_2 = value

    def set_Last(self):
        self._last = True

    def get_pos(self):
        return self._pos

    def get_result(self, data, lenght):
        tmp_rst = self._value.get_result(data)
        print(tmp_rst)
        if tmp_rst['rule_match']:
            return {
                'pos': self._pos,
                'rst': tmp_rst,
                'size': 0,
                'label': ''
            }
        
        tmp_rst = None     

        if lenght > 0:
            if self.next_1 != None:
                tmp_rst = self.next_1.get_result(data, (lenght-1))
                if tmp_rst != None: return tmp_rst

            tmp_rst = None 

            if self.next_2 != None:
                tmp_rst = self.next_2.get_result(data, (lenght-1))
                if tmp_rst != None: return tmp_rst

        return None

class HandLinkModel(Imodel):
    def __init__(self, label="", model_value=[]):
        self._label = label
        self._raiz = None
        self._size = 0
        self._model_complete = True
        self.LinkValues(model_value=model_value)

    def getSize(self):
        return self._size
    
    def get_result(self, data):
        tmp =  self._raiz.get_result(data, 2)
        if tmp is None: return None
        tmp['size'] = self._size
        tmp['label'] = self._label
        print(tmp)
        return tmp
    
    def get_result_byPos(self, data, pos):
        model_result = self.find_nodo(self._raiz, pos)
        tmp =  model_result.get_result(data, 1)
        if tmp is None: return None
        tmp['size'] = self._size
        tmp['label'] = self._label
        return tmp

    def LinkValues(self, model_value=[]):
        try:
            pos = 1
            for i in range(len(model_value)):
                if pos == 1 and i == 0 and self._raiz is None:
                    self._raiz = HandLink(pos=pos, value=model_value[i], next_1=None, next_2=None, last=False)                
                if (i+2) < len(model_value):  
                    self._model_complete = self._model_complete and self.add_der(pos_parent=pos, pos_hijo=(pos+2), model_value=model_value[i], isLast=False)   
                if (i+1) < len(model_value):
                    self._model_complete = self._model_complete and self.add_izq(pos_parent=pos, pos_hijo=(pos+1), model_value=model_value[i], isLast=False)
                
                if self._model_complete == False:
                    print("Error Ocurrido [HandLinkModel], -{0}- Mensaje: {1}".format(self._label, "Excepcion, construccion de red fallida."))
                    raise SystemError

                self._size = self._size + 1
                pos = pos + 1

            pos = pos - 1
            for i in range(5):
                model_last = self.find_nodo(self._raiz, (pos-i))
                model_last.set_Last()

        except Exception as e:
            print("Error Ocurrido [HandLinkModel], Mensaje: {0}".format(str(e)))
            raise SystemError

    def add_izq(self, pos_parent, pos_hijo, model_value, isLast=False):
        model_parent = self.find_nodo(self._raiz, pos_parent)
        if model_parent:
            model_parent.setNext1(HandLink(pos=pos_hijo, value=model_value, next_1=None, next_2=None, last=isLast))
            return True
        return False

    def add_der(self, pos_parent, pos_hijo, model_value, isLast=False):
        model_parent = self.find_nodo(self._raiz, pos_parent)
        if model_parent != None:
            model_parent.setNext2(HandLink(pos=pos_hijo, value=model_value, next_1=None, next_2=None, last=isLast))
            return True
        return False

    def find_nodo(self, model_actual, pos):
        if model_actual is None or model_actual.get_pos() == pos:
            return model_actual

        nodo_izquierdo = self.find_nodo(model_actual.next_1, pos)
        if nodo_izquierdo:
            return nodo_izquierdo

        nodo_derecho = self.find_nodo(model_actual.next_2, pos)
        return nodo_derecho


