#recoleccion de datos obtenidos
## --output -> model_result_object [resultados obtenidos]
def model_object_result(value_result, Error = None):
    model_results = {
        'logs': [],
        'coincidences': []
    }
    if Error == None:
        model_results["coincidences"] = list(filter(lambda a: a['rule_match'], value_result))
        model_results['logs'] = {
            "message": "recognition_model_execution_pass",
            "value": "A total of "+ str(len(model_results["coincidences"])) + " matching results were found",
            #"models_evaluated": value_result
        }
    else:
        model_results['logs'] = {
            "message": "error",
            "value": (Error),
            "type_error": type(Error)
        }

    return model_results