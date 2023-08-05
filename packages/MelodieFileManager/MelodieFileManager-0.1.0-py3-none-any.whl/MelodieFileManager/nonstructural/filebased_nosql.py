import json  
import os
import shutil
from typing import Callable, Dict, List  
class TableDesc:
    def __init__(self, name: str, type: str='singlefile') -> None:
        self.name = name
        self.type = type
        assert type in {"singlefile", 'folder'}

class MelodieNoSQLDB:
    def __init__(self, root: str, tables: List[TableDesc], json_indent=2, ensure_ascii=False) -> None:
        assert os.path.exists(root), FileNotFoundError(root)
        self.root = root
        self.ensure_ascii = ensure_ascii
        self.json_indent = json_indent
        self.tables: Dict[str, TableDesc] = {table.name:table for table in  tables}

    def _get_folder(self, table_name: str):
        # 构建存储记录的文件夹路径  
        folder_path = os.path.join(self.root, table_name)
        
        # 创建文件夹（如果不存在）  
        if not os.path.exists(folder_path):  
            os.makedirs(folder_path)  
        return folder_path
    
    def _get_file(self, table_name: str):
        file = os.path.join(self.root, table_name + ".json")
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('[]')
        return file

    def clear_table(self, table_name:str):
        if self.tables[table_name].type == "singlefile":
            with open(self._get_file(table_name), "w") as f:
                f.write("[]")
        else:
            shutil.rmtree(self._get_folder(table_name))
            assert os.path.exists(self._get_folder(table_name))

    def submit_record(self, table_name: str, record: Dict):  
        if self.tables[table_name].type == "singlefile":
            file = self._get_file(table_name)
            with open(file, "r") as f:  
                l = json.load(f)
            l.append(record)
            with open(file, "w") as f:  
                json.dump(l, f, indent=self.json_indent, ensure_ascii=self.ensure_ascii)
        else:
            # 获取当前时间戳的哈希值作为文件名  
            file_name = hash(str(record))  
            folder_path = self._get_folder(table_name)
            # 构建记录文件的路径  
            file_path = os.path.join(folder_path, f"{file_name}.json")  
            
            # 将记录写入文件  
            with open(file_path, "w") as file:  
                json.dump(record, file, indent=self.json_indent, ensure_ascii=self.ensure_ascii)
    
    def submit_records(self, table_name: str, records: List[Dict]):  
        if self.tables[table_name].type == "singlefile":
            file = self._get_file(table_name)
            with open(file, "r") as f:  
                l: List = json.load(f)
            l.extend(records)
            with open(file, "w") as f:  
                json.dump(l, f, indent= self.json_indent, ensure_ascii=self.ensure_ascii)
        else:
            for record in records:
                # 获取当前时间戳的哈希值作为文件名  
                file_name = hash(str(record))  
                folder_path = self._get_folder(table_name)
                # 构建记录文件的路径  
                file_path = os.path.join(folder_path, f"{file_name}.json")  
                
                # 将记录写入文件  
                with open(file_path, "w") as file:  
                    json.dump(record, file, indent=self.json_indent, ensure_ascii=self.ensure_ascii)

    def list_tables(self)->List[str]:
        return self.tables.keys()

    def _single_file_based_find_one(self, table_name: str, query: Callable[[Dict], bool])->Dict:
        with open(self._get_file(table_name), 'r') as f:
            data = json.load(f)
        for d in data:
            if query(d):
                return d
            
    def _single_file_based_find_all(self, table_name: str, query: Callable[[Dict], bool])->Dict:
        with open(self._get_file(table_name), 'r') as f:
            data = json.load(f)
        res = []
        for d in data:
            if query(d):
                res.append(d)
        return res

    def _folder_based_find_one(self, table_name: str, query: Callable[[Dict], bool]) -> Dict: 
        folder_path = self._get_folder(table_name)
        
        # 获取文件夹中所有的JSON文件  
        json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]  
        
        # 遍历JSON文件并返回所有记录的JSON字符串  
        for json_file in json_files:  
            file_path = os.path.join(folder_path, json_file)  
            with open(file_path, "r") as file:  
                data = json.load(file)  
                if query(data):
                    return data
        return None
    
    def _folder_based_find_all(self, table_name: str, query: Callable[[Dict], bool]) -> List[Dict]: 
        folder_path = self._get_folder(table_name)
        
        # 获取文件夹中所有的JSON文件  
        json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]  
        all = []
        # 遍历JSON文件并返回所有记录的JSON字符串  
        for json_file in json_files:  
            file_path = os.path.join(folder_path, json_file)  
            with open(file_path, "r") as file:  
                data = json.load(file)  
                if query(data):
                    all.append(data)
        return all
    
    def find_one(self, table_name: str, query: Callable[[Dict], bool])->Dict:
        if self.tables[table_name].type == "singlefile":
            return self._single_file_based_find_one(table_name, query)
        else:
            return self._folder_based_find_one(table_name, query)

    def find_all(self, table_name: str, query: Callable[[Dict], bool])->List[Dict]:
        if self.tables[table_name].type == "singlefile":
            return self._single_file_based_find_all(table_name, query)
        else:
            return self._folder_based_find_all(table_name, query)