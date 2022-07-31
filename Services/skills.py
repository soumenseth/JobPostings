# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from collections import defaultdict
import itertools
from pathlib import Path

import srsly
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.language import Language
from spacy.pipeline import EntityRuler


class SkillsExtractor:
    """Extracts skills from text using SpaCy's EntityRuler Component"""

    def __init__(self, nlp: Language, data_path: Path = Path("Data")):
        self.nlp = nlp
        self.data_path = data_path
        self.skills = self._get_skills()

        patterns = self._build_patterns(self.skills)
        extra_patterns = self._get_extra_skill_patterns()
        # ruler = EntityRuler(nlp, overwrite_ents=True)
        ruler = self.nlp.add_pipe("entity_ruler", name="skills_ruler")
        ruler.add_patterns(itertools.chain(patterns, extra_patterns))

    def _get_skills(self):
        """Query skills from skills collection"""
        skills_path = self.data_path / "skills.json"
        skills = srsly.read_json(skills_path)
        return skills

    def _get_extra_skill_patterns(self):
        """Load extra user added skill patterns"""
        extra_patterns_path = self.data_path / "extra_skill_patterns.jsonl"
        extra_skill_patterns = srsly.read_jsonl(extra_patterns_path)
        return extra_skill_patterns

    def _skill_pattern(self, skill: str, split_token: str = None):
        """Create a single skill pattern"""
        pattern = []
        if split_token:
            split = skill.split(split_token)
        else:
            split = skill.split()
        for b in split:
            if b:
                if b.upper() == skill:
                    pattern.append({"TEXT": b})
                else:
                    pattern.append({"LOWER": b.lower()})

        return pattern

    def _build_patterns(self, skills: list, create: bool = False):
        """Build all matcher patterns"""
        patterns_path = self.data_path / "skill_patterns.jsonl"
        if not patterns_path.exists() or create:
            """Build up lists of spacy token patterns for matcher"""
            patterns = []
            split_tokens = [".", "/", "-"]

            for skill_id, skill_info in skills.items():
                aliases = skill_info['aliases']
                sources = skill_info['sources']
                skill_names = set()
                for al in aliases:
                    skill_names.add(al)
                for source in sources:
                    if "displayName" in source:
                        skill_names.add(source["displayName"])

                for name in skill_names:
                    if name.upper() == name:
                        skill_name = name
                    else:
                        skill_name = name.lower().strip()

                    if skill_name not in STOP_WORDS:
                        pattern = self._skill_pattern(skill_name)

                        if pattern:
                            label = f"SKILL|{skill_id}"
                            patterns.append({"label": label, "pattern": pattern})

                            for t in split_tokens:
                                if t in skill_name:
                                    patterns.append(
                                        {
                                            "label": label,
                                            "pattern": self._skill_pattern(
                                                skill_name, t
                                            ),
                                        }
                                    )

            srsly.write_jsonl(patterns_path, patterns)
            return patterns
        else:
            patterns = srsly.read_jsonl(patterns_path)
            return patterns

    def extract_skills(self, text: str):
        """Extract skills from text unstructured text"""
        doc = self.nlp(text)
        found_skills = defaultdict(lambda: defaultdict(list))

        for ent in doc.ents:
            if "|" in ent.label_:
                ent_label, skill_id = ent.label_.split("|")
                if ent_label == "SKILL" and skill_id:
                    found_skills[skill_id]["matches"].append(
                        {
                            "start": ent.start_char,
                            "end": ent.end_char,
                            "label": ent_label,
                            "text": ent.text,
                        }
                    )
                    try:
                        skill_info = self.skills[skill_id]
                        sources = skill_info['sources']

                        # Some sources have better Skill Descriptions than others.
                        # This is a simple heuristic for cascading through the sources 
                        # to pick the best description available per skill
                        main_source = sources[0]
                        for source in sources:
                            if source["sourceName"] == "Github Topics":
                                main_source = source
                                break
                            elif source["sourceName"] == "Microsoft Academic Topics":
                                main_source = source
                                break
                            elif source["sourceName"] == "Stackshare Skills":
                                main_source = source
                                break
                    except KeyError:
                        # This happens when a pattern defined in data/extra_skill_patterns.jsonl
                        # is matched. The skill is not added to data/skills.json so there's no
                        # extra metadata about the skill from an established source.
                        sources = []
                        main_source = {
                            "displayName": ent.text,
                            "shortDescription": "",
                            "longDescription": ""
                        }

                    keys = ["displayName", "shortDescription", "longDescription"]
                    for k in keys:
                        found_skills[skill_id][k] = main_source[k]
                    found_skills[skill_id]["sources"] = [
                        {"name": s["sourceName"], "url": s["url"]} for s in sources
                    ]
        return found_skills
