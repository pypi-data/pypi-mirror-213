from huggingface_hub import hf_hub_download
from huggingface_hub import login
from huggingface_hub import HfApi


login()
api = HfApi()

api.create_repo(repo_id="super-cool-model", token="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")


api.upload_file(
    path_or_fileobj="/path/to/local/folder/README.md",
    path_in_repo="README.md",
    repo_id="username/test-dataset",
    repo_type="dataset",
)

api.upload_folder(
    folder_path="/path/to/local/space",
    repo_id="username/my-cool-space",
    repo_type="space",
)

hf_hub_download(repo_id="lysandre/arxiv-nlp", 
                filename="config.json")
                # revision="4d33b01d79672f27f001f6abade33f22d993b151")