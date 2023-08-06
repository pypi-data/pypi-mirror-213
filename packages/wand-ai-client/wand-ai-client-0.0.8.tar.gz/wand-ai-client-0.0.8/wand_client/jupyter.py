from typing import Any, List, Optional

import requests
from IPython.display import display
from ipywidgets import FileUpload
from rich.progress import Progress

from wand_client.cli.formatters import RichProgressListener
from wand_client.sdk.core import Model, WandClient


def chat(model_id: str, client: WandClient) -> None:
    chat_session = client.models.start_chat(model_id)

    print(f"You are talking to model with id {model_id}. Type 'exit' to close.")

    while True:
        prompt_text = input("> ")
        if prompt_text == "exit":
            return
        print("Generating answer...")
        print("\n")
        resp = chat_session.ask(prompt_text)
        print(resp)


class TrainByFileManager:
    def __init__(self, client: WandClient) -> None:
        self._client = client
        self._upload = FileUpload()
        self.model: Optional[Model] = None

    def display_picker(self) -> None:
        display(self._upload)

    def do_train(self, _: Any) -> None:
        value = self._upload.value
        if isinstance(value, tuple):
            if len(value) != 1:
                return
            item = value[0]
        elif isinstance(value, dict):
            if len(value) != 1:
                return
            item = list(value.values())[0]
        else:
            print(f"Got invalid result from FileUpload widget: {value}")
            return

        item_name = item.get(
            "name", item.get("metadata", {}).get("name", "name-unknown")
        )
        item_content = item["content"]

        print(f"Got a file with name {item_name}")
        print("Uploading...")
        file_res = self._client.source.create_file(item_name)
        requests.put(file_res.upload_url, data=item_content)
        print("Uploaded, file source id: ", file_res.source.id)

        print("Starting training")

        with Progress() as progress:
            self.model = self._client.models.train(
                [file_res.source.id], RichProgressListener(progress)
            )

        print(f"Training completed. Model id = {self.model.id}")


class TrainFromUrlsManager:
    def __init__(self, client: WandClient) -> None:
        self._client = client
        self.model: Optional[Model] = None

    def start_training(self, urls: List[str], max_crawl_pages: int = 10000) -> None:
        print("Creating web source...")
        source = self._client.source.create_web(urls, max_crawl_pages=max_crawl_pages)
        print(f"Web source created, id = {source.id}")

        print("Starting training")

        with Progress() as progress:
            self.model = self._client.models.train(
                [source.id], RichProgressListener(progress)
            )

        print(f"Training completed. Model id = {self.model.id}")
