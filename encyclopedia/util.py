import re
from random import randint

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def substring_search(title):
    """
    Return a list of encyclopeida entries that includes the substring.
    """
    entries = list_entries()
    sub_list = []
    for entry in entries:
        if re.search(title.lower(), entry.lower()):
            sub_list.append(entry)
    return sub_list


def no_entry_conflict(title):
    """Check if title already exist."""
    entries = list_entries()
    if title in entries:
        return False
    elif title not in entries:
        return True


def random_entry():
    """Generate random page to be displayed."""
    entries = list_entries()
    entry_number = randint(0 , len(entries)-1)
    entry = entries[entry_number]
    return entry
