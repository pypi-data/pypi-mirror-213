
import os
import json
import requests
from requests.adapters import HTTPAdapter, Retry
from pathlib import Path
from live4safe_commons.liveness_status_enum import LivenessStatusEnum
from live4safe_commons.logger_app import get_logger


from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.aio._eventprocessor.partition_context import PartitionContext
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


EVENT_HUB_CONNECTION_STR = os.getenv('EVENT_HUB_CONNECTION_STR')
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
BLOB_CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME')


class Connection:
    video_path = None
    port = None
    choosen_method = None
    connection = None
    channel = None
    current_method = None

    def __init__(self, cho_method, cur_method):
        self.logger = get_logger(cho_method)
        self.logger.info(f'Initiating {cho_method}...')
        self.choosen_method = cho_method

        try:
            Path("./videos").mkdir(parents=True, exist_ok=True)
            self.current_method = cur_method

        except SystemExit:
            os._exit(0)
  
    def callback(self, message):
        self.logger.info("Method: {}".format(self.choosen_method))
        self.logger.info("Analysing Video: {}".format(message))
        answer = {}
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[492, 500, 502, 503, 504 ])
        session = requests.Session()
        session.mount('https://',HTTPAdapter(max_retries=retries))
        session.mount('http://',HTTPAdapter(max_retries=retries))
        url_callback = f'{message.get("callback")}{message.get("liveness_id")}'
        try:
            # Download video file from video_path in Google Storage
            self.logger.info("Downloading video from Bucket")
            pth = "./videos/" + str(message["video_path"]).split("/")[-1]
            header = {message.get("token_type"): message.get("token")}
            r = session.get(message["video_path"], allow_redirects=True)
            if r.ok:
                with open(pth, "wb") as target:
                    target.write(r.content)
                # PROCESS VIDEO                
                session.put(url=url_callback,
                    headers=header,
                    json={
                        f"{self.choosen_method}_status": 
                        LivenessStatusEnum.processing.name}
                )
                answer = self.current_method.analyse_video(pth)
                
                self.logger.info("Finishing Liveness method.")
                Path(pth).unlink()
                session.put(url=url_callback,
                               headers=header,
                               json=answer)
            else:
                self.logger.error(
                    "Video %s was not found on server, aborting processing...",
                    str(message["video_path"]).split("/")[-1],
                )
                session.put(
                    url=url_callback,
                    headers=header,
                    json={
                        f"{self.choosen_method}_status":
                        LivenessStatusEnum.error.name},
                )

        except Exception as ex:
            self.logger.exception(
                "An exception ocurred when trying to process video: %s",
                ex
            )
            session.put(
                url=url_callback,
                headers=header,
                json={
                    f"{self.choosen_method}_status":
                    LivenessStatusEnum.execption.name},
            )

    async def run(self):
        checkpoint_store = BlobCheckpointStore.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME
        )
        client = EventHubConsumerClient.from_connection_string(
            EVENT_HUB_CONNECTION_STR,
            consumer_group='$Default',
            eventhub_name=self.choosen_method,
            retry_total=5,
            checkpoint_store=checkpoint_store
        )
        async with client:
            await client.receive(on_event=self.on_event)
                
    
    async def on_event(self,partition_context:PartitionContext, event:EventData):

            body = event.body_as_json(encoding='UTF-8')
            self.callback(body)
            await partition_context.update_checkpoint(event)