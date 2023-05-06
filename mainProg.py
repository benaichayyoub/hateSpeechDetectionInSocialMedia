import os
from google.cloud import storage, pubsub_v1
from google.cloud.vision_v1 import types
import json

# Set up Pub/Sub publisher and subscriber
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Set up Google Cloud Storage client
storage_client = storage.Client()

# Set up Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient()

# Define function for detecting hate speech
def detect_hate_speech(image_path):
    # Load image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    
    # Use Google Cloud Vision to detect text in image
    response = vision_client.text_detection(image=image)
    text_annotations = response.text_annotations
    
    # Check if text contains hate speech keywords
    hate_speech_keywords = ['hate', 'racist', 'sexist',]
    for text in text_annotations:
        for keyword in hate_speech_keywords:
            if keyword in text.description.lower():
                return True
    
    return False

# Define function for deleting bad content from GCS
def delete_bad_content(object_name):
    # Delete object from GCS
    bucket_name = 'my_bucket'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.delete()

# Set up Pub/Sub subscription
subscription_path = 'projects/my_project/subscriptions/my_subscription'
def callback(message):
    # Parse message data
    message_data = json.loads(message.data.decode('utf-8'))
    object_name = message_data['name']
    
    # Download image from GCS
    bucket_name = 'my_bucket'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    image_path = '/tmp/' + object_name
    blob.download_to_filename(image_path)
    
    # Detect hate speech in image
    if detect_hate_speech(image_path):
        # Delete image from GCS if it contains hate speech
        delete_bad_content(object_name)
    else:
        # Publish message to a new topic for further processing
        new_topic_name = 'my_new_topic'
        topic_path = publisher.topic_path('my_project', new_topic_name)
        message_data = {'name': object_name}
        message_data_encoded = json.dumps(message_data).encode('utf-8')
        future = publisher.publish(topic_path, data=message_data_encoded)
    
    # Acknowledge the message
    message.ack()

# Start the Pub/Sub subscriber
subscriber.subscribe(subscription_path, callback=callback)

# Run indefinitely
while True:
    pass
