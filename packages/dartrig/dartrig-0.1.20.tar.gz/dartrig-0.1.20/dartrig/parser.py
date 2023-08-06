import json
from typing import Dict, List, Tuple
import re


class DsafNode:
    def __init__(self, dcm_no, ele_id, offset, length, dtd, text=None, id=None, rcp_no=None):
        self.dcm_no = dcm_no
        self.ele_id = ele_id
        self.offset = offset
        self.length = length
        self.dtd = dtd
        self.text = text
        self.id = id
        self.rcp_no = rcp_no

    def to_dict(self) -> Dict[str, str]:
        return {
            "dcm_no": self.dcm_no,
            "ele_id": self.ele_id,
            "offset": self.offset,
            "length": self.length,
            "dtd": self.dtd,
            "text": self.text,
            "id": self.id,
            "rcp_no": self.rcp_no
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __str__(self):
        return f"dcm_no : {self.dcm_no}, ele_id : {self.ele_id}, offset : {self.offset}, length : {self.length}, " \
               f"dtd : {self.dtd}, text : {self.text}, id : {self.id}, rcp_no : {self.rcp_no}"


def extract_node(part: str) -> DsafNode:
    """
    keys : text, id, rcpNo, dcmNo, eleId, offset, length, dtd, tocNo
    {'text': '2. 계열회사 현황(상세)', 'id': '51', 'rcpNo': '20220318000989', 'dcmNo': '8479041', 'eleId': '51', 'offset': '863891', 'length': '3225', 'dtd': 'dart3.xsd', 'tocNo': '49'}
    :param part:
    :return:
    """
    matches = re.finditer(r"\['(.*)'\]\s*=\s*\"(.*)\";", part)
    data = {}
    for matchNum, match in enumerate(matches, start=1):
        groups = match.groups()
        if len(groups) < 2:
            continue
        data[groups[0]] = groups[1]
    return DsafNode(dcm_no=data.get("dcmNo"), ele_id=data.get("eleId"), offset=data.get("offset"),
                    length=data.get("length"), dtd=data.get("dtd"), text=data.get("text"), id=data.get("id"),
                    rcp_no=data.get("rcpNo"))


def extract_nodes(html) -> List[DsafNode]:
    regex = r"var node\d{1,2}[\s\S]*?cnt\+\+;"
    matches = re.finditer(regex, html)
    return [extract_node(match.group()) for match in matches]


def extract_base_node(html) -> DsafNode:
    regex = r"viewDoc\('([\d]*)'[,\s]*'([\d]*)'[,\s]*'([\d]*)'[,\s]*'([\d]*)'[,\s]*'([\d]*)'[,\s]*'([a-zA-Z0-9.]*)'[,\s]*'.*'\);"
    matches = re.search(regex, html, re.MULTILINE)
    if matches:
        rcp_no, dcm_no, ele_id, offset, length, dtd = matches.groups()
        return DsafNode(dcm_no=dcm_no, ele_id=ele_id, offset=offset, length=length, dtd=dtd)
    else:
        return None


def parse_dsaf(html) -> Tuple[str, List[DsafNode]]:
    numbers = re.findall("\d{7}", html)
    dcm_no = numbers[2]
    base_node = extract_base_node(html)
    nodes = extract_nodes(html)
    nodes.insert(0, base_node)
    return dcm_no, nodes


def is_financial_company(company: str) -> bool:
    keywords = ["금융지주", "인베스트먼트", "증권", "금융투자"]
    postfixs = ["보험", "뱅크", "신탁", "생명"]
    
    for keyword in keywords:
        if keyword in company:
            return True
    for postfix in postfixs:
        if company.endswith(postfix):
            return True
    return False
