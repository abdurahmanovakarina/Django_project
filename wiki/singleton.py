from .models import Section


class SectionTree:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.tree = cls.get_tree()
        return cls._instance

    @classmethod
    def get_tree(cls):
        sections = Section.objects.all()
        tree = []
        for section in sections:
            if not section.parent:
                tree.append(cls.get_section_info(section))
        return tree

    @classmethod
    def get_section_info(cls, section):
        info = {
            "section": section,
            "subsections": [],
            "articles": list(section.articles.all()),
        }
        for subsection in section.section_set.all():
            info["subsections"].append(cls.get_section_info(subsection))
        return info

    @classmethod
    def update_tree(cls):
        cls._instance.tree = cls.get_tree()
