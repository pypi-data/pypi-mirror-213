import cv2
import json
import mediapipe as mp
from jw_lensegua.lensegua import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_detection
mp_body = mp.solutions.pose
tracking = Jw_Lensegua()

##method
def recog_model_handler(results, model_object, image):
  image_height, image_width, _ = image.shape
  isheadness_model = results.multi_handedness
  index_now = 0

  for hand_landmarks in results.multi_hand_landmarks:
    if index_now > 1:
      break
    model_object['model_hand'][index_now]['position'] = isheadness_model[index_now].classification[0].label
    model_object['model_hand'][index_now]['index'].append({
            "index": "WRIST",
            "x": hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
            "y": hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
            "z": hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z,
            "width": image_width,
            "height": image_height,
            "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * image_width,
            "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height
          })
    model_object['model_hand'][index_now]['index'].append({
      "index": "THUMB_CMC",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "THUMB_MCP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "THUMB_IP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "THUMB_TIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "INDEX_FINGER_MCP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "INDEX_FINGER_PIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "INDEX_FINGER_DIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "INDEX_FINGER_TIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "MIDDLE_FINGER_MCP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "MIDDLE_FINGER_PIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "MIDDLE_FINGER_DIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "MIDDLE_FINGER_TIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "RING_FINGER_MCP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "RING_FINGER_PIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "RING_FINGER_DIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "RING_FINGER_TIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "PINKY_MCP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "PINKY_PIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "PINKY_DIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height
    })

    model_object['model_hand'][index_now]['index'].append({
      "index": "PINKY_TIP",
      "x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x,
      "y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y,
      "z": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].z,
      "width": image_width,
      "height": image_height,
      "transform_x": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * image_width,
      "transform_y": hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height
    })

    index_now = index_now + 1
  
  if index_now < 2:
    model_object['model_hand'][index_now]['position'] = 'Right' if  model_object['model_hand'][index_now-1]['position'] != 'Right' else 'Left'

def recog_model_handler_face(results, model_object, image):
  image_height, image_width, _ = image.shape
  for detection in results.detections:
    model_object['model_face'].append({
            "index": "RIGHT_EYE",
            "x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EYE).x,
            "y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EYE).y,
            "width": image_width,
            "height": image_height,
            "transform_x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EYE).x * image_width,
            "transform_y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EYE).y * image_height
          })
    model_object['model_face'].append({
            "index": "LEFT_EYE",
            "x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EYE).x,
            "y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EYE).y,
            "width": image_width,
            "height": image_height,
            "transform_x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EYE).x * image_width,
            "transform_y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EYE).y * image_height
          })
    model_object['model_face'].append({
            "index": "NOSE_TIP",
            "x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.NOSE_TIP).x,
            "y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.NOSE_TIP).y,
            "width": image_width,
            "height": image_height,
            "transform_x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.NOSE_TIP).x * image_width,
            "transform_y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.NOSE_TIP).y * image_height
          })
    model_object['model_face'].append({
            "index": "MOUTH_CENTER",
            "x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.MOUTH_CENTER).x,
            "y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.MOUTH_CENTER).y,
            "width": image_width,
            "height": image_height,
            "transform_x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.MOUTH_CENTER).x * image_width,
            "transform_y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.MOUTH_CENTER).y * image_height
          })
    model_object['model_face'].append({
            "index": "RIGHT_EAR_TRAGION",
            "x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EAR_TRAGION).x,
            "y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EAR_TRAGION).y,
            "width": image_width,
            "height": image_height,
            "transform_x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EAR_TRAGION).x * image_width,
            "transform_y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.RIGHT_EAR_TRAGION).y * image_height
          })
    model_object['model_face'].append({
            "index": "LEFT_EAR_TRAGION",
            "x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EAR_TRAGION).x,
            "y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EAR_TRAGION).y,
            "width": image_width,
            "height": image_height,
            "transform_x": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EAR_TRAGION).x * image_width,
            "transform_y": mp_face.get_key_point(detection, mp_face.FaceKeyPoint.LEFT_EAR_TRAGION).y * image_height
          })

def recog_model_handler_body(results, model_object, image):
    image_height, image_width, _ = image.shape
    model_object['model_body'].append({
            "index": "NOSE",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.NOSE].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.NOSE].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.NOSE].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.NOSE].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.NOSE].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_EYE_INNER",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_INNER].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_INNER].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_INNER].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_INNER].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_INNER].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_EYE",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_EYE_OUTER",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_OUTER].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_OUTER].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_OUTER].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_OUTER].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EYE_OUTER].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_EYE_INNER",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_INNER].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_INNER].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_INNER].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_INNER].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_INNER].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_EYE",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_EYE_OUTER",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_OUTER].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_OUTER].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_OUTER].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_OUTER].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EYE_OUTER].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_EAR",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EAR].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EAR].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EAR].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EAR].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_EAR].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_EAR",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EAR].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EAR].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EAR].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EAR].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_EAR].y * image_height
          })
    model_object['model_body'].append({
            "index": "MOUTH_LEFT",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_LEFT].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_LEFT].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_LEFT].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_LEFT].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_LEFT].y * image_height
          })
    model_object['model_body'].append({
            "index": "MOUTH_RIGHT",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_RIGHT].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_RIGHT].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_RIGHT].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_RIGHT].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.MOUTH_RIGHT].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_SHOULDER",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_SHOULDER].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_SHOULDER].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_SHOULDER].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_SHOULDER].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_SHOULDER].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_SHOULDER",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_SHOULDER].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_SHOULDER].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_SHOULDER].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_SHOULDER].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_SHOULDER].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_ELBOW",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_ELBOW].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_ELBOW].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_ELBOW].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_ELBOW].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_ELBOW].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_ELBOW",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_ELBOW].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_ELBOW].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_ELBOW].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_ELBOW].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_ELBOW].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_WRIST",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_WRIST].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_WRIST].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_WRIST].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_WRIST].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_WRIST].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_WRIST",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_WRIST].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_WRIST].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_WRIST].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_WRIST].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_WRIST].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_PINKY",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_PINKY].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_PINKY].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_PINKY].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_PINKY].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_PINKY].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_PINKY",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_PINKY].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_PINKY].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_PINKY].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_PINKY].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_PINKY].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_INDEX",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_INDEX].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_INDEX].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_INDEX].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_INDEX].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_INDEX].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_INDEX",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_INDEX].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_INDEX].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_INDEX].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_INDEX].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_INDEX].y * image_height
          })
    model_object['model_body'].append({
            "index": "LEFT_THUMB",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_THUMB].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_THUMB].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_THUMB].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_THUMB].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.LEFT_THUMB].y * image_height
          })
    model_object['model_body'].append({
            "index": "RIGHT_THUMB",
            "x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_THUMB].x,
            "y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_THUMB].y,
            "z": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_THUMB].z,
            "width": image_width,
            "height": image_height,
            "transform_x": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_THUMB].x * image_width,
            "transform_y": results.pose_landmarks.landmark[mp_body.PoseLandmark.RIGHT_THUMB].y * image_height
          })


cap = cv2.VideoCapture(0)
with mp_face.FaceDetection(
    model_selection=1, min_detection_confidence=0.6) as face_detection:

  with mp_hands.Hands(
      static_image_mode=False,
      max_num_hands=2,
      model_complexity=0,
      min_detection_confidence=0.60) as hands:

    with mp_body.Pose(
      static_image_mode=False,
      model_complexity=2,
      enable_segmentation=True,
      min_detection_confidence=0.6) as pose:
      while cap.isOpened():
        model_object = {
          "model_body": [],
          "model_face": [],
          "model_hand": [
            {
              "position": "left",
              "index": []
            },
            {
              "position": "rigth",
              "index": []
            }
          ]
        }
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results_face  = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        results_hands = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        results_body  = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        value_recognized = ""

        if results_face.detections and  results_hands.multi_hand_landmarks and results_body.pose_landmarks:
          
          recog_model_handler(results=results_hands, model_object=model_object, image=image)
          recog_model_handler_face(results=results_face, model_object=model_object, image=image)
          recog_model_handler_body(results=results_body, model_object=model_object, image=image)
          
          print("---------------------------")
          tracking.set_model(model_object)
          tracking.recognition()
          value = (tracking.get_resultscoincidence())
          print(value)
          if len(value)>0:
              for i in range(len(value)):
                value_recognized = value_recognized + value[i]['hand_value']
                if i+1 < len(value):
                    value_recognized = value_recognized + ","
          tracking.destroy()
          print("---------------------------")
          if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
              mp_drawing.draw_landmarks(
                  image,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  mp_drawing_styles.get_default_hand_landmarks_style(),
                  mp_drawing_styles.get_default_hand_connections_style())
              
          if results_face.detections:
            for detection in results_face.detections:
              mp_drawing.draw_detection(image, detection)

          mp_drawing.draw_landmarks(
            image,
            results_body.pose_landmarks,
            mp_body.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        # Flip the image horizontally for a selfie-view display.
        image_height, image_width, _ = image.shape
        value_text = value_recognized if value_recognized != None else ""
        cv2.putText(image, value_text, (10, image_height-40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 5)
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
          break
cap.release()