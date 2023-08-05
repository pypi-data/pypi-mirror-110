## Some example on how to publish messages for testing purposes


### 1. Load Slack Chat history
``gcloud pubsub topics publish local-background-worker  --message='{ "job_type": "LoadChatHistoryJob", "data": { "user_id": "5d9db09e3710ae3ec4b4592f" } }'``

### 2. Restart BOTS
``gcloud pubsub topics publish local-background-worker --message='{ "job_type": "RestartBotsJob", "data": { "bots": [] }}'``

### 3. Update BOTS credentials
``gcloud pubsub topics publish local-background-worker --message='{ "job_type": "BotsCredentialsUpdateJob", "data": { "bot_name": "mitrixdataprocessing" }}'``

### 4. Update User BOT credentials
``gcloud pubsub topics publish local-background-worker --message='{ "job_type": "UserBotsCredentialsUpdateJob", "data": { "user_id": "5d9db09e3710ae3ec4b4592f", "bot_name": "mitrixdataprocessing" }}'``

### 5. Update user slack profile
``gcloud pubsub topics publish local-background-worker --message='{ "job_type": "UpdateUserSlackProfileJob", "data": { "user_id": "5d9db09e3710ae3ec4b4592f", "bot_name": "mitrixdataprocessing" }}'``

