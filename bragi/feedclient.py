from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional
from xml.etree.ElementTree import Element

import requests
from defusedxml.ElementTree import fromstring as defused_xml_parse

NAMESPACE = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'feed': 'http://www.w3.org/2005/Atom'
}

def _get_child(element: Element, name) -> Optional[Element]:
    return element.find(name, namespaces=NAMESPACE)

def _get_children(element: Element, name) -> List[Element]:
    return element.findall(name, namespaces=NAMESPACE)

def _get_text(element: Element, name) -> Optional[str]:
    child = _get_child(element, name)
    if child is None:
        return None

    return child.text.strip()

def _get_attribute_text(element: Element, name, attribute) -> Optional[str]:
    children = _get_children(element, name)
    if children is None:
        return None

    for child in children:
        if attribute in child.attrib:
            return child.attrib[attribute]

@dataclass
class AtomEntry:
    id: str
    title: str
    url: Optional[str] = None
    published: Optional[datetime] = None
    updated: Optional[datetime] = None
    summary: Optional[str] = None

@dataclass
class AtomFeed:
    title: str
    icon: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    entries: List[AtomEntry] = field(default_factory=list)

class AtomClient:

    def fetch(self, url) -> AtomFeed:
        response = requests.request('GET', url)
        root = defused_xml_parse(response.content)
        title = _get_text(root, './feed:title')
        icon = _get_text(root, './feed:icon')
        image = _get_text(root, './feed:logo')
        url = _get_attribute_text(root, './feed:link[@rel="alternate"]', 'href')
        entries = self.get_entries(root)

        return AtomFeed(
            title,
            icon,
            image,
            url,
            entries
        )

    def get_entries(self, element:Element) -> List[AtomEntry]:
        entries = []
        for child in _get_children(element, './feed:entry'):
            entries.append(self.get_entry(child))
        return entries

    def get_entry(self, element:Element) -> AtomEntry:
        id = _get_text(element, './feed:id')
        title = _get_text(element, './feed:title')
        url = _get_attribute_text(element, './feed:link[@rel="alternate"]', 'href')
        published = _get_text(element, './feed:published')
        updated = _get_text(element, './feed:updated')
        summary = _get_text(element, './feed:summary')

        return AtomEntry(id, title, url, published, updated, summary)
