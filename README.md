
# Speech Hate Detection with Google Cloud Services

This project demonstrates the use of various Google Cloud services to detect hate speech in images and delete them from Google Cloud Storage (GCS) in real-time. The project uses Google Cloud Vision to extract text from images stored in GCS, and uses a custom algorithm to detect hate speech in the extracted text. If the image contains hate speech, it is deleted from GCS. Otherwise, a message is published to a new topic for further processing.

## Getting Started

### Prerequisites

Before running this project, you need to have the following:

- A Google Cloud Platform (GCP) account with billing enabled
- A GCS bucket with images that you want to process
- A Pub/Sub subscription to receive messages when new images are uploaded to the GCS bucket

### Installation

To run this project, follow these steps:

1. Clone this repository to your local machine
2. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your GCP service account key file
3. Update the following variables in the `main.py` file with your own values:
   - `subscription_path`: The Pub/Sub subscription path
   - `bucket_name`: The GCS bucket name
   - `hate_speech_keywords`: A list of keywords to use for detecting hate speech
   - `new_topic_name`: The name of the new Pub/Sub topic to publish messages to
4. Run `python main.py` to start the subscriber

### Usage

When a new image is uploaded to the GCS bucket, the subscriber will receive a message and the following will happen:

1. The image will be downloaded from GCS to a temporary file
2. Google Cloud Vision will be used to extract text from the image
3. The custom algorithm will check the extracted text for the presence of hate speech keywords
4. If the image contains hate speech, it will be deleted from GCS
5. Otherwise, a message will be published to the new topic for further processing

