
# MOdel Test Harness (Moth)

Simple way to interrogate your AI model from a separate testing application

# Quickstart

`moth server <folder path>`

`moth client`

Simplest possible classification model client
```
from moth import Moth
from moth.message import ImagePromptMsg, ClassificationResultMsg, HandshakeTaskTypes

moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION)

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    return ClassificationResultMsg(prompt_id=prompt.id, class_name="cat") # Most pictures are cat pictures 

moth.run()
```

Simplest possible object detection model client
```
from moth import Moth
from moth.message import ImagePromptMsg, ObjectDetectionResultMsg, ObjectDetectionResult, HandshakeTaskTypes

moth = Moth("my-ai", task_type=HandshakeTaskTypes.OBJECT_DETECTION)

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    # Make a list of ObjectDetectionResults
    l = []
    l.append(ObjectDetectionResult(0, 0, 50, 50, class_name="cat", class_index=0, confidence=0.9))
    l.append(ObjectDetectionResult(10, 10, 50, 35, class_name="dog", class_index=1, confidence=0.1))
    return ObjectDetectionResultMsg(prompt_id=prompt.id, object_detection_results=l)
 

moth.run()
```
