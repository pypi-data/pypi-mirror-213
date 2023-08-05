import asyncio
import copy
import os
import shutil

import parse

from metalayer.auto_obsidian import engine

MAX_FILE_CHARS = 5000
MAKE_FOLDER_THRESH = 6
MARKDOWN_FORMAT = """\
---
description: {0}
---
{1}\
"""

node_parser = parse.compile(MARKDOWN_FORMAT)


class Node():
    
    def __init__(self, name=None, description=None, content=None):
        self.name = name
        self.description = description
        self.content = content
        self.children = []
        self.parent = None
        self.lock = asyncio.Lock()

    def add_children(self, *children):
        for child in children:
            self.children.append(child)
            child.parent = self
    
    def get_parents(self):
        parents = []
        curr = self.parent
        while curr is not None:
            parents.append(curr)
            curr = curr.parent
        return parents
    
    def list_children(self):
        lines = []
        for i, child in enumerate(self.children):
            lines.append(f'{i+1}. ' + str(child))
        return '\n'.join(lines)
    
    def get_path(self):
        return '/'.join([p.name for p in self.get_parents()[::-1] + [self]])
    
    def to_markdown(self, md_path):
        node_text = MARKDOWN_FORMAT.format(self.description, self.content)
        os.makedirs(os.path.dirname(md_path), exist_ok=True)
        with open(md_path, 'w') as f:
            f.write(node_text)

    def copy(self):
        return copy.copy(self)

    def __repr__(self):
        return self.get_path() + ' - ' + self.description
    

class Graph():

    def __init__(self, vault_dir):
        self.root = Node('')
        self.vault_dir = vault_dir
        self._load_graph()

    def _load_graph(self, root=None):
        if root is None:
            root = self.root

        children = []
        root_dir = os.path.join(self.vault_dir, root.get_path().strip('/'))
        for fname in os.listdir(root_dir):
            if fname.startswith('.'):
                continue

            if fname == '_description.md':
                with open(root_dir + '/_description.md', 'r') as f:
                    root.description = f.read()
                continue

            node = Node()
            node_path = os.path.join(root_dir, fname)

            if os.path.isfile(node_path) and node_path.endswith('.md'):
                node.name = fname[:-3]
                with open(node_path, 'r') as f:
                    file_content = f.read()
                    description, content = node_parser.parse(file_content)
                    node.description = description
                    node.content = content
                root.add_children(node)
             
            elif os.path.isdir(node_path):
                node.name = fname
                children.append(node)
        
        root.add_children(*children)
        for child in children:
            self._load_graph(child)

    def save_graph(self, root=None, save_path=None):
        if root is None:
            root = self.root
        if save_path is None:
            save_path = self.vault_dir

        if root is not self.root:
            root_path = os.path.join(save_path, root.get_path().strip('/'))
            os.makedirs(root_path, exist_ok=True)
            if root.description is not None:
                with open(root_path + '/_description.md', 'w') as f:
                    f.write(root.description)

        for node in root.children:
            node_path = os.path.join(save_path, node.get_path().strip('/'))

            if node.content is not None:
                node.to_markdown(node_path + '.md')
                continue

            self.save_graph(node, save_path)

    async def insert_knowledge(self, app, title, summary, activity, info, ocr_results):
        node_choice = self.root
        depth = 0
        print('Selecting node')
        while True:
            no_subdirs = all(c.content is not None for c in node_choice.children)
            if no_subdirs:
                break

            async with node_choice.lock:
                new_node_choice = await engine.choose_node(node_choice, app, title, summary, activity, '\n'.join(info))

            if new_node_choice is None or new_node_choice.content is not None:
                break
            depth += 1
            if depth >= 10:
                print('[WARNING]: Depth exceeded, not inserting')
                return
            node_choice = new_node_choice

        if node_choice is self.root:
            print('[WARNING]: Selected root node, not inserting')
            return
        print(f'Selected node {node_choice.get_path()}')

        new_node = Node()
        new_node.parent = node_choice
        print('Creating node')
        ocr_lines = '\n'.join(t for b, t in ocr_results)
        new_node = await engine.create_node(new_node, ocr_lines, app, title)
        print(f'Created node under {node_choice.get_path()}')

        while True:
            print('Choosing node to update')
            async with node_choice.lock:
                node_to_update = await engine.choose_node_to_update(new_node)
            if node_to_update is None:
                print('No knowledge found to index, node not created')
                return
            if node_to_update.content is not None:
                break
            new_node.parent = node_to_update
            if len(node_to_update.children) == 0:
                break

        print('Updating node')
        if node_to_update is new_node:
            created, node_to_update = await self.insert_node(node_to_update)
            overwrite_ok = not created
        else:
            node_to_update = await self.append_to_node(node_to_update, new_node)
            overwrite_ok = True

        if len(node_to_update.content) > MAX_FILE_CHARS:
            res = await engine.split_node(node_to_update)
            if res is not None:
                node_to_update, new_node = res
                created, new_node = await self.insert_node(new_node)
                self.save_node(new_node, overwrite=not created)
                print(f'Split node {node_to_update.get_path()} into {new_node.get_path()}')

        self.save_node(node_to_update, overwrite=overwrite_ok)


    async def insert_node(self, node):
        parent = node.parent
        print('Adding name and description')
        node = await engine.add_name_and_description(node)
        print(f'Added name and description to node {node.get_path()}')
        print(f'Inserting node {node.get_path()} into {parent.get_path()}')
        created = False
        async with parent.lock:
            child_names = [c.name for c in parent.children]
            if node.name in child_names:
                print('[WARNING]: Tried to create node that already exists, appending instead')
                node_to_update = parent.children[child_names.index(node.name)]
                node = await self.append_to_node(node_to_update, node)
            else:
                parent.add_children(node)
                print(f'Created node {node.get_path()}')
                created = True

        if len(parent.children) >= MAKE_FOLDER_THRESH:
            await self.make_folders(parent)
        return created, node

    async def append_to_node(self, node, node_to_append):
        async with node.lock:
            print(f'Appending to node {node.get_path()}')
            node = await engine.merge_nodes(node, node_to_append)
            node = await engine.add_name_and_description(node, ignore_name=True)
            print(f'Appended to node {node.get_path()}')
            return node

    def save_node(self, node, overwrite=False):
        save_path = os.path.join(self.vault_dir, node.get_path().strip('/') + '.md')
        if not overwrite and os.path.exists(save_path):
            print('[WARNING]: Tried to overwrite existing node, not saving')
        elif os.path.dirname(save_path) == self.vault_dir:
            print('[WARNING]: Tried to save to root directory, not saving')
        else:
            node.to_markdown(save_path)

    async def make_folders(self, parent_node):
        print(f'Making folders for {parent_node.get_path()}')
        new_folders = await engine.make_folders(parent_node)
        new_nodes = [Node(name, desc) for name, desc in new_folders]

        async with parent_node.lock:
            updated_nodes = set()
            for node in parent_node.children:
                if node.content is None:
                    continue
                # insert node into one of the new folders
                async with node.lock:
                    # make dummy parent with only new folders as children
                    dummy_parent = parent_node.copy()
                    dummy_parent.children = new_nodes
                    node.parent = dummy_parent
                    node_to_update = await engine.choose_node_to_update(node)
                    if node_to_update in new_nodes:
                        node_to_update.add_children(node)
                        updated_nodes.add(node_to_update)
                    else:
                        node.parent = parent_node

            parent_node.children = [n for n in parent_node.children if n.parent is parent_node]
            parent_node.add_children(*updated_nodes)
            shutil.rmtree(os.path.join(self.vault_dir, parent_node.get_path().strip('/')))
            self.save_graph(root=parent_node)

            print(f'Made {len(updated_nodes)} new folders for {parent_node.get_path()}')

    
if __name__ == '__main__':
    g = Graph('/Users/iyevenko/Knowledge Repo')
    # g.save_graph(save_path='/Users/iyevenko/Knowledge Repo Copy')
    asyncio.run(g.make_folders(g.root.children[1]))
