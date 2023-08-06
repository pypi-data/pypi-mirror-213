import model_class_tf as mc
import model_transfer as mf
import json

class sign_language:
    def __init__(self):
        self.__sign_models_ev = []
        self.__sign_models_mov = []

    def get_SignModels(self,training_configuration=[]):
        list_Trains = []
        try:
            error = False
            for signs in training_configuration:
                
                if 'label' in signs and 'configuration' in signs and 'folderPath' in signs and 'countTraining' in signs:
                    
                    dataTmp = []
                    path = signs['folderPath']
                    value = signs['label']

                    for num in range(signs['countTraining']):
                        data_obtained = None
                        try:
                            f = open(path+'\\'+value+'\\'+value+str(num)+'.json')
                            data_obtained = json.load(f)
                        except Exception as e:
                            data_obtained = None
                            error = True
                            print("Error Ocurrido, Mensaje: Entrenamiento Invalido, verifique la data de entrenamiento de la letra:[{0}]".format(value))
                            break

                        if data_obtained != None:
                            dataTmp.append(data_obtained)
                    
                    if not error:
                        #verifica que la configuracion este correcta - identidad temporal
                        tmp_identity = mf.SignModel(SYSTEM=True, data=dataTmp, configuration=signs['configuration'])
                        
                        ##modelo entrenamiento
                        TrainTmp = mc.TrainModel(
                            label=signs['label'],
                            data=tmp_identity.get_dataModel(), 
                            hands_relation=tmp_identity.get_isHandsRelationModel(),
                            face_relation=tmp_identity.get_isFaceRelationModel(),
                            body_relation=tmp_identity.get_isBodyRelationModel(),
                            move_relation=tmp_identity.get_isMoveRelationModel()
                        )

                        list_Trains.append(TrainTmp)
                if error:
                    list_Trains = []
                    break
                    
        except Exception as e:
            print("Error Ocurrido [getValues], Mensaje: {0}".format(str(e)))
            list_Trains = []
        
        return list_Trains

    def Train(self, training_configuration=[]):
        try:
            if len(training_configuration)>0:
                list_Trains = self.get_SignModels(training_configuration=training_configuration)
                list_Trains_static = list(filter(lambda a: a.isMoveRelation() == False, list_Trains))
                for trains in list_Trains_static:
                    ## building model - static words 
                    
                    #### validacion entrenamiento
                    trains.Train_models()
                    model_evaluation = trains.getModel_Evaluation()
                    model_configuration = trains.getConfiguration()

                    if len(model_evaluation[0]) == 0:
                        self.__sign_models_ev = []
                        break

                    ### creacion modelo de evaluacion
                    self.__sign_models_ev.append(
                        mc.Model(
                            hands_relation=model_configuration['hands_relation'],
                            face_relation=model_configuration['face_relation'],
                            body_relation=model_configuration['body_relation'],
                            move_relation=model_configuration['move_relation'],
                            label=model_configuration['label'],
                            ModelsEvaluation=model_evaluation[0]
                        )
                    )
                
                list_Trains_mov = list(filter(lambda a: a.isMoveRelation() == True, list_Trains))

                for trains in list_Trains_mov:
                    ## building model - mov words 
                    
                    #### validacion entrenamiento
                    trains.Train_modelsMov()
                    model_evaluation = trains.getModel_Evaluation()
                    model_configuration = trains.getConfiguration()

                    if len(model_evaluation[0]) == 0:
                        self.__sign_models_ev = []
                        break

                    sign_models_ev_tmp = []
                    for model_evaluation_value in model_evaluation[0]:
                        sign_models_ev_tmp.append(
                            mc.Model(
                                hands_relation=model_configuration['hands_relation'],
                                face_relation=model_configuration['face_relation'],
                                body_relation=model_configuration['body_relation'],
                                move_relation=model_configuration['move_relation'],
                                label=model_configuration['label'],
                                ModelsEvaluation=model_evaluation_value
                            )
                        )

                    self.__sign_models_mov.append(
                        mc.HandLinkModel(
                            label=model_configuration['label'],
                            model_value=sign_models_ev_tmp
                        )
                    )
                print("Modelo Implementado, señas reconocidas: {0}".format(str(len(self.__sign_models_ev)+len(self.__sign_models_mov))))

            else:
                raise mf.InvalidModelException()
        except Exception as e:
            print("Error Ocurrido [Train], Mensaje: {0}".format(str(e)))

    def Predict(self, data=[]):
        try:
            ## execution identify words
            value_result = []
            for a in self.__sign_models_ev:
                value_result.append(a.get_result(data=data))
            
            if len(list(filter(lambda a: a['rule_match'], value_result)))>0: 
                return self.model_object_result(value_result=value_result)
            
            ## execution identify movement words
            value_resultMov = []
            for a in self.__sign_models_mov:
                tmp = a.get_result(data=data)
                if tmp != None: value_resultMov.append(tmp)

            if len(list(filter(lambda a: a['rule_match'], value_resultMov)))>0: 
                return self.model_object_result(value_result=value_resultMov)


            return self.model_object_result(value_result=[])
        except Exception as e:
            print("Error Ocurrido [Predict], Mensaje: {0}".format(str(e)))
            return self.model_object_result(value_result=[])

    def model_object_result(self,value_result):
        model_results = {
            'logs': [],
            'coincidences': [],
            'results': []
        }
        model_results["coincidences"] = list(filter(lambda a: a['rule_match'], value_result))
        model_results['logs'] = {
            "message": "recognition_model_execution_pass",
            "value": "A total of "+ str(len(model_results["coincidences"])) + " matching results were found",
        }
        model_results["results"] = value_result

        return model_results