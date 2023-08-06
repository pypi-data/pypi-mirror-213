## reconocimiento Patron A
def hand_A(data):
    result = {
        "hand_value": "A",
        "rule_match": False
    }
    points_midd = [
        data[0],
        data[4],
        data[5],
        data[9], 
        data[13],
        data[17]
    ]

    points_tip = [
        data[1],
        data[2],
        data[3],
        data[4]
    ]

    points_top = [
        data[4],
        data[8],
        data[12],
        data[16], 
        data[20]
    ]

    ## obtener el punto mas alto, entre los puntos de enmedio conforme el pulgar
    results_y_iter = dict(map(lambda a: (a['index'], a['y']), points_midd))
    Y_axis_major = (list(filter(lambda x: results_y_iter[x] == min(results_y_iter.values()), results_y_iter))[0])

    ## obtener el punto mas alto, entre los puntos de enmedio conforme el pulgar
    results_top_iter = dict(map(lambda a: (a['index'], a['y']), points_top))
    top_axis_major = (list(filter(lambda x: results_top_iter[x] == min(results_top_iter.values()), results_top_iter))[0])

    ## distancia entre puntos Y_axis
    diff_y_values = (points_top[1]['y'] - points_top[0]['y']) > (0.1)

    ## obtener el punto mas alto entre los puntos medios para identificar posicion, sin incluir WRIST
    results_z_iter = dict(map(lambda a: (a['index'], a['y']), points_midd))
    results_z_iter.pop("WRIST")
    Z_axis_major = (list(filter(lambda x: results_z_iter[x] == min(results_z_iter.values()), results_z_iter))[0])

    ## determinacion de la variacion entre puntos, evita ser relacionado con G y otros
    results_thumb_iter = list(map(lambda a: abs(a['y']), points_tip))
    shift_thumb = (list(filter(lambda a: a>1, results_thumb_iter)))

    if diff_y_values:
        if Y_axis_major == Z_axis_major and top_axis_major == Y_axis_major and Z_axis_major==top_axis_major:
            if len(shift_thumb) == 0:
                result['rule_match'] = True
    return result

## reconocimiento Patron B
def hand_B(data):
    result = {
        "hand_value": "B",
        "rule_match": False
    }
    points_1 = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_2 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ] 
    points_3 = [
        data[7],
        data[11],
        data[15],
        data[20]
    ]

    points_p1 = points_1 + [data[4]]
    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p1_diff_minor = (list(filter(lambda x: p1_diff[x] == max(p1_diff.values()), p1_diff))[0])
    p1_diff_major1 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("MIDDLE_FINGER_TIP")
    p1_diff_major2 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])

    p2_diff1 = (data[4]['x'] < (data[13]['x']+0.001)) and (data[4]['x'] < (data[13]['x']-0.001))
    p2_diff2 = (data[4]['x'] > (data[5]['x']+0.001)) and (data[4]['x'] > (data[5]['x']-0.001))
    p2_diff = p2_diff1 and p2_diff2

    points_p2 = points_2 + points_3 + [data[4]]
    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p3_diff_major1 = (list(filter(lambda x: p3_diff[x] == min(p3_diff.values()), p3_diff))[0])
    p3_diff.pop("MIDDLE_FINGER_DIP")
    p3_diff_major2 = (list(filter(lambda x: p3_diff[x] == min(p3_diff.values()), p3_diff))[0])
    
    if p1_diff_minor == "THUMB_TIP":
        if p2_diff:
            if p1_diff_major1 == "MIDDLE_FINGER_TIP" or p1_diff_major2 == "INDEX_FINGER_TIP":
                if p3_diff_major1 == "MIDDLE_FINGER_DIP" or p3_diff_major2 == "INDEX_FINGER_DIP":
                    result['rule_match'] = True
    return result
    
## reconocimiento Patron C
def hand_C(data):
    result = {
        "hand_value": "C",
        "rule_match": False
    }
    points_top = [
        data[12],
        data[16],
        data[20]
    ]
    points_midd = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_reference = [
        data[4],
        data[8]
    ]
    points_ref = [
        data[8],
        data[10],
        data[4]
    ]

    ## identificacion de punto relativo
    points_calculate = points_midd + points_reference
    results_top_dif = dict(map(lambda a: (a['index'], a['y']), points_calculate))
    results_sup_diff = (list(filter(lambda x: results_top_dif[x] == max(results_top_dif.values()), results_top_dif))[0])
    results_top_diff = (list(filter(lambda x: results_top_dif[x] == min(results_top_dif.values()), results_top_dif))[0])

    ## distancia entre puntos 4,8  Y_axis
    results_distance = points_reference[0]['y'] - points_reference[1]['y']

    ## distancia entre puntos 4,8 X_axis
    diff_x_values = (abs(points_reference[0]['x'] - points_reference[1]['x']) < 0.1)
  
    ## obtemer el punto mas alto entre los puntos de relacion
    points_major = points_midd + points_top + points_reference
    points_major_dict = dict(map(lambda a: (a['index'], a['y']), points_major))
    point_minor = (list(filter(lambda x: points_major_dict[x] == max(points_major_dict.values()), points_major_dict))[0])
    point_major = (list(filter(lambda x: points_major_dict[x] == min(points_major_dict.values()), points_major_dict))[0])

    points_defined = [points_midd[0] , points_reference[0]]
    points_defined_dict = dict(map(lambda a: (a['index'], a['y']), points_defined))
    defined_minor = (list(filter(lambda x: points_defined_dict[x] == max(points_defined_dict.values()), points_defined_dict))[0])
    defined_major = (list(filter(lambda x: points_defined_dict[x] == min(points_defined_dict.values()), points_defined_dict))[0])

    points_top_diff = abs(points_ref[0]['y'] - points_ref[2]['y'])
    points_mid_diff = points_top_diff/2
    points_top_diff1 = abs(points_mid_diff - abs(points_ref[0]['y'] - points_ref[1]['y']))
    points_top_diff2 = abs(points_mid_diff -abs(points_ref[1]['y'] - points_ref[2]['y']))

    if results_top_diff == "INDEX_FINGER_TIP" and results_sup_diff == "THUMB_TIP":
        if results_distance > 0:
            if diff_x_values:
                if point_major == "INDEX_FINGER_TIP" and point_minor == "PINKY_TIP":
                    if defined_major == "INDEX_FINGER_MCP" and defined_minor == "THUMB_TIP":
                        if points_top_diff2 == points_top_diff1 and points_top_diff1 < 0.01:
                            result['rule_match'] = True
    return result

## reconocimiento Patron D
def hand_D(data):
    result = {
        "hand_value": "D",
        "rule_match": False
    }
    points_top = [
        data[8],
        data[7]
    ]
    points_mid = [
        data[10],
        data[5],
        data[9],
        data[13],
        data[17],
        data[14],
        data[19]
    ]
    points_sup = [
        data[16],
        data[20]
    ]
    points_reference = [
        data[4],
        data[12]
    ]

    ## convergencia de puntos de relacion 4,8
    diff_reference_y = (abs(points_reference[0]['y'] - points_reference[1]['y']))
    diff_reference_x = (abs(points_reference[0]['x'] - points_reference[1]['x']))
    
    ## diferencia entre el mayor de los puntos
    points_defined = points_top + points_mid + points_reference + points_sup
    points_defined_dict = dict(map(lambda a: (a['index'], a['y']), points_defined))
    defined_minor = (list(filter(lambda x: points_defined_dict[x] == max(points_defined_dict.values()), points_defined_dict))[0])
    defined_major = (list(filter(lambda x: points_defined_dict[x] == min(points_defined_dict.values()), points_defined_dict))[0])

    ## diferencia entre el mayor de los puntos
    points_defined_sup = points_reference + points_sup
    points_defined_sup_dict = dict(map(lambda a: (a['index'], a['y']), points_defined_sup))
    points_defined_sup_dict.pop("MIDDLE_FINGER_TIP")
    defined_minor_sup = (list(filter(lambda x: points_defined_sup_dict[x] == max(points_defined_sup_dict.values()), points_defined_sup_dict))[0])
    defined_major_sup = (list(filter(lambda x: points_defined_sup_dict[x] == min(points_defined_sup_dict.values()), points_defined_sup_dict))[0])
    
    #diferencia entre puntos de relacion - aspecto
    diff_reference_10_4 = (abs(points_mid[0]['y'] - points_reference[1]['y']))
    diff_reference_6_10 = (abs(data[6]['y'] - points_mid[0]['y']))

    if diff_reference_x < 0.01 and diff_reference_y < 0.01:
        if defined_major == "INDEX_FINGER_TIP":
            if defined_minor == "PINKY_TIP" or defined_minor == "RING_FINGER_TIP":
                if defined_major_sup == "THUMB_TIP":
                    if defined_minor_sup == "PINKY_TIP" or defined_minor_sup == "RING_FINGER_TIP":
                        if diff_reference_10_4 > 0.01 and diff_reference_6_10 > 0.01:
                            result['rule_match'] = True

    return result

## reconocimiento Patron E
def hand_E(data):
    result = {
        "hand_value": "E",
        "rule_match": False
    }
    points_top = [
        data[6],
        data[10],
        data[14],
        data[18]
    ]
    points_mid = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_mid_sup = [
        data[7],
        data[11],
        data[15],
        data[19]
    ]
    points_mid_top = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    point_ref = [
        data[4],
        data[3]
    ]

    results_top_diff = dict(map(lambda a: (a['index'], a['y']), points_top))
    results_top_major = (list(filter(lambda x: results_top_diff[x] == min(results_top_diff.values()), results_top_diff))[0])

    points_p = points_mid
    points_p.append(data[4])
    results_p_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    results_p_minor = (list(filter(lambda x: results_p_diff[x] == max(results_p_diff.values()), results_p_diff))[0])
    points_p.pop()

    points_m = points_mid_sup + points_mid_top
    results_m_diff = dict(map(lambda a: (a['index'], a['y']), points_m))
    results_m_major = (list(filter(lambda x: results_m_diff[x] == min(results_m_diff.values()), results_m_diff))[0])
    results_m_minor = (list(filter(lambda x: results_m_diff[x] == max(results_m_diff.values()), results_m_diff))[0])
   
    points_m1 = points_mid_top + points_mid
    results_m1_diff = dict(map(lambda a: (a['index'], a['y']), points_m1))
    results_m1_major = (list(filter(lambda x: results_m1_diff[x] == min(results_m1_diff.values()), results_m1_diff))[0])
    results_m1_minor = (list(filter(lambda x: results_m1_diff[x] == max(results_m1_diff.values()), results_m1_diff))[0])
 
    result_diff_point = abs(point_ref[0]['y']-point_ref[1]['y'])<0.01

    if results_top_major == "MIDDLE_FINGER_PIP":
        if results_p_minor == "THUMB_TIP":
            if results_m_minor == "INDEX_FINGER_TIP" and results_m_major == "MIDDLE_FINGER_DIP":
                if results_m1_major == "RING_FINGER_TIP" or results_m1_major == "PINKY_TIP":
                    if results_m1_minor == "PINKY_MCP":
                        if result_diff_point:
                            result["rule_match"] = True

    return result

## reconocimiento Patron F
def hand_F(hand1):
    result = {
        "hand_value": "F",
        "rule_match": False
    }
    

    return result

## reconocimiento Patron G
def hand_G(model_input):
    result = {
        "hand_value": "G",
        "rule_match": False
    }
    if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
        data_1 = model_input['model_hand'][0]['index']
        data_2 = model_input['model_hand'][1]['index']
        result_tmp = hand_GOperation(hand=data_1, hand_direction=model_input['model_hand'][0]['position'], face=model_input['model_face'], body=model_input['model_body'])
        if result_tmp['rule_match'] == False:
            result_tmp1 = hand_GOperation(hand=data_2, hand_direction=model_input['model_hand'][1]['position'],face=model_input['model_face'], body=model_input['model_body'])
            result["rule_match"] = result_tmp1['rule_match']
        else:
            result["rule_match"] = result_tmp['rule_match']
    else:
        data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
        hand_directions = model_input['model_hand'][0]['position'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['position']
        result_tmp = hand_GOperation(hand=data, hand_direction=hand_directions,face=model_input['model_face'], body=model_input['model_body'])
        result["rule_match"] = result_tmp['rule_match']
    return result

def hand_GOperation(hand, hand_direction, face, body):
    result_tmp = {
        "hand_value": "G",
        "rule_match": False
    }
    
    #hand-evaluation
    points_top = [
        hand[6],
    ]
    points_ref = [
        hand[4],
        hand[8],
        hand[10]
    ]
    points_sup = [
        hand[16],
        hand[17],
        hand[20]
    ]

    point_ear = None
    pose_ear = None

    #face-evaluation
    if hand_direction == "Left":
        point_ear = face[5]
    else:
        point_ear = face[4]

    #pose-evaluation
    if hand_direction == "Left":
        pose_ear = body[7]
    else:
        pose_ear = body[8]

    #-----------------------------------
    diff_ear_tmp_y = abs(point_ear['y'] - pose_ear['y'])<0.01
    diff_ear_tmp_x = abs(point_ear['x'] - pose_ear['x'])<0.01

    points_p = points_top + points_ref
    results_p_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    results_p_minor = (list(filter(lambda x: results_p_diff[x] == min(results_p_diff.values()), results_p_diff))[0])
    
    results_ref_diff = dict(map(lambda a: (a['index'], a['y']), points_ref))
    min_ref_diff = (max(results_ref_diff.values()))
    pose_diff_ref = abs(pose_ear['y'] - min_ref_diff)<0.1
    face_diff_ref = abs(point_ear['y'] - min_ref_diff)<0.1
    
    results_ref_diffx = dict(map(lambda a: (a['index'], a['x']), points_ref))
    min_ref_diffx = (max(results_ref_diffx.values()))
    pose_diff_refx = abs(pose_ear['x'] - min_ref_diffx)<0.1
    face_diff_refx = abs(point_ear['x'] - min_ref_diffx)<0.1   

    min_diff_sup = dict(map(lambda a: (a['index'], a['y']), points_sup))
    results_max_sup = (list(filter(lambda x: min_diff_sup[x] == min(min_diff_sup.values()), min_diff_sup))[0])
    results_min_sup = (list(filter(lambda x: min_diff_sup[x] == max(min_diff_sup.values()), min_diff_sup))[0])

    if results_p_minor == "INDEX_FINGER_PIP":
        if results_max_sup == "PINKY_MCP":
            if results_min_sup == "PINKY_TIP" or results_min_sup == "RING_FINGER_TIP":
                if pose_diff_ref and face_diff_ref:
                    if pose_diff_refx and face_diff_refx:
                        if diff_ear_tmp_x and diff_ear_tmp_y:
                            result_tmp["rule_match"] = True

    return result_tmp

## reconocimiento Patron H
def hand_H(model_input):
    result = {
        "hand_value": "H",
        "rule_match": False
    }
    if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
        data_1 = model_input['model_hand'][0]['index']
        data_2 = model_input['model_hand'][1]['index']
        result_tmp = hand_HOperation(hand=data_1, hand_direction=model_input['model_hand'][0]['position'], face=model_input['model_face'], body=model_input['model_body'])
        if result_tmp['rule_match'] == False:
            result_tmp1 = hand_HOperation(hand=data_2, hand_direction=model_input['model_hand'][1]['position'],face=model_input['model_face'], body=model_input['model_body'])
            result["rule_match"] = result_tmp1['rule_match']
        else:
            result["rule_match"] = result_tmp['rule_match']
    else:
        data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
        hand_directions = model_input['model_hand'][0]['position'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['position']
        result_tmp = hand_HOperation(hand=data, hand_direction=hand_directions,face=model_input['model_face'], body=model_input['model_body'])
        result["rule_match"] = result_tmp['rule_match']
    return result

def hand_HOperation(hand, hand_direction, face, body):
    result_tmp = {
        "hand_value": "H",
        "rule_match": False
    }

    #hand-evaluation
    points_top = [
        hand[8],
        hand[12]
    ]
    points_mid = [
        hand[5],
        hand[9],
        hand[13],
        hand[17]
    ]
    
    #body-evaluation
    pose_mouth = [
        body[9],
        body[10]
    ]

    #face-evaluation
    face_mouth = face[3]

    #----------------------------
    diff_top_y = abs(points_top[0]['y']-points_top[1]['y'])<0.01
    diff_top_x = abs(points_top[0]['x']-points_top[1]['x'])<0.1

    diff_x_mouth1 = ((pose_mouth[1]['x']-0.01)<= points_top[0]['x'] <= (pose_mouth[0]['x']-0.01)) or ((pose_mouth[1]['x']+0.01)<= points_top[0]['x'] <= (pose_mouth[0]['x']+0.01))
    diff_x_mouth2 = ((pose_mouth[1]['x']-0.01)<= points_top[1]['x'] <= (pose_mouth[0]['x']-0.01)) or ((pose_mouth[1]['x']+0.01)<= points_top[1]['x'] <= (pose_mouth[0]['x']+0.01))

    diff_y_mouth1_tmp1 = (((pose_mouth[1]['y']-0.01)<= points_top[0]['y']) or ((pose_mouth[0]['x']-0.01)<= points_top[0]['y'])) or (((pose_mouth[1]['y']+0.01)<= points_top[0]['y']) or ((pose_mouth[0]['x']+0.01)<= points_top[0]['y']))
    diff_y_mouth1_tmp2 = (((pose_mouth[1]['y']-0.01)>= points_top[0]['y']) or ((pose_mouth[0]['x']-0.01)>= points_top[0]['y'])) or (((pose_mouth[1]['y']+0.01)>= points_top[0]['y']) or ((pose_mouth[0]['x']+0.01)>= points_top[0]['y']))
    diff_y_mouth2_tmp1 = (((pose_mouth[1]['y']-0.01)<= points_top[1]['y']) or ((pose_mouth[0]['x']-0.01)<= points_top[1]['y'])) or (((pose_mouth[1]['y']+0.01)<= points_top[1]['y']) or ((pose_mouth[0]['x']+0.01)<= points_top[1]['y']))
    diff_y_mouth2_tmp2 = (((pose_mouth[1]['y']-0.01)>= points_top[1]['y']) or ((pose_mouth[0]['x']-0.01)>= points_top[1]['y'])) or (((pose_mouth[1]['y']+0.01)>= points_top[1]['y']) or ((pose_mouth[0]['x']+0.01)>= points_top[1]['y']))
    diff_y_mouth1 = diff_y_mouth1_tmp1 or diff_y_mouth1_tmp2
    diff_y_mouth2 = diff_y_mouth2_tmp1 or diff_y_mouth2_tmp2

    points_p = points_mid
    points_p.append(hand[4])
    results_p_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    results_p_major = (list(filter(lambda x: results_p_diff[x] == min(results_p_diff.values()), results_p_diff))[0])
    results_p_minor = (list(filter(lambda x: results_p_diff[x] == max(results_p_diff.values()), results_p_diff))[0])
    points_p.pop()

    points_p_temp = points_mid
    points_p_temp.append(hand[16])
    points_p_temp.append(hand[20])
    results_tmp_diff = dict(map(lambda a: (a['index'], a['y']), points_p_temp))
    results_tmp_major = (list(filter(lambda x: results_tmp_diff[x] == min(results_tmp_diff.values()), results_tmp_diff))[0])
    results_tmp_minor = (list(filter(lambda x: results_tmp_diff[x] == max(results_tmp_diff.values()), results_tmp_diff))[0])
    points_p_temp.pop()

    if diff_top_y and diff_top_x:
        if diff_x_mouth2 and diff_x_mouth1:
            if diff_y_mouth1 and diff_y_mouth2:
                if results_p_major == "THUMB_TIP" and results_p_minor == "PINKY_MCP":
                    if results_tmp_minor == "PINKY_TIP" and results_tmp_major == "INDEX_FINGER_MCP":
                        result_tmp['rule_match'] = True
    
    return result_tmp

## reconocimiento Patron I
def hand_I(model_input):
    result = {
        "hand_value": "I",
        "rule_match": False
    }
    if len(model_input['model_hand'][0]['index']) > 0 and len(model_input['model_hand'][1]['index']) > 0:
        data_1 = model_input['model_hand'][0]['index']
        data_2 = model_input['model_hand'][1]['index']
        result_tmp = hand_IOperation(hand=data_1, hand_direction=model_input['model_hand'][0]['position'], face=model_input['model_face'], body=model_input['model_body'])
        if result_tmp['rule_match'] == False:
            result_tmp1 = hand_IOperation(hand=data_2, hand_direction=model_input['model_hand'][1]['position'],face=model_input['model_face'], body=model_input['model_body'])
            result["rule_match"] = result_tmp1['rule_match']
        else:
            result["rule_match"] = result_tmp['rule_match']
    else:
        data = model_input['model_hand'][0]['index'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['index']
        hand_directions = model_input['model_hand'][0]['position'] if (len(model_input['model_hand'][0]['index']) > 0) else model_input['model_hand'][1]['position']
        result_tmp = hand_IOperation(hand=data, hand_direction=hand_directions,face=model_input['model_face'], body=model_input['model_body'])
        result["rule_match"] = result_tmp['rule_match']
    return result

def hand_IOperation(hand, hand_direction, face, body):
    result_tmp = {
        "hand_value": "I",
        "rule_match": False
    }

    #hand-evaluation
    points_top = [
        hand[20]
    ]
    points_mid = [
        hand[10],
        hand[14],
        hand[18]
    ]
    points_sup = [
        hand[8],
        hand[12],
        hand[16],
        hand[17]
    ]

    face_value = None
    body_value = None
    
    #face-evaluation, pose-evaluation
    if hand_direction == "Right":
        face_value = [
            face[2],
            face[0],
            face[3]            
        ]
        body_value = [
            body[0],
            body[5],
            body[10]
        ]
    else:
        face_value = [
            face[2],
            face[1],
            face[3]            
        ]
        body_value = [
            body[0],
            body[2],
            body[9]
        ]
    
    results_p_diff = dict(map(lambda a: (a['index'], a['y']), points_sup))
    results_p_major = (list(filter(lambda x: results_p_diff[x] == min(results_p_diff.values()), results_p_diff))[0])
    results_p_minor = (list(filter(lambda x: results_p_diff[x] == max(results_p_diff.values()), results_p_diff))[0])
    
    res_diff_tmp1 = abs(points_mid[0]['y'] - points_mid[1]['y'])<0.01
    res_diff_tmp2 = abs(points_mid[0]['y'] - points_mid[2]['y'])<0.01

    #mouth-validation
    res_tmp  = (points_top[0]['y'] <= (face_value[2]['y']-0.01)) or (points_top[0]['y'] <= (face_value[2]['y']+0.01))
    res_tmp1 = (points_top[0]['y'] <= (body_value[2]['y']-0.01)) or (points_top[0]['y'] <= (body_value[2]['y']+0.01))
    #eye-validation
    res_tmp2 = (points_top[0]['y'] >= (face_value[1]['y']-0.01)) or (points_top[0]['y'] >= (face_value[1]['y']+0.01))
    res_tmp3 = (points_top[0]['y'] >= (body_value[1]['y']-0.01)) or (points_top[0]['y'] >= (body_value[1]['y']+0.01))
    #nose-validation
    res_tmp4 = (points_top[0]['y'] >= (face_value[0]['y']-0.01)) or (points_top[0]['y'] >= (face_value[0]['y']+0.01))
    res_tmp5 = (points_top[0]['y'] >= (body_value[0]['y']-0.01)) or (points_top[0]['y'] >= (body_value[0]['y']+0.01))
    res_tmp6 = (points_top[0]['y'] <= (face_value[0]['y']-0.01)) or (points_top[0]['y'] <= (face_value[0]['y']+0.01))
    res_tmp7 = (points_top[0]['y'] <= (body_value[0]['y']-0.01)) or (points_top[0]['y'] <= (body_value[0]['y']+0.01))

    validation_mouth = res_tmp or res_tmp1
    validation_eye   = res_tmp2 or res_tmp3
    validation_nose  = res_tmp4 or res_tmp5 or res_tmp6 or res_tmp7

    if results_p_major == "INDEX_FINGER_TIP" and (results_p_minor == "RING_FINGER_TIP" or results_p_minor == "PINKY_MCP"):
        if res_diff_tmp2 and res_diff_tmp1:
            if validation_eye and validation_mouth and validation_nose:
                result_tmp['rule_match'] = True

    return result_tmp

## reconocimiento Patron J
def hand_J(data):
    result = {
        "hand_value": "J",
        "rule_match": False
    }
    

    return result

## reconocimiento Patron K
def hand_K(data):
    result = {
        "hand_value": "K",
        "rule_match": False
    }
    
    points_top = [
        data[4],
        data[8],
        data[12]
    ]
    points_mid = [
        data[14],
        data[16],
        data[17],
        data[20]
    ]
    points_sup = [
        data[13], data[4], #top4
        data[9], data[12], #top9
        data[5],  data[8]  #top8
    ]

    top_diff = dict(map(lambda a: (a['index'], a['y']), points_top))
    top_diff_major = (list(filter(lambda x: top_diff[x] == min(top_diff.values()), top_diff))[0])
    top_diff_minor = (list(filter(lambda x: top_diff[x] == max(top_diff.values()), top_diff))[0])
    
    mid_diff = dict(map(lambda a: (a['index'], a['y']), points_mid))
    mid_diff_major = (list(filter(lambda x: mid_diff[x] == min(mid_diff.values()), mid_diff))[0])
    mid_diff_minor = (list(filter(lambda x: mid_diff[x] == max(mid_diff.values()), mid_diff))[0])

    #sup1
    sup1 = [points_sup[0], points_sup[1]]
    sup1_diff = dict(map(lambda a: (a['index'], a['y']), sup1))
    sup1_diff_major = (list(filter(lambda x: sup1_diff[x] == min(sup1_diff.values()), sup1_diff))[0])
    #sup2
    sup2 = [points_sup[2], points_sup[3]]
    sup2_diff = dict(map(lambda a: (a['index'], a['y']), sup2))
    sup2_diff_major = (list(filter(lambda x: sup2_diff[x] == min(sup2_diff.values()), sup2_diff))[0])
    #sup3
    sup3 = [points_sup[4], points_sup[5]]
    sup3_diff = dict(map(lambda a: (a['index'], a['y']), sup3))
    sup3_diff_major = (list(filter(lambda x: sup3_diff[x] == min(sup3_diff.values()), sup3_diff))[0])

    if top_diff_major == "INDEX_FINGER_TIP" and top_diff_minor == "MIDDLE_FINGER_TIP":
        if mid_diff_major == "PINKY_MCP" and mid_diff_minor == "PINKY_TIP":
            if sup1_diff_major == "THUMB_TIP" and sup2_diff_major == "MIDDLE_FINGER_MCP" and sup3_diff_major == "INDEX_FINGER_TIP":
                result['rule_match'] = True

    return result

## reconocimiento Patron L
def hand_L(data):
    result = {
        "hand_value": "L",
        "rule_match": False
    }
    points_1 = [
        data[4],
        data[12],
        data[16],
        data[20]
    ]
    points_2 = [
        data[8],
        data[10],
        data[14],
        data[18]
    ]
    points_3 = [
        data[5],
        data[9],
        data[10],
        data[12],
        data[13],
        data[14],
        data[16],
        data[17],
        data[20]
    ]
    points_4 = [
        data[4],
        data[8],
        data[12],
        data[16],
        data[20]
    ]

    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_minor = (list(filter(lambda x: p1_diff[x] == max(p1_diff.values()), p1_diff))[0])
    
    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_major = (list(filter(lambda x: p2_diff[x] == min(p2_diff.values()), p2_diff))[0])

    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p3_diff_minor = (list(filter(lambda x: p3_diff[x] == max(p3_diff.values()), p3_diff))[0])
    
    p4_diff = dict(map(lambda a: (a['index'], a['x']), points_4))
    p4_diff_major = (list(filter(lambda x: p4_diff[x] == min(p4_diff.values()), p4_diff))[0])

    if p1_diff_minor == "THUMB_TIP":
        if p2_diff_major == "INDEX_FINGER_TIP":
            if p3_diff_minor == "RING_FINGER_TIP" or p3_diff_minor == "PINKY_TIP" or p3_diff_minor == "MIDDLE_FINGER_TIP":
                if p4_diff_major == "THUMB_TIP":
                    result['rule_match'] = True

    return result

## reconocimiento Patron M
def hand_M(data):
    result = {
        "hand_value": "M",
        "rule_match": False
    }

    points_1_tmp = [
        data[5],
        data[9],
        data[13],
        data[17]
    ] 
    points_1 = [
        data[6],
        data[10],
        data[14]
    ]
    points_2 = [
        data[8],
        data[12],
        data[16]
    ]
    points_3 = [
        data[4],
        data[5],
        data[8],
        data[9],
        data[12],
        data[13],
        data[16],
        data[17],
        data[20]
    ]
    points_4_tmp = [
        data[6],
        data[10],
        data[14]
    ]
    points_4 = [
        data[8],
        data[12],
        data[16]
    ]

    p1_diff_tmp = dict(map(lambda a: (a['index'], a['y']), points_1_tmp))
    p1_diff_tmp_index_major = (list(filter(lambda x: p1_diff_tmp[x] == min(p1_diff_tmp.values()), p1_diff_tmp))[0])
    p1_diff_tmp_major = (min(p1_diff_tmp.values()))

    p1_diff = list(map(lambda a: (a['y']), points_1))
    p1_diff_major = (min(p1_diff))

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_major = (list(filter(lambda x: p2_diff[x] == min(p2_diff.values()), p2_diff))[0])
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    
    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p3_diff_major = (list(filter(lambda x: p3_diff[x] == min(p3_diff.values()), p3_diff))[0])

    p4_diff_tmp = dict(map(lambda a: (a['index'], a['y']), points_4_tmp))
    p4_diff__tmp_major = min(p4_diff_tmp.values())

    p4_diff = list(map(lambda a: (a['y']), points_4))
    p4_diff_major = min(p4_diff)

    points_p = points_1 + points_2 + points_3 + points_4
    points_p.append(data[0])
    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    p5_diff_major = (list(filter(lambda x: p5_diff[x] == min(p5_diff.values()), p5_diff))[0])
    
    if p1_diff_tmp_major < p1_diff_major:
        if p2_diff_major == "INDEX_FINGER_TIP" and (p2_diff_major == "RING_FINGER_TIP" or p2_diff_minor == "MIDDLE_FINGER_TIP"):
            if p1_diff_tmp_index_major == p3_diff_major:
                if p4_diff__tmp_major < p4_diff_major:
                    if p5_diff_major == "WRIST":
                        result['rule_match'] = True    

    return result

## reconocimiento Patron N
def hand_N(data):
    result = {
        "hand_value": "N",
        "rule_match": False
    }

    points_1 = [
        data[0],
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_2 = [
        data[4],
        data[8],
        data[12],
        data[16],
        data[20]
    ]

    points_3 = [
        data[4],
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_4 = [
        data[3],
        data[14],
        data[18]
    ]
    points_5 = [
        data[16],
        data[20]
    ]

    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_major = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("WRIST")

    p1_diff_major_value = (min(p1_diff.values()))

    p3_diff = list(map(lambda a: (a['y']), points_3))
    p3_diff_value_major = (min(p3_diff))

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    p2_diff.pop("MIDDLE_FINGER_TIP")
    p2_diff_minor2 = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])

    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_4))
    p4_diff_minor = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])

    points_p = points_5 + points_4
    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    p5_diff_minor = (list(filter(lambda x: p5_diff[x] == max(p5_diff.values()), p5_diff))[0])
    p5_diff_major = (list(filter(lambda x: p5_diff[x] == min(p5_diff.values()), p5_diff))[0])

    if p1_diff_major == "WRIST":
        if p2_diff_minor == "MIDDLE_FINGER_TIP" and p2_diff_minor2 == "INDEX_FINGER_TIP":
            if p1_diff_major_value < p3_diff_value_major:
                if p4_diff_minor == "RING_FINGER_PIP":
                    if p5_diff_major == "PINKY_TIP" or p5_diff_major == "RING_FINGER_TIP":
                        if p5_diff_minor == "PINKY_PIP" or p5_diff_minor == "RING_FINGER_PIP":
                            result['rule_match'] = True
    
    return result

## reconocimiento Patron ENIE
def hand_ENIE(data, data1):
    result = {
        "hand_value": "ENIE",
        "rule_match": False
    }

    vals = value_N(data=data)
    vals1 = value_N(data=data1)

    points_1 = None
    points_1tmp = None
    points_2 = None
    points_2tmp = None
    points_3 = None
    points_3tmp = None
    points_4 = None
    
    if vals1:
        points_1 = [
            data[5],
            data[8]
        ]
        points_1tmp = [
            data1[10],
            data1[12]
        ]
        points_2 = [
            data[8],
            data[6]
        ]
        points_2tmp = [
            data1[6],
            data1[10]
        ]
        points_3 = [
            data[0]
        ]
        points_3tmp = [
            data1[0]
        ]
        points_4 = [
            data[0],
            data[5]
        ]
    else:
        points_1 = [
            data1[5],
            data1[8]
        ]
        points_1tmp = [
            data[10],
            data[12]
        ]
        points_2 = [
            data1[8],
            data1[6]
        ]
        points_2tmp = [
            data[6],
            data[10]
        ]
        points_3 = [
            data1[0]
        ]
        points_3tmp = [
            data[0]
        ]
        points_4 = [
            data1[0],
            data1[5]
        ]

    p1_diff_tmp1_1 = ((points_1[0]['x']>= (points_1tmp[0]['x']-0.01)) or (points_1[1]['x']>= (points_1tmp[0]['x']-0.01))) or ((points_1[0]['x']>= (points_1tmp[0]['x']+0.01)) or (points_1[1]['x']>= (points_1tmp[0]['x']+0.01)))
    p1_diff_tmp1_2 = ((points_1[0]['x']<= (points_1tmp[0]['x']-0.01)) or (points_1[1]['x']<= (points_1tmp[0]['x']-0.01))) or ((points_1[0]['x']<= (points_1tmp[0]['x']+0.01)) or (points_1[1]['x']<= (points_1tmp[0]['x']+0.01)))
    p1_diff_tmp2_1 = ((points_1[0]['x']>= (points_1tmp[1]['x']-0.01)) or (points_1[1]['x']>= (points_1tmp[1]['x']-0.01))) or ((points_1[0]['x']>= (points_1tmp[1]['x']+0.01)) or (points_1[1]['x']>= (points_1tmp[1]['x']+0.01)))
    p1_diff_tmp2_2 = ((points_1[0]['x']<= (points_1tmp[1]['x']-0.01)) or (points_1[1]['x']<= (points_1tmp[1]['x']-0.01))) or ((points_1[0]['x']<= (points_1tmp[1]['x']+0.01)) or (points_1[1]['x']<= (points_1tmp[1]['x']+0.01)))
    
    p2_diff_tmp1_1 = ((points_2[0]['x']<= (points_2tmp[0]['y']-0.01)) or (points_2[1]['x']<= (points_2tmp[0]['y']-0.01))) or ((points_2[0]['y']<= (points_2tmp[0]['x']+0.01)) or (points_2[1]['y']<= (points_2tmp[0]['y']+0.01)))
    p2_diff_tmp1_2 = ((points_2[0]['x']<= (points_2tmp[0]['y']-0.01)) or (points_2[1]['x']<= (points_2tmp[0]['y']-0.01))) or ((points_2[0]['y']<= (points_2tmp[0]['x']+0.01)) or (points_2[1]['y']<= (points_2tmp[0]['y']+0.01)))
    p2_diff_tmp2_1 = ((points_2[0]['x']<= (points_2tmp[1]['y']-0.01)) or (points_2[1]['x']<= (points_2tmp[1]['y']-0.01))) or ((points_2[0]['y']<= (points_2tmp[1]['x']+0.01)) or (points_2[1]['y']<= (points_2tmp[1]['y']+0.01)))
    p2_diff_tmp2_2 = ((points_2[0]['x']<= (points_2tmp[1]['y']-0.01)) or (points_2[1]['x']<= (points_2tmp[1]['y']-0.01))) or ((points_2[0]['y']<= (points_2tmp[1]['x']+0.01)) or (points_2[1]['y']<= (points_2tmp[1]['y']+0.01)))
    
    p3_diff = points_3[0]['y'] > points_3tmp[0]['y']

    p4_diff = points_4[0]['y'] > points_4[1]['y']

    if vals or vals1:
        if (p1_diff_tmp1_1 or p1_diff_tmp1_2) and (p1_diff_tmp2_1 or p1_diff_tmp2_2):
            if (p2_diff_tmp1_1 or p2_diff_tmp1_2) and (p2_diff_tmp2_1 or p2_diff_tmp2_2):
                if p3_diff:
                    if p4_diff:
                        result['rule_match'] = True
    return result

def value_N(data):
    points_1 = [
        data[0],
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_2 = [
        data[4],
        data[8],
        data[12],
        data[16],
        data[20]
    ]

    points_3 = [
        data[4],
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_4 = [
        data[3],
        data[14],
        data[18]
    ]
    points_5 = [
        data[16],
        data[20]
    ]

    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_major = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("WRIST")

    p1_diff_major_value = (min(p1_diff.values()))

    p3_diff = list(map(lambda a: (a['y']), points_3))
    p3_diff_value_major = (min(p3_diff))

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    p2_diff.pop("MIDDLE_FINGER_TIP")
    p2_diff_minor2 = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])

    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_4))
    p4_diff_minor = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])

    points_p = points_5 + points_4
    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    p5_diff_minor = (list(filter(lambda x: p5_diff[x] == max(p5_diff.values()), p5_diff))[0])
    p5_diff_major = (list(filter(lambda x: p5_diff[x] == min(p5_diff.values()), p5_diff))[0])

    if p1_diff_major == "WRIST":
        if p2_diff_minor == "MIDDLE_FINGER_TIP" and p2_diff_minor2 == "INDEX_FINGER_TIP":
            if p1_diff_major_value < p3_diff_value_major:
                if p4_diff_minor == "RING_FINGER_PIP":
                    if p5_diff_major == "PINKY_TIP" or p5_diff_major == "RING_FINGER_TIP":
                        if p5_diff_minor == "PINKY_PIP" or p5_diff_minor == "RING_FINGER_PIP":
                            return True
    
    return False

## reconocimiento Patron O
def hand_O(data):
    result = {
        "hand_value": "O",
        "rule_match": False
    }
    points_1 = [
        data[12],
        data[16],
        data[20]
    ]
    points_1tmp = [
        data[4],
        data[8]
    ]
    points_2 = [
        data[6],
        data[10],
        data[14]
    ]
    points_3 = [
        data[4],
        data[8]
    ]
    points_4 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_5 = [
        data[2],
        data[6]
    ]
    points_5tmp = [
        data[1],
        data[5]
    ]
    points_6 = [
        data[8],
        data[20]
    ]
    points_7 = [
        data[10],
        data[14],
        data[18]
    ]
    #-------------------------
    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_major = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff_majorvalue = min(p1_diff.values())

    p1tmp_diff = dict(map(lambda a: (a['index'], a['y']), points_1tmp))
    p1tmp_diff_major = (list(filter(lambda x: p1tmp_diff[x] == min(p1tmp_diff.values()), p1tmp_diff))[0])
    p1tmp_diff_majorvalue = min(p1tmp_diff.values())

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    
    p3_difftmp1 = (points_3[0]['y'] > (points_3[1]['y']+0.01)) or (points_3[0]['y'] > (points_3[1]['y']-0.01))
    p3_difftmp2 = (points_3[0]['x'] < (points_3[1]['x']+0.01)) or (points_3[0]['x'] < (points_3[1]['x']-0.01))

    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_4))
    p4_diff_minor = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])
    
    p5_difftmp1 = (points_5[0]['x'] < (points_5tmp[0]['x']+0.01)) or (points_5[0]['x'] < (points_5tmp[0]['x']-0.01))
    p5_difftmp2 = (points_5[1]['x'] < (points_5tmp[1]['x']+0.01)) or (points_5[1]['x'] < (points_5tmp[1]['x']-0.01))

    p6_diff = (points_6[0]['y'] > (points_6[1]['y']+0.1)) or (points_6[0]['y'] > (points_6[1]['y']-0.1))

    points_p = points_1 + points_7
    p7_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
    p7_diff_major = (list(filter(lambda x: p7_diff[x] == min(p7_diff.values()), p7_diff))[0])

    if p1_diff_major == "MIDDLE_FINGER_TIP" or p1_diff_major == "PINKY_TIP" or p1_diff_major == "RING_FINGER_TIP":
        if p1tmp_diff_major == "INDEX_FINGER_TIP":
            if p1tmp_diff_majorvalue > p1_diff_majorvalue:
                if p2_diff_minor == "INDEX_FINGER_PIP":
                    if p3_difftmp1 and p3_difftmp2:
                        if p4_diff_minor == "INDEX_FINGER_MCP" or "PINKY_MCP":
                            if p5_difftmp1 and p5_difftmp2:
                                if p6_diff:
                                    if p7_diff_major == "MIDDLE_FINGER_TIP" or p7_diff_major == "PINKY_TIP" or p7_diff_major == "RING_FINGER_TIP":
                                        result['rule_match'] = True

    return result

## reconocimiento Patron P
def hand_P(data):
    result = {
        "hand_value": "P",
        "rule_match": False
    }
    points_1 = [
        data[0],
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_2 = [
        data[8],
        data[12]
    ]
    points_3 = [
        data[14],
        data[18]
    ]
    points_4 = [
        data[7],
        data[11],
        data[14],
        data[18]
    ]
    points_5 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_6 = [
        data[6],
        data[10]
    ]

    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_major = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])

    p2_diff = (points_2[0]['y'] < (points_2[1]['y']-0.01)) or (points_2[0]['y'] < (points_2[1]['y']+0.01))

    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p3_diff_major = (list(filter(lambda x: p3_diff[x] == max(p3_diff.values()), p3_diff))[0])
    
    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_4))
    p4_diff_minor = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])

    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_5))
    p5_diff_minor = (list(filter(lambda x: p5_diff[x] == max(p5_diff.values()), p5_diff))[0])
    
    p6_diff = dict(map(lambda a: (a['index'], a['y']), points_6))
    p6_diff_major = (list(filter(lambda x: p6_diff[x] == min(p6_diff.values()), p6_diff))[0])

    if p1_diff_major == "WRIST":
        if p2_diff:
            if p4_diff_minor == "MIDDLE_FINGER_DIP" or p4_diff_minor == "INDEX_FINGER_DIP":
                if p5_diff_minor == "PINKY_MCP" or p5_diff_minor == "INDEX_FINGER_MCP":
                    if p3_diff_major == "PINKY_PIP" or p6_diff_major == "INDEX_FINGER_PIP":
                        #diferencia entre falanges 
                        if abs(data[6]['y']) < abs(data[10]['y']):
                            if abs(data[6]['z']) < abs(data[10]['z']):
                                    if abs(data[4]['y']) < abs(data[20]['y']):
                                        if abs(data[16]['y']) < abs(data[8]['y']) or abs(data[16]['y']) > abs(data[12]['y']):
                                            result['rule_match'] = True

    return result

## reconocimiento Patron Q
def hand_Q(data, data1):
    result = {
        "hand_value": "Q",
        "rule_match": False
    }
    
    points_1 = None
    points_2 = None
    points_3 = None

    value_result_min = handQ_ev1(data=data)
    if value_result_min:
        points_1 = [
            data1[5],
            data1[9],
            data1[13],
            data1[17]
        ]
        points_2 = [
            data1[8],
            data1[12],
            data1[16],
            data1[20]
        ]
        points_3 = [
            data1[7],
            data1[11],
            data1[15]
        ]
    else:
        value_result_min = handQ_ev1(data=data1)
        if value_result_min:
            points_1 = [
                data[5],
                data[9],
                data[13],
                data[17]
            ]
            points_2 = [
                data[8],
                data[12],
                data[16],
                data[20]
            ]
            points_3 = [
                data[7],
                data[11],
                data[15]
            ]

    if points_1 != None and points_2 != None and points_3 != None:

        p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
        p1_diff_major = (min(p1_diff.values()))
        p1_diff_result = (data[4]['y'] > (p1_diff_major+0.01)) or (data[4]['y'] > (p1_diff_major-0.01))
        
        points_p = points_1 + points_2
        p2_diff = dict(map(lambda a: (a['index'], a['y']), points_p))
        p2_diff_major = (list(filter(lambda x: p2_diff[x] == min(p2_diff.values()), p2_diff))[0])
        
        p3_diff = (data[20]['y'] < (data[4]['y']+0.01)) or (data[20]['y'] < (data[4]['y']-0.01))
        
        p4_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
        p4_diff_major = (min(p4_diff.values()))
        p4_diff_result = (data[20]['y'] > (p4_diff_major+0.01)) or (data[20]['y'] > (p4_diff_major-0.01))

        if value_result_min:
            if p1_diff_result:
                if p2_diff_major == "MIDDLE_FINGER_TIP" or p2_diff_major == "RING_FINGER_TIP":
                    if p3_diff:
                        if p4_diff_result:
                            result['rule_match'] = True
    return result

def handQ_ev1(data):

    points_1 = [
        data[4],
        data[20]
    ]
    points_2 = [
        data[6],
        data[10],
        data[14],
        data[18]
    ]
    points_3 = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]

    p1_diff = (points_1[0]['y'] < (points_1[1]['y']+0.01)) or (points_1[0]['y'] < (points_1[1]['y']-0.01))

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_major = (min(p2_diff.values()))
    p2_diff_result = (p2_diff_major < (points_1[0]['y']+0.01)) or (p2_diff_major < (points_1[0]['y']-0.01)) 

    p3_diff_result = (p2_diff_major < (data[8]['y']+0.01)) or (p2_diff_major < (data[8]['y']-0.01)) 
    
    p4_diff_result = (p2_diff_major < (data[0]['y']+0.01)) or (p2_diff_major < (data[0]['y']-0.01)) 

    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p5_diff_major = (min(p5_diff.values()))
    p5_diff_result = (p5_diff_major < (points_1[0]['y']+0.01)) or (p5_diff_major < (points_1[0]['y']-0.01)) 

    if p1_diff:
        if p2_diff_result:
            if p3_diff_result:
                if p4_diff_result:
                    if p5_diff_result:
                        return True
    return False

## reconocimiento Patron R
def hand_R(data):
    result = {
        "hand_value": "R",
        "rule_match": False
    }
    
    points_1 = [
        data[8],
        data[12]
    ]
    points_3 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]

    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_major = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    
    p1_diff_y = (points_1[0]['y'] > (points_1[1]['y']+0.01)) or (points_1[0]['y'] > (points_1[1]['y']-0.01))
    p1_diff_z = (abs(points_1[1]['z']) > (abs(points_1[0]['z'])+0.01)) or (abs(points_1[1]['z']) > (abs(points_1[0]['z'])-0.01))
    p1_diff_x = (abs(points_1[1]['x']) - abs(points_1[0]['x'])) < 0.01

    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p3_diff_major = (min(p3_diff.values()))
    p3_diff_result = (data[20]['y'] > (p3_diff_major+0.01)) or (data[20]['y'] > (p3_diff_major-0.01))

    p4_diff_result = (data[14]['y'] < (p3_diff_major+0.01)) or (data[14]['y'] < (p3_diff_major-0.01))

    p5_diff_result = (data[4]['y'] < (data[20]['y']+0.01)) or (data[4]['y'] < (data[20]['y']-0.01))
    
    if p1_diff_major == "MIDDLE_FINGER_TIP":
        if p1_diff_y:
            if p1_diff_z:
                if p1_diff_x:
                    if p3_diff_result:
                        if p4_diff_result:
                            if p5_diff_result:
                                result['rule_match'] = True
    return result

## reconocimiento Patron S
def hand_S(data):
    result = {
        "hand_value": "S",
        "rule_match": False
    }
    

    return result

## reconocimiento Patron T
def hand_T(data, face, body):
    result = {
        "hand_value": "T",
        "rule_match": False
    }
    
    points_1 = [
        data[6],
        data[7],
        data[8]
    ]
    points_2 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_3 = [
        data[1],
        data[4],
        data[10]
    ]
    points_face = [
        face[2],
        face[1],
        face[0]
    ]
    points_body = [
        body[0],
        body[2],
        body[5]
    ]
    #----------------------------
    p1_diff_tmp1 = points_1[0]['x']-points_1[1]['x'] > 0.01
    p1_diff_tmp2 = points_1[0]['x']-points_1[2]['x'] > 0.01
    p1_diff_tmp3 = points_1[1]['x']-points_1[2]['x'] > 0.01
    p1_diff = p1_diff_tmp1 or p1_diff_tmp2 or p1_diff_tmp3

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_major = (list(filter(lambda x: p2_diff[x] == min(p2_diff.values()), p2_diff))[0])
    
    p3_diff = (points_3[1]['y'] > (points_3[2]['y']+0.01)) or (points_3[1]['y'] > (points_3[2]['y']-0.01))

    p4_diff = (points_3[0]['y'] < (points_3[2]['y']+0.01)) or (points_3[0]['y'] < (points_3[2]['y']-0.01))

    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p5_diff_major = min(p5_diff.values())

    p_diff_noise_tmp1 = (p5_diff_major < (points_face[0]['y']+0.01)) or (p5_diff_major < (points_face[0]['y']-0.01))
    p_diff_noise_tmp2 = (p5_diff_major < (points_body[0]['y']+0.01)) or (p5_diff_major < (points_body[0]['y']-0.01))
    p_diff_noise = p_diff_noise_tmp1 or p_diff_noise_tmp2
    
    p_diff_leye_tmp1 = (p5_diff_major > (points_face[1]['y']+0.01)) or (p5_diff_major > (points_face[1]['y']-0.01))
    p_diff_leye_tmp2 = (p5_diff_major > (points_body[1]['y']+0.01)) or (p5_diff_major > (points_body[1]['y']-0.01))
    p_diff_left_eye = p_diff_leye_tmp1 or p_diff_leye_tmp2

    p_diff_reye_tmp1 = (p5_diff_major > (points_face[2]['y']+0.01)) or (p5_diff_major > (points_face[2]['y']-0.01))
    p_diff_reye_tmp2 = (p5_diff_major > (points_body[2]['y']+0.01)) or (p5_diff_major > (points_body[2]['y']-0.01))
    p_diff_rigth_eye = p_diff_reye_tmp1 or p_diff_reye_tmp2
    
    if p1_diff:
        if p2_diff_major == "MIDDLE_FINGER_MCP":
            if p3_diff:
                if p4_diff:
                    if p_diff_noise:
                        if p_diff_rigth_eye or p_diff_left_eye:
                            result['rule_match'] = True
    return result

## reconocimiento Patron U
def hand_U(data):
    result = {
        "hand_value": "U",
        "rule_match": False
    }
    points_1 = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_2 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_3 = [
        data[7],
        data[10],
        data[14],
        data[19]
    ]
    #--------------------------------------
    points_p1 = points_1 + [data[4]]
    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p1_diff_major1 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("INDEX_FINGER_TIP")
    p1_diff_major2 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    
    points_p2 = points_2 + [data[4], data[12], data[16]]
    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p2_diff_minor1 = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    p2_diff.pop("RING_FINGER_TIP")
    p2_diff_minor2 = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
   
    points_p3 = points_2 + [data[4]]
    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_p3))
    p3_diff_minor = (list(filter(lambda x: p3_diff[x] == max(p3_diff.values()), p3_diff))[0])
   
    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p4_diff_minor1 = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])
    p4_diff.pop("RING_FINGER_PIP")
    p4_diff_minor2 = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])

    if p1_diff_major1  == "INDEX_FINGER_TIP" and p1_diff_major2 == "PINKY_TIP":
        if p2_diff_minor1 == "RING_FINGER_TIP" and p2_diff_minor2 == "MIDDLE_FINGER_TIP":
            if p3_diff_minor == "THUMB_TIP":
                if p4_diff_minor1 == "RING_FINGER_PIP" and p4_diff_minor2 == "MIDDLE_FINGER_PIP":
                    result['rule_match'] = True   
    return result

## reconocimiento Patron V
def hand_V(data):
    result = {
        "hand_value": "V",
        "rule_match": False
    }
    points_1 = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_2 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_3 = [
        data[4],
        data[16],
        data[20]
    ]
    points_4 = [
        data[6],
        data[10],
        data[14],
        data[18]
    ]
    #--------------------------------------
    points_p1 = points_1 + [data[4]] + points_2
    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p1_diff_major1 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("MIDDLE_FINGER_TIP")
    p1_diff_major2 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    
    points_p2 = points_4 + [data[8]]
    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
   
    points_p3 = points_2 + [data[16], data[20]]
    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_p3))
    p3_diff_minor = (list(filter(lambda x: p3_diff[x] == max(p3_diff.values()), p3_diff))[0])
   
    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p4_diff_major= (list(filter(lambda x: p4_diff[x] == min(p4_diff.values()), p4_diff))[0])

    points_p4 = points_2 + [data[4]]
    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_p4))
    p5_diff_minor1 = (list(filter(lambda x: p5_diff[x] == max(p5_diff.values()), p5_diff))[0])
    p5_diff.pop("PINKY_MCP")
    p5_diff_minor2 = (list(filter(lambda x: p5_diff[x] == max(p5_diff.values()), p5_diff))[0])

    points_p5 = [data[4], data[16], data[17], data[19], data[20]]
    p6_diff = dict(map(lambda a: (a['index'], a['y']), points_p5))
    p6_diff_major = (list(filter(lambda x: p6_diff[x] == min(p6_diff.values()), p6_diff))[0])

    points_p6 = [data[4], data[16], data[17], data[19], data[20]]
    p6_diff = dict(map(lambda a: (a['index'], a['y']), points_p6))
    p6_diff_major = (list(filter(lambda x: p6_diff[x] == min(p6_diff.values()), p6_diff))[0])

    if p1_diff_major2  == "INDEX_FINGER_TIP" and p1_diff_major1 == "MIDDLE_FINGER_TIP":
        if p2_diff_minor == "PINKY_PIP":
            if p3_diff_minor == "PINKY_TIP":
                if p4_diff_major == "THUMB_TIP":
                    if p5_diff_minor1 == "PINKY_MCP" and p5_diff_minor2 == "THUMB_TIP":
                        if p6_diff_major == "THUMB_TIP":
                            result['rule_match'] = True   
    return result

## reconocimiento Patron W
def hand_W(data):
    result = {
        "hand_value": "W",
        "rule_match": False
    }
    points_1 = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_2 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_3 = [
        data[6],
        data[10],
        data[14],
        data[18],
        data[19]
    ]
    #--------------------------------------
    points_p1 = points_1 + [data[4]] + points_2
    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p1_diff_major1 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("MIDDLE_FINGER_TIP")
    p1_diff_major2 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("RING_FINGER_TIP")
    p1_diff_major3 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    
    points_p2 = points_2 + [data[4]]
    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])

    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_3))
    p3_diff_minor = (list(filter(lambda x: p3_diff[x] == max(p3_diff.values()), p3_diff))[0])
    
    points_p3 = points_2 + [data[4], data[20]]
    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_p3))
    p4_diff_minor = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0]) 

    if p1_diff_major2  == "RING_FINGER_TIP" and p1_diff_major1 == "MIDDLE_FINGER_TIP" and p1_diff_major3 == "INDEX_FINGER_TIP":
        if p2_diff_minor == "THUMB_TIP":
            if p3_diff_minor == "PINKY_DIP":
                if p4_diff_minor == "PINKY_TIP":
                    result['rule_match'] = True   
    return result

## reconocimiento Patron X
def hand_X(data, data1):
    result = {
        "hand_value": "X",
        "rule_match": False
    }
    hand1 = handhandx(data)
    hand2 = handhandx(data1)

    if hand1 and hand2:
        result['rule_match'] = True
    return result

def handhandx(data):
    points_1 = [
        data[5],
        data[8],
        data[9],
        data[12],
        data[13],
        data[16],
        data[17],
        data[20]
    ]
    points_2 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]

    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_1))
    p1_diff_minor = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])

    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_2))
    p2_diff_major = (list(filter(lambda x: p2_diff[x] == min(p2_diff.values()), p2_diff))[0])
    p2_diff_minor = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    
    points_p1 = points_2 + [data[20]]
    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p3_diff_minor = (list(filter(lambda x: p3_diff[x] == max(p3_diff.values()), p3_diff))[0])
    
    points_p2 = points_2 + [data[16]]
    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p4_diff_minor = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])

    points_p3 = [data[8],data[4]]
    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_p3))
    p5_diff_minor = (list(filter(lambda x: p5_diff[x] == max(p5_diff.values()), p5_diff))[0])
    
    if p1_diff_minor == "INDEX_FINGER_TIP":
        if p2_diff_major == "INDEX_FINGER_MCP" or p2_diff_major == "MIDDLE_FINGER_MCP":
            if p3_diff_minor == "PINKY_TIP":
                if p4_diff_minor == "RING_FINGER_TIP":
                    if p2_diff_minor == "PINKY_MCP":
                        if p5_diff_minor == "THUMB_TIP":
                            return True
    return False

## reconocimiento Patron Y
def hand_Y(data):
    result = {
        "hand_value": "Y",
        "rule_match": False
    }
    points_1 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    
    points_p1 = points_1 + [data[4], data[8], data[12]]
    p1_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p1_diff_major1 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    p1_diff.pop("INDEX_FINGER_TIP")
    p1_diff_major2 = (list(filter(lambda x: p1_diff[x] == min(p1_diff.values()), p1_diff))[0])
    
    points_p2 = points_1 + [data[16], data[20]]
    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p2_diff_minor1 = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    p2_diff.pop("PINKY_TIP")
    p2_diff_minor2 = (list(filter(lambda x: p2_diff[x] == max(p2_diff.values()), p2_diff))[0])
    
    points_p3 = points_1 + [data[4]]
    p3_diff = dict(map(lambda a: (a['index'], a['y']), points_p3))
    p3_diff_major1 = (list(filter(lambda x: p3_diff[x] == min(p3_diff.values()), p3_diff))[0])

    points_p4 = [data[8], data[12]]
    p4_diff = dict(map(lambda a: (a['index'], abs(a['z'])), points_p4))
    p4_diff_major1 = (list(filter(lambda x: p4_diff[x] == min(p4_diff.values()), p4_diff))[0])
    p4_diff_minor1 = (list(filter(lambda x: p4_diff[x] == max(p4_diff.values()), p4_diff))[0])

    if p1_diff_major1 == "INDEX_FINGER_TIP" and p1_diff_major2 == "MIDDLE_FINGER_TIP":
        if p2_diff_minor1 == "PINKY_TIP" and p2_diff_minor2 == "RING_FINGER_TIP":
            if p3_diff_major1 == "THUMB_TIP":
                if p4_diff_major1 == "INDEX_FINGER_TIP" and p4_diff_minor1 == "MIDDLE_FINGER_TIP":
                    result['rule_match'] = True

    return result

## reconocimiento Patron Z
def hand_Z(hand, hand_direction, body):
    result = {
        "hand_value": "Z",
        "rule_match": False
    }

    hand_result = handZ(hand)
    if hand_result:
        points_2 = None        
        if hand_direction != "Left":
            points_2 = [
                body[12],
                body[14],
                body[16]
            ]
        else:
            points_2 = [
                body[11],
                body[13],
                body[15]
            ]
        
        if points_2 != None:

            p_diff2 = dict(map(lambda a: (a['index'], abs(a['y'])), points_2))
            
            #y_difference
            p1_diff_major = (list(filter(lambda x: p_diff2[x] == max(p_diff2.values()), p_diff2))[0])
            p1_diff_minor = (list(filter(lambda x: p_diff2[x] == min(p_diff2.values()), p_diff2))[0])
            
            if hand_direction == "Left":
                if p1_diff_major == "LEFT_WRIST" and p1_diff_minor == "LEFT_SHOULDER":
                        result['rule_match'] = True
            else:
                if p1_diff_major == "RIGHT_WRIST" and p1_diff_minor == "RIGHT_SHOULDER":
                    result['rule_match'] = True
                    
    return result

def handZ(data):
    points_1 = [
        data[5],
        data[9],
        data[13],
        data[17]
    ]
    points_2 = [
        data[8],
        data[12],
        data[16],
        data[20]
    ]
    points_3 = [
        data[7],
        data[11],
        data[15],
        data[19]
    ]

    p1_diff1 = list(map(lambda a: abs(a['y']), points_1))
    p1_diff2 = list(map(lambda a: abs(a['y']), points_2))
    p1_diff1_result = min(p1_diff1)
    p1_diff2_result = min(p1_diff2)

    points_p1 = points_1 + [data[0]]
    p2_diff = dict(map(lambda a: (a['index'], a['y']), points_p1))
    p2_diff_major1 = (list(filter(lambda x: p2_diff[x] == min(p2_diff.values()), p2_diff))[0])
    p2_diff1 = dict(map(lambda a: (a['index'], a['y']), points_1))
    p2_diff_major2 = (list(filter(lambda x: p2_diff1[x] == min(p2_diff1.values()), p2_diff1))[0])
    
    p3_diff = (data[4]['y'] < (data[1]['y']+0.1)) or (data[4]['y'] < (data[1]['y']-0.1))
    
    points_p2 = points_2 + [data[0]]
    p4_diff = dict(map(lambda a: (a['index'], a['y']), points_p2))
    p4_diff_major1 = (list(filter(lambda x: p4_diff[x] == min(p4_diff.values()), p4_diff))[0])
    p4_diff.pop("INDEX_FINGER_TIP")
    p4_diff_major2 = (list(filter(lambda x: p4_diff[x] == min(p4_diff.values()), p4_diff))[0])

    points_p3 = points_3 + [data[3]]
    p5_diff = dict(map(lambda a: (a['index'], a['y']), points_p3))
    p5_diff_major1 = (list(filter(lambda x: p5_diff[x] == min(p5_diff.values()), p5_diff))[0])
    p5_diff.pop("INDEX_FINGER_DIP")
    p5_diff_major2 = (list(filter(lambda x: p5_diff[x] == min(p5_diff.values()), p5_diff))[0]) 

    points_p4 = [data[4], data[5]]
    p6_diff = dict(map(lambda a: (a['index'], a['y']), points_p4))
    p6_diff_minor1 = (list(filter(lambda x: p6_diff[x] == max(p6_diff.values()), p6_diff))[0])  

    points_p5 = [data[4], data[17]]
    p7_diff = dict(map(lambda a: (a['index'], a['y']), points_p5))
    p7_diff_major1 = (list(filter(lambda x: p7_diff[x] == min(p7_diff.values()), p7_diff))[0])  

    p8_diff1 = dict(map(lambda a: (a['index'], abs(a['z'])), points_2))
    p8_diff2 = dict(map(lambda a: (a['index'], abs(a['z'])), points_3))

    #1
    tmp1 = (p8_diff1["INDEX_FINGER_TIP"] > (p8_diff2['INDEX_FINGER_DIP']+0.001)) and (p8_diff1["INDEX_FINGER_TIP"] > (p8_diff2['INDEX_FINGER_DIP']-0.001))
    #2
    tmp2 = (p8_diff1["MIDDLE_FINGER_TIP"] > (p8_diff2['MIDDLE_FINGER_DIP']+0.001)) and (p8_diff1["MIDDLE_FINGER_TIP"] > (p8_diff2['MIDDLE_FINGER_DIP']-0.001))
    #3
    tmp3 = (p8_diff1["RING_FINGER_TIP"] > (p8_diff2['RING_FINGER_DIP']+0.001)) and (p8_diff1["RING_FINGER_TIP"] > (p8_diff2['RING_FINGER_DIP']-0.001))
    #4
    tmp4 = (p8_diff1["PINKY_TIP"] > (p8_diff2['PINKY_DIP']+0.001)) and (p8_diff1["PINKY_TIP"] > (p8_diff2['PINKY_DIP']-0.001))

    if p1_diff1_result > p1_diff2_result or p1_diff1_result < p1_diff2_result:
        if p2_diff_major1 == p2_diff_major2:
            if p3_diff:
                if p4_diff_major1 == "INDEX_FINGER_TIP" and p4_diff_major2 == "MIDDLE_FINGER_TIP":
                    if p5_diff_major1 == "INDEX_FINGER_DIP" and p5_diff_major2 == "MIDDLE_FINGER_DIP":
                        if p6_diff_minor1 == "THUMB_TIP" and p7_diff_major1 == "THUMB_TIP":
                            if tmp1 and tmp2 and tmp3 and tmp4:
                                return True

    return False