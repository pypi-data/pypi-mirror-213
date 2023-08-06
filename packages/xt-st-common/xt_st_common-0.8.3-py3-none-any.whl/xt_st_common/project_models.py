import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

from bson import ObjectId
from pydantic import BaseModel, Field

from xt_st_common.config import StreamlitBaseSettings
from xt_st_common.storage import FileRef, storage_client

settings = StreamlitBaseSettings()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ProjectState(str, Enum):
    PROJECT_DELETE_CONFIRM = "proj_delete_confirm"
    PROJECT_TO_DELETE = "proj_delete"
    PROJECT_SUCCESS_MESSAGE = "proj_success_message"
    PROJECT_WARNING_MESSAGE = "proj_warning_message"

    FOLDER_TO_DELETE = "upload_delete_folder"
    FOLDER_ADDED = "upload_folder_added"

    UPLOAD_SUCCESS_MESSAGE = "upload_success_message"
    UPLOAD_WARNING_MESSAGE = "upload_warning_message"
    UPLOAD_DELETE_CONFIRM = "upload_delete_confirm"

    FILE_DELETE_CONFIRM = "file_delete_confirm"
    FILE_TO_DELETE = "file_to_delete"
    FILE_SUCCESS_MESSAGE = "file_success_message"
    FILE_WARNING_MESSAGE = "file_warning_message"

    # FILE_MANAGER_UPLOAD = "file_manager_upload_file"
    FILE_MANAGER_REPLACE_FILE = "file_manager_replace_file"


class Project(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")  # noqa: A003
    name: str
    description: str = ""
    public: bool = False
    application: str = settings.APP_NAME
    files: List[FileRef] = []
    folders: List[str] = []
    owner: str = ""
    users: List[str] = []  # Users with access to this project

    def get_users_string(self):
        return ",".join(self.users)

    def get_folders_map(self):
        fol_dict = {"/": "Project Root"}
        for folder in self.folders:
            parts = folder.strip("/").split("/")
            fol_dict[folder] = " - ".join(parts)
        return fol_dict

    def get_folder_path(self, folder):
        return f"{str(self.id)}/{self.name}/{folder}".strip("/")

    def get_files_in_folder(self, folder: str, include_subfolders=True, extensions=None, null_option=None):
        _files: Dict[str, Union[None, FileRef]] = {} if null_option is None else {null_option: None}

        path = self.get_folder_path(folder)
        for file in self.files:
            if path in file.path:
                file_path = file.path.removeprefix(path).strip("/")
                if (include_subfolders or file_path.find("/") <= 0) and (
                    extensions is None or str(Path(file.name).suffix.lower()) in extensions
                ):
                    _files[file_path] = file

        return _files

    def populate_node(self, _dict, part, parts):
        if part not in _dict:
            _dict[part] = {}

        if parts:
            self.populate_node(_dict[part], parts[0], parts[1:])

    def populate_children(self, _dict, key, children, path):
        if child_dict := _dict[key]:
            for child_key in child_dict:
                new_children = None
                new_path = f"{path}/{child_key}"
                if child_dict[child_key]:
                    new_children = []
                    self.populate_children(child_dict, child_key, new_children, new_path)
                children.append(
                    {
                        "label": child_key,
                        "value": f"{path}/{child_key}",
                        "children": new_children,
                    }
                )

    def get_file_tree(self):
        main_dict = {}
        full_list = (
            [file.path.removeprefix(self.get_folder_path("")).strip("/") for file in self.files] if self.files else []
        )
        if self.folders:
            full_list.extend(self.folders)
        if not full_list:
            return []
        for folder in full_list:
            parts = folder.split("/")
            self.populate_node(main_dict, parts[0], parts[1:])

        nodes = []
        for key in main_dict:
            children = None
            if main_dict[key]:
                children = []
                self.populate_children(main_dict, key, children, key)
            nodes.append({"label": key, "value": key, "children": children})

        return nodes

    def add_replace_file(self, data_file, folder: str, filename: str, content_type=None) -> FileRef:
        path = f"{self.get_folder_path(folder)}/{filename}".strip("/")
        return self.add_replace_file_by_path(data_file, path, content_type=content_type)

    def add_replace_file_by_path(self, data_file, path: str, content_type=None) -> FileRef:
        file_ref = storage_client().write_file(path, data_file, content_type)
        replaced = False
        for idx, file in enumerate(self.files):
            if file.path == path:
                self.files[idx] = file_ref
                replaced = True
                break
        if not replaced:
            self.files.append(file_ref)

        return file_ref

    def move_file_to_path(self, file: FileRef, new_path: str) -> FileRef:
        new_file_ref = storage_client().move_file(file.path, new_path, file.content_type, file.size_bytes)
        index = self.files.index(file)
        self.files[index] = new_file_ref
        return new_file_ref

    def delete_file(self, file: FileRef):
        storage_client().delete_file(file.path)
        try:
            self.files.remove(file)
        except ValueError:
            logging.warning(f"File {file.path} didn't exist and couldn't be deleted.")

    def add_folders(self, folders_string: str):
        folders = set(self.folders)
        new_folders = folders_string.split(",")
        count = 0
        for folder in new_folders:
            folder = folder.strip().replace(" ", "_").strip("/")
            folder_parts = folder.split("/")
            for idx, part in enumerate(folder_parts):
                if idx == 0:
                    folders.add(f"{part}")
                else:
                    folders.add(f"{'/'.join(folder_parts[:idx+1])}")
                count += 1
        try:
            self.folders = list(folders)
        except AttributeError:
            logging.warning("Weird odmatic error, attempting to ignore")

        return count

    def delete_folder(self, folder: str):
        try:
            folder_path = self.get_folder_path(folder)
            self.folders.remove(folder)
            for file in [x for x in self.files if folder_path in x.path]:
                self.delete_file(file)
        except ValueError:
            logging.warning(f"Folder {folder} didn't exist and couldn't be deleted.")

    class Config:
        anystr_strip_whitespace = True
        # collection = "project"
