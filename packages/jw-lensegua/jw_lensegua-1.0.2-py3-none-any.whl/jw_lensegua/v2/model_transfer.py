import json

class InvalidModelException(Exception):
    "Raised when valuemodel is None"
    pass

class SignModel:
        
    def __init__(self, SYSTEM = False, data: list=None, configuration = None):
        self.__data = []
        self.__configuration = {
            'label': '',
            'hands_relation': False,
            'face_relation': False,
            'body_relation': False,
            'move_relation': False
        }
        if SYSTEM:
            if data != None:
                if configuration != None:
                    if 'label' in configuration:
                        if 'hands_relation' in configuration:
                            if 'face_relation' in configuration:
                                if 'body_relation' in configuration:
                                    if 'move_relation' in configuration:
                                        self.__data = data
                                        self.__configuration = configuration
                                    else:
                                        raise InvalidModelException()
                                else:
                                    raise InvalidModelException()
                            else:
                                raise InvalidModelException()
                        else:
                            raise InvalidModelException()
                    else:
                        raise InvalidModelException()
                else:
                    raise InvalidModelException()
            else:
                raise InvalidModelException()
        
    def get_dataModel(self):
        return self.__data
    
    def get_labelModel(self):
        return self.__configuration['label']
    
    def get_isHandsRelationModel(self):
        return self.__configuration['hands_relation']
    
    def get_isFaceRelationModel(self):
        return self.__configuration['face_relation']
    
    def get_isBodyRelationModel(self):
        return self.__configuration['body_relation']
    
    def get_isMoveRelationModel(self):
        return self.__configuration['move_relation']

    def from_json(self, json_data: str):
        try:
            json_object = json.loads(json_data)
            if 'data' in json_object:
                if 'configuration' in json_object:
                    if 'label' in json_object['configuration']:
                        if 'hands_relation' in json_object['configuration']:
                            if 'face_relation' in json_object['configuration']:
                                if 'body_relation' in json_object['configuration']:
                                    if 'move_relation' in json_object['configuration']:
                                        self.__data = json_object['data']
                                        self.__configuration = json_object['configuration']
                                    else:
                                        print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, [configuration] is invalid"))
                                else:
                                    print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, [configuration] is invalid"))
                            else:
                                print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, [configuration] is invalid"))
                        else:
                            print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, [configuration] is invalid"))
                    else:
                        print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, [configuration] is invalid"))
                else:
                    print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, missing attr - [configuration] is required"))
            else:
                print("Error Ocurrido, Mensaje: {0}".format("JSON Invalido, missing attr - [data] is required"))
        except Exception as e:
            print("Error Ocurrido, Mensaje: {0}".format(str(e)))