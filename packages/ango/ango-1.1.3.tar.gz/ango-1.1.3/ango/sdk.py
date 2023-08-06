import datetime
import mimetypes
import urllib.request
import uuid
import zipfile
from enum import Enum
from typing import List

import requests
import json

from tqdm import tqdm

from ango.models.enums import TaskStatus
from ango.models.label_category import ToolCategory, ClassificationCategory, RelationCategory


class SDK:

    def __init__(self, api_key, host="https://api.ango.ai"):
        self.api_key = api_key
        self.host = host
        self.session = requests.Session()

    def list_projects(self, page=1, limit=10):
        url = "%s/v2/listProjects?page=%s&limit=%s" % (self.host, page, limit)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = self.session.get(url, headers=headers, data=payload)
        return response.json()

    def get_project(self, project_id):
        url = "%s/v2/project/%s" % (self.host, project_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = self.session.get(url, headers=headers, data=payload)
        return response.json()

    def get_tasks(self, project_id: str, page: int = 1, limit: int = 10, status: str = None, batches: List[str] = None):
        url = "%s/v2/project/%s/tasks?page=%s&limit=%s" % (self.host, project_id, page, limit)
        if status:
            url += "&status[eq]=%s" % status
        if batches:
            tags = self.__getTags(project_id, batches)
            url += "&tag=%s" % json.dumps(tags)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = self.session.get(url, headers=headers, data=payload)
        return response.json()

    def get_task(self, task_id):
        url = "%s/v2/task/%s" % (self.host, task_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = self.session.get(url, headers=headers, data=payload)
        return response.json()

    def set_task_status(self, task_id: str, status: TaskStatus):
        url = "%s/v2/task/%s/status" % (self.host, task_id)

        payload = {
            'status': status.value
        }
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def assign_task(self, task, userid=None, email=None):
        url = "%s/v2/task/assign" % self.host

        payload = {"task": task}
        if userid:
            payload["user"] = userid
        elif email:
            payload["username"] = email
        else:
            return Exception("userid or email required!")

        payload = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = self.session.post(url, headers=headers, data=payload)
        return response.json()

    def _get_upload_url(self, fname: str):
        url = "%s/v2/getUploadUrl?name=%s" % (self.host, fname)
        headers = {
            'apikey': self.api_key
        }
        r = self.session.get(url, headers=headers).json()
        url = r["data"]["uploadUrl"]
        return url

    def __getTags(self, project_id, tags):
        ptags = self.get_batches(project_id)
        resp = []
        for t1 in tags:
            tag_exist = False
            for t2 in ptags:
                if t1 == t2["_id"] or t1 == t2["name"]:
                    resp.append(t2["_id"])
                    tag_exist = True
            if not tag_exist:
                raise Exception("Tag %s not found" % t1)
        return resp

    def __check_integration(self, project_id, integration_id):
        resp = self.get_integrations(project_id)
        integrations_list = resp['data']['integrations']
        integration_exists = False
        for t1 in integrations_list:
            if '_id' in t1 and t1['_id'] == integration_id:
                integration_exists = True
        return integration_exists

    def upload_files(self, project_id: str, file_paths: List, integration_id: str = None, batches: List[str] = None):
        if integration_id and not self.__check_integration(project_id, integration_id):
            raise "Integration ID is Invalid!"
        assets = []
        for path in tqdm(file_paths):
            uid = uuid.uuid4().hex
            data = ""
            external_id = ""
            if isinstance(path, str):
                data = path
                external_id = uid
            else:
                data = path.get("data")
                external_id = path.get("externalId", uid)
            file = open(data, 'rb')
            fname = uid + '.' + file.name.split('.')[-1]
            url = self._get_upload_url(fname)
            requests.put(url, data=file.read())
            asset = {'data': url.split('?')[0], 'externalId': external_id}
            if integration_id:
                asset['storage'] = integration_id
            assets.append(asset)

        url = "%s/v2/project/%s/cloud" % (self.host, project_id)
        if batches:
            tags = self.__getTags(project_id, batches)
            url += "?tags=%s" % json.dumps(tags)

        payload = json.dumps({"assets": assets})
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = self.session.post(url, headers=headers, data=payload)
        return response.json()

    def upload_files_cloud(self, project_id: str, assets, integration_id: str = None, batches: List[str] = None):
        if integration_id and not self.__check_integration(project_id, integration_id):
            raise "Integration ID is Invalid!"
        url = "%s/v2/project/%s/cloud" % (self.host, project_id)

        tagMap = {}
        ptags = self.get_batches(project_id)
        for tag in ptags:
            tagMap[tag['name']] = tag['_id']

        def switch_tags_names_with_ids(tags):
            resp = []
            for t1 in tags:
                tag_exist = False
                for t2 in ptags:
                    if t1 == t2["_id"] or t1 == t2["name"]:
                        resp.append(t2["_id"])
                        tag_exist = True
                if not tag_exist:
                    raise Exception("Tag %s not found" % t1)
            return resp

        for a in assets:
            if integration_id:
                a['storage'] = integration_id
            if "batches" in a:
                a['tags'] = switch_tags_names_with_ids(a['batches'])

        if batches:
            tags = switch_tags_names_with_ids(batches)
            url += "?tags=%s" % json.dumps(tags)

        payload = json.dumps({"assets": assets})
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = self.session.post(url, headers=headers, data=payload)
        return response.json()

    def create_issue(self, task_id, content, position):
        url = "%s/v2/issues" % self.host

        payload = {
            "content": content,
            "labelTask": str(task_id),
            "position": str(position)
        }
        headers = {
            'apikey': self.api_key
        }

        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def get_assets(self, project_id, asset_id=None, external_id=None, page=1, limit=10):
        url = "%s/v2/project/%s/assets?page=%s&limit=%s" % (self.host, project_id, page, limit)
        if asset_id:
            url += "?_id=" % asset_id
        if external_id:
            url += "?externalId=" % external_id

        headers = {
            'apikey': self.api_key
        }
        response = self.session.get(url, headers=headers)
        return response.json()

    def set_asset_priority(self, project_id: str, priority: int, external_id: str = None, asset_id: str = None):
        if external_id is None and asset_id is None:
            return Exception("External id or Assest Id should be provided!")

        url = "%s/v2/priority/%s" % (self.host, project_id)

        payload = {
            "priority": priority,
            "externalId": external_id,
            "assetId": asset_id
        }
        headers = {
            'apikey': self.api_key
        }

        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def create_attachment(self, project_id, attachments):

        url = "%s/v2/attachments" % self.host

        payload = {
            "project": project_id,
            "attachments": attachments
        }
        headers = {
            'apikey': self.api_key
        }

        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def export(self, project_id: str, assignees: List[str] = None, completed_at: List[datetime.datetime] = None,
               updated_at: List[datetime.datetime] = None, batches: List[str] = None):

        url = "%s/v2/export?project=%s&labeledAt=true&reviewedAt=true&completion=true&totalDuration=true&skip=true" \
              "&reviewConf=true&format=json&labelDuration=true&assetStatus=true&consensus=true&batches=true" \
              "&updateInfo=true&issues=true&mask=true&boxImage=true&annotationMetadata=true&benchmark=true" \
              "&labelStatus=true&segmentationPoints=true&sendEmail=false&doNotNotify=true" % (self.host, project_id)
        if type(assignees) == list and len(assignees) > 0:
            url += "&assignee=" + json.dumps(assignees)
        if type(batches) == list and len(batches) > 0:
            url += "&tag=" + json.dumps(batches)
        if type(completed_at) == list and len(completed_at) == 2:
            if completed_at[0] is not None:
                url += "&completedAt[gt]=" + completed_at[0].isoformat()
            if completed_at[1] is not None:
                url += "&completedAt[lt]=" + completed_at[1].isoformat()
        if type(updated_at) == list and len(updated_at) == 2:
            if updated_at[0] is not None:
                url += "&updatedAt[gt]=" + updated_at[0].isoformat()
            if completed_at[1] is not None:
                url += "&updatedAt[lt]=" + updated_at[1].isoformat()

        headers = {
            'apikey': self.api_key
        }
        response = self.session.get(url, headers=headers)
        link = response.json()['data']['exportPath']
        filehandle, _ = urllib.request.urlretrieve(link)
        zip_file_object = zipfile.ZipFile(filehandle, 'r')
        first_file = zip_file_object.namelist()[0]
        file = zip_file_object.open(first_file)
        content = file.read()
        json_response = json.loads(content)
        return json_response

    def create_label_set(self, project_id: str, tools: List[ToolCategory] = [],
                         classifications: List[ClassificationCategory] = [],
                         relations: List[RelationCategory] = []):

        url = "%s/v2/project/%s" % (self.host, project_id)
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "categorySchema": {
                "tools": list(map(lambda t: t.toDict(), tools)),
                "classifications": list(map(lambda t: t.toDict(), classifications)),
                "relations": list(map(lambda t: t.toDict(), relations))
            }
        }

        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def import_labels(self, project_id: str, labels: List[dict]):

        url = "%s/v2/import/labels" % self.host
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "project": project_id,
            "jsonContent": labels
        }

        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def get_integrations(self, id: str = None):
        url = "%s/v2/integrations" % self.host
        headers = {
            'apikey': self.api_key
        }
        response = self.session.get(url, headers=headers)
        if id:
            for i in response.json().get('data', {}).get("integrations", []):
                if i["_id"] == id:
                    return i
        return response.json()

    def get_batches(self, project_id: str):
        p = self.get_project(project_id)
        if 'data' in p:
            return p.get("data", {}).get("project", {}).get("tags", [])
        else:
            raise Exception('Invalid Project Id!')

    def create_batch(self, project_id: str, batch_name: str):
        url = "%s/v2/batches/%s" % (self.host, project_id)
        tags = self.get_batches(project_id)
        headers = {
            'apikey': self.api_key
        }
        tags.append({
            'name': batch_name
        })
        payload = {
            "tags": tags,
        }
        response = self.session.post(url, headers=headers, json=payload)
        return response.json().get("data", []).get("project", []).get("tags", [])

    def assign_batches(self, project_id: str, asset_ids: List[str], batches: List[str]):
        url = "%s/v2/assignBatches" % self.host
        tags = self.__getTags(project_id, batches)
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "assets": asset_ids,
            "tags": tags,
        }
        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def create_project(self, name, description=""):
        url = "%s/v2/project" % self.host
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "name": name,
            "description": description,
        }
        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def create_webhook(self, webhook_url: str, project_id: str, secret: str, types: List[str]):
        url = "%s/v2/webhook" % self.host
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "url": webhook_url,
            "types": types,
            "secret": secret,
            "project": project_id
        }
        response = self.session.post(url, headers=headers, json=payload)
        return response.json()

    def _annotate(self, task_id: str, answer: dict):
        url = "%s/v2/annotate/%s?nextStage=true" % (self.host, task_id)
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "answer": answer,
            "duration": 0
        }
        response = self.session.post(url, headers=headers, json=payload)
        return response.status_code == 200
