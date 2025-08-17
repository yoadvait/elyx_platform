import xml.etree.ElementTree as ET
from typing import List, Dict, Any

class XMLEpisodeParser:
    def __init__(self, xml_content: str):
        self.xml_content = xml_content

    def parse_episodes(self) -> List[Dict[str, Any]]:
        """
        Parses the XML content and returns a list of episodes.
        """
        root = ET.fromstring(self.xml_content)

        episodes = []
        for episode_elem in root.findall('episode'):
            episode = {
                "name": episode_elem.get('name'),
                "duration": episode_elem.get('duration'),
                "context": episode_elem.find('context').text,
                "messages": []
            }
            for msg_elem in episode_elem.findall('.//message'):
                message = {
                    "sender": msg_elem.get('sender'),
                    "day": msg_elem.get('day'),
                    "text": msg_elem.text
                }
                episode["messages"].append(message)
            episodes.append(episode)

        return episodes
