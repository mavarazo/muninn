from datetime import datetime
from dateutil.parser import parse
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

def _get_datetime(element:Element, name) -> Optional[datetime]:
    child = _get_child(element, name)
    if child is None:
        return None

    return parse(child.text.strip())

def _get_attribute_text(element: Element, name, attribute) -> Optional[str]:
    children = _get_children(element, name)
    if children is None:
        return None

    for child in children:
        if attribute in child.attrib:
            return child.attrib[attribute]

@dataclass
class Item:
    id: str
    title: str
    url: Optional[str] = None
    published: Optional[datetime] = None
    updated: Optional[datetime] = None
    summary: Optional[str] = None

@dataclass
class Channel:
    title: str
    icon: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    items: List[Item] = field(default_factory=list)

class AtomClient:

    def fetch(self, url) -> Channel:
        response = requests.request('GET', url)
        root = defused_xml_parse(response.content)
        title = _get_text(root, './feed:title')
        icon = _get_text(root, './feed:icon')
        image = _get_text(root, './feed:logo')
        url = _get_attribute_text(root, './feed:link[@rel="alternate"]', 'href')
        items = self._get_items(root)

        return Channel(
            title,
            icon,
            image,
            url,
            items
        )

    def _get_items(self, element:Element) -> List[Item]:
        items = []
        for child in _get_children(element, './feed:entry'):
            items.append(self._get_item(child))
        return items

    def _get_item(self, element:Element) -> Item:
        id = _get_text(element, './feed:id')
        title = _get_text(element, './feed:title')
        url = _get_attribute_text(element, './feed:link[@rel="alternate"]', 'href')
        published = _get_datetime(element, './feed:published')
        updated = _get_datetime(element, './feed:updated')
        summary = _get_text(element, './feed:summary')

        return Item(id, title, url, published, updated, summary)


class RssClient:

    def fetch(self, url) -> Channel:
        response = requests.request('GET', url)
        root = defused_xml_parse(response.content)
        title = _get_text(root, './channel/title')
        icon = _get_text(root, './channel/image/url')
        image = _get_text(root, './channel/image/ur')
        url = _get_text(root, './channel/url')
        items = self._get_items(root)

        return Channel(
            title,
            icon,
            image,
            url,
            items
        )

    def _get_items(self, element:Element) -> List[Item]:
        items = []
        for child in _get_children(element, './channel/item'):
            items.append(self._get_item(child))
        return items

    def _get_item(self, element:Element) -> Item:
        id = _get_text(element, './guid')
        title = _get_text(element, './title')
        url = _get_text(element, './link')
        published = _get_datetime(element, './pubDate')
        updated = _get_datetime(element, './pubDate')
        summary = _get_text(element, './description')

        return Item(id, title, url, published, updated, summary)
