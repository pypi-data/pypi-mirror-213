import asyncio
import json
import os

from tqdm import tqdm
from glob import glob

from metalayer import CAPTURE_DIR, ACTIVITY_LOG_DIR
CAPTURE_DIR = CAPTURE_DIR.replace('data', 'brian_data')
ACTIVITY_LOG_DIR = ACTIVITY_LOG_DIR.replace('data', 'brian_data')

from metalayer.auto_obsidian.graph import Node
from metalayer.auto_obsidian.engine import append_to_node, complete_node, choose_node

def load_data():
    metalayer_data = []
    for timestamp in sorted(os.listdir(ACTIVITY_LOG_DIR)):
        for log_path in glob(ACTIVITY_LOG_DIR + timestamp + '/*.json'):
            entry = {}
            with open(log_path, 'r') as f:
                log = json.load(f)
                entry.update(log)

            fname = os.path.basename(log_path)
            capture_path = os.path.join(CAPTURE_DIR, timestamp, fname)
            with open(capture_path, 'r') as f:
                m = json.load(f)
                entry['ocr_results'] = m.pop('ocr_results')
                entry['metadata'] = m

            metalayer_data.append(entry)
    return metalayer_data


def init_graph(vault_path):
    root = Node('', 'The root node of my knowledge graph', None)
    globe = Node('Globe', "My knowledge capture and visualization startup named Globe. Here I hold all my conversations and lessons I've learned while building it.", None)
    engineering = Node('Engineering', "Everything I've learned about engineering from school, my internships and my personal research. This is a big ontology of my knowledge, like my personal wiki.", None)
    ideas = Node('Ideas', "All my ideas for projects, startups, and research. Only the ones good enough to write down or tell someone about. ", None)
    root.add_children(globe, engineering, ideas)

    conversations = Node('Conversations', "All of my conversations about globe, grouped by who I was talking to.", None)
    lessons = Node('Lessons', "All of my lessons learned while building globe (startups, software, learning etc.). No grouping here, just a list of nodes.", None)
    globe.add_children(conversations, lessons)

    startups_hard = Node('Why startups are hard', "All the reasons I've realized why startups are hard", "")
    lessons.add_children(startups_hard)

    make_vault_dirs(root, vault_path)

    return root


def make_vault_dirs(root, vault_path):
    for node in root.children:
        if node.content is not None:
            node_path = os.path.join(vault_path, node.name + '.md')
            node.to_markdown(node_path)
            continue

        node_path = os.path.join(vault_path, node.name)
        os.makedirs(node_path, exist_ok=True)
        with open(node_path + '/_description.md', 'w') as f:
            f.write(node.description)
        make_vault_dirs(node, node_path)


async def auto_document(loop, root_node, data, output_path):
    tasks = []
    for d in data:
        m = d['metadata']
        task = loop.create_task(insert_knowledge(root_node, output_path,
                                                 m['app'], m['title'], d['summary'],
                                                 d['activity'], d['info'], d['ocr_results']))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)
        

async def insert_knowledge(root_node, output_path, app, title, summary, activity, info, ocr_results):
    node_choice = root_node
    depth = 0
    while True:
        async with node_choice.lock:
            new_node_choice = await choose_node(node_choice, app, title, summary, activity, '\n'.join(info))
        
        if new_node_choice is None:
            if node_choice is root_node:
                return
            break
        depth += 1
        if depth >= 10:
            print('WARNING: Depth exceeded, not inserting')
            return
        node_choice = new_node_choice

    ocr_lines = '\n'.join(t for b, t in ocr_results)

    async with node_choice.lock:
        if node_choice.content is not None and len(node_choice.content) > 0:
            print(f'Appending to node {node_choice.get_path()}')
            await append_to_node(node_choice, ocr_lines, app, title)
            updated_node = node_choice
        else:
            print(f'Creating node under {node_choice.get_path()}')
            new_node = Node()
            node_choice.add_children(new_node)
            updated_node = await complete_node(new_node, ocr_lines, app, title)
            if new_node is None:
                print('No knowledge found to index, node not created')
                return
            print(f'Created node {str(updated_node)}')
    
        save_path = os.path.join(output_path, updated_node.get_path().strip('/') + '.md')
        updated_node.to_markdown(save_path)
        

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python3 obsidianize.py <vault_path>')
        sys.exit(0)
    vault_path = sys.argv[1]

    data = load_data()
    root_node = init_graph(vault_path)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auto_document(loop, root_node, data, vault_path))
    