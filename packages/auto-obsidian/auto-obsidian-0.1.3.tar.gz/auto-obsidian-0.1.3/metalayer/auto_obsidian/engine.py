import re
from metalayer.chatgpt import complete_async
from metalayer.chatgpt.utils import fill_messages, retry_on_exception


choose_node_prompt = """\
\"""
Application: {0}
Window Title: {1}
Summary:
{2}
Activity:
{3}
Screen Content:
{4}
\"""
Based on the given information, which folder would be the best fit for the user's activity? \
Please choose from the following options or suggest a new one by selecting the "New folder option":

{5}

Respond with only the number of your answer\
"""
@retry_on_exception(retries=3)
async def choose_node(parent_node, app, title, summary, activity, info):
    if len(parent_node.children) == 0 or parent_node.content is not None:
        return None
    options = parent_node.list_children() + f'\n{len(parent_node.children)+1}. New folder'
    messages = fill_messages(None, choose_node_prompt, app, title, summary, activity, info, options)
    response = await complete_async(messages, temperature=0, stop=['.', ' ', '\n'])
    # find first integer in response
    match = re.search(r'\d+', response)
    if match is None:
        return None
    child_idx = int(match.group()) - 1
    if child_idx < 0 or child_idx >= len(parent_node.children):
        return None
    return parent_node.children[child_idx]


merge_node_prompt = """\
\"""
{0}
\"""

\"""
{1}
\"""

Merge the above two markdown files into one. Use markdown format! Use headings and lists when necessary.\
"""
@retry_on_exception(retries=3)
async def merge_nodes(node1, node2):
    messages = fill_messages(None, merge_node_prompt, node1.content, node2.content)
    response = await complete_async(messages, temperature=0)
    merged_content = response.strip('"')
    merged_node = node1.copy()
    merged_node.content = merged_content
    return merged_node


create_node_system_prompt = """\
DO NOT acknowledge the existence of a user or their screen. \
Just put educational content into the notes.\
"""

create_node_prompt = """\
\"""
{0}
\"""

I currently have a "{1}" window titled "{2}" open on my computer. Above is all the text currently visible on my screen. \
I need to document the information currently on my screen in a markdown file under the following folder on my computer:

{3}

Write the relevant information on my screen in a markdown note, using headings and lists when necessary. \
This should be an independent note that can be placed in the above folder.

VERY IMPORTANT: DO NOT mention open tabs, bookmarks, files, folders, buttons, or any other system elements \
from the user's screen. DO NOT acknowledge the existence of a user or their screen. \
If you include this information you fail the task.\
"""
@retry_on_exception(retries=3)
async def create_node(node, ocr_lines, app, title):
    messages = fill_messages(create_node_system_prompt, create_node_prompt, ocr_lines, app, title, str(node.parent))
    response = await complete_async(messages, temperature=0)
    node.content = response.strip('"')
    return node


choose_write_location_prompt = """\
\"""
{0}
\"""
Given the markdown note above, determine which of the following folders the note should be added to:

{1}

Choose one of the numbered options by only responding with a number.\
"""
@retry_on_exception(retries=3)
async def choose_node_to_update(node):
    parent_node = node.parent
    N = len(parent_node.children)
    options = parent_node.list_children()
    options += f'\n{N+1}. New folder in the {parent_node.get_path()} directory'
    options += f'\n{N+2}. Does not belong in this directory'

    messages = fill_messages(None, choose_write_location_prompt, node.content, options)
    response = await complete_async(messages, temperature=0, stop=['.', ' ', '\n'])
    # find first integer in response
    match = re.search(r'\d+', response)
    if match is None:
        return None
    child_idx = int(match.group()) - 1

    if 0 <= child_idx < len(parent_node.children):
        return parent_node.children[child_idx]
    elif child_idx == len(parent_node.children):
        return node
    return None

name_and_description_prompt = """\
\"""
{0}
\"""

Give the above markdown note a name and a 1-3 sentence description. \
The name should only include alphanumeric characters and spaces. Format your response like:
Name | Description\
"""
@retry_on_exception(retries=3)
async def add_name_and_description(node, ignore_name=False, ignore_description=False):
    messages = fill_messages(None, name_and_description_prompt, node.content)
    response = await complete_async(messages, temperature=0)
    name, description, *_ = response.strip('"').split('|')
    name = name.strip()
    description = description.strip()
    if not ignore_name:
        node.name = name
    if not ignore_description:
        node.description = description
    return node


split_node_prompt = """\
\"""
{0}
\"""
I need to move some information from this note into a new one. Can you choose a range of headings that could be moved into an independent. Respond with one range of heading indices to remove formatted like this:

[a-b]\
"""
@retry_on_exception(retries=3)
async def split_node(node):
    # Number the headings
    content = node.content
    lines = []
    heading_inds = []
    for i, line in enumerate(content.split('\n')):
        if line.startswith('#'):
            heading_inds.append(i)
            line = f'[{len(heading_inds)}] ' + line
        lines.append(line)
    heading_inds.append(len(lines))
    numbered_lines = '\n'.join(lines)

    messages = fill_messages(None, split_node_prompt, numbered_lines)
    response = await complete_async(messages, temperature=0)
    match = re.search(r'\[\d+-\d+]', response)
    if match is None:
        return None
    start, end = match.group().strip('[]').split('-')
    start, end = int(start)-1, int(end)-1
    if start < 0 or end >= len(heading_inds) or start >= end:
        return None

    # Convert heading indices to line indices
    start_line = heading_inds[start]
    end_line = heading_inds[end+1]

    # Split the node
    new_node = node.copy()
    new_node.content = '\n'.join(lines[start_line:end_line])
    node.content = '\n'.join(lines[:start_line] + lines[end_line:])
    return node, new_node

make_folders_prompt = """\
I have the following folder:

{0}

It already has the following folders:

{1}

Can you generate 3-5 NEW (distinct from those listed above) folders that could be used to organize my notes in the above folder? Use this format:

Folder Name - Description of what to put into these folders. Should be 1-3 sentences. DO NOT add any other list formatting to your response.\
"""

def remove_line_numbering(s):
    lines = []
    for line in s.split('\n'):
        match = re.search('[a-zA-Z]', line)
        if match is None:
            continue
        i = match.start()
        lines.append(line[i:])
    return '\n'.join(lines)

@retry_on_exception(retries=3)
async def make_folders(node):
    subfolders= [f'{child.name} - {child.description}' for child in node.children if child.content is None]
    if len(subfolders) == 0:
        subfolders = ['NONE - directory is empty']
    else:
        subfolders = '\n'.join(subfolders)

    messages = fill_messages(None, make_folders_prompt, node.get_path(), subfolders)
    response = await complete_async(messages, temperature=0)
    response = remove_line_numbering(response)
    folders = []
    for line in response.split("\n"):
        if len(line) > 0:
            name, *description = line.split(" - ")
            name = name.strip()
            description = ' - '.join(description).strip()
            folders.append((name, description))
    return folders
