import requests
import json
from tqdm import tqdm
import os
from lm_dataformat import Reader
import hashlib
from datetime import datetime
import glob

class StructureDownloader(object):

    def __init__(self, replicate_dir):
        self.replicate_dir = replicate_dir

    def _remove_old_files(self, url):
        
        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filter = os.path.join(self.replicate_dir, hash + "-*.json")
        files = glob.glob(filter)
        for f in files:
            try:
                os.remove(f)
            except:
                pass

        return

    def get_structure(self, url, hourly = True):

        now = datetime.now()
        data = None

        if hourly:
            ts = now.strftime("-%m_%d_%y_%H")
        else:
            ts = now.strftime("-%m_%d_%y")

        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        file = os.path.join(self.replicate_dir, hash + ts + ".json")

        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                return data
            except:
                pass

        self._remove_old_files(url)

        try:
            r = requests.get(url)
            if r.ok:
                data = json.loads(r.text)
        except:
            pass

        try:
            with open(file, 'w') as f:
                json.dump(data, f)
        except:
            pass
        
        return data

class Speakleash(object):

    def __init__(self, replicate_dir, lang = "pl"):
        
        self.replicate_dir = replicate_dir
        self.datasets = []

        url = "https://speakleash.space/datasets_text/"
        structure_file = "speakleash.json"

        if lang == "hr":
            url = "https://speakleash.space/datasets_text_hr/"
            structure_file = "speakleash_hr.json"

        names = StructureDownloader(replicate_dir).get_structure(url + structure_file)

        if names:      
            for item in names:
                if "name" in item:
                    self.datasets.append(SpeakleashDataset(item["name"], url, self.replicate_dir))

    def get(self, name):
        for d in self.datasets:
            if d.name == name:
                return d
        return None

class SpeakleashDataset(object):

    def __init__(self, name, url, replicate_dir):
        self.url = url
        self.name = name
        self.replicate_dir = replicate_dir
        self.manifest = self._download_manifest()

    def _download_file(self, file_name):

        ok = True
        url = self.url + self.name + ".jsonl.zst"
        file_path = os.path.join(self.replicate_dir, file_name)

        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            ok = False

        return ok

    def _download_manifest(self):

        data =StructureDownloader(self.replicate_dir).get_structure(self.url + self.name + ".manifest")

        if data:
            return data
        else:
            print("Error downloading manifest {0}".format(self.url + self.name + ".manifest"))
 
        return {}

    @property
    def characters(self):
        s = self.manifest.get("stats",{}).get("characters",0)
        return s

    @property
    def documents(self):
        s = self.manifest.get("stats",{}).get("documents",0)
        return s

    @property
    def stopwords(self):
        s = self.manifest.get("stats",{}).get("stopwords",0)
        return s

    @property
    def nouns(self):
        return self.manifest.get("stats",{}).get("nouns",[])

    @property
    def verbs(self):
        return self.manifest.get("stats",{}).get("verbs",[])

    @property
    def symbols(self):
        return self.manifest.get("stats",{}).get("symbols",[])

    @property
    def punctuations(self):
        return self.manifest.get("stats",{}).get("punctuations",[])

    @property
    def sentences(self):
        return self.manifest.get("stats",{}).get("sentences",[])

    @property
    def words(self):
        return self.manifest.get("stats",{}).get("words",[])

    @property
    def description(self):
        return self.manifest.get("description","")

    @property
    def license(self):
        return self.manifest.get("license","")

    @property
    def category(self):
        return self.manifest.get("category","")

    @property
    def sources (self):
        return self.manifest.get("sources",{})


    @property
    def jsonl_zst_file_size(self):
        return self.manifest.get("file_size",0)


    def check_file(self):

        if not os.path.exists(self.replicate_dir):
            os.makedirs(self.replicate_dir, exist_ok=True)

        file_name_json_zst = os.path.join(self.name + ".jsonl.zst")
        file_path_json_zst = os.path.join(self.replicate_dir, file_name_json_zst)
        file_json_zst_exists = False

        if os.path.exists(file_path_json_zst):
            file_size = os.path.getsize(file_path_json_zst)
            if file_size == self.jsonl_zst_file_size:
                file_json_zst_exists = True

        if not file_json_zst_exists:
            if not self._download_file(file_name_json_zst):
                return False, ""

        return True, file_path_json_zst


    @property
    def samples(self):
        data =StructureDownloader(self.replicate_dir).get_structure(self.url + self.name + ".sample", False)
        if data:
            return data
        return []

    @property
    def ext_data(self):

        ok, file_path_json_zst = self.check_file()
        if not ok:
            return None

        rdr = Reader(file_path_json_zst)
        return rdr.stream_data(get_meta=True)

    @property
    def data(self):

        ok, file_path_json_zst = self.check_file()
        if not ok:
            return None

        rdr = Reader(file_path_json_zst)
        return rdr.stream_data()

    def __repr__(self):
        return "SpeakleashDataset([{0},{1},{2}])".format(self.name, self.url, self.characters)

    def __str__(self):
        return "name: {0}, url: {1}, characters: {2}".format(self.name, self.url, self.characters)
    
