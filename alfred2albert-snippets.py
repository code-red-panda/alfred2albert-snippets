#!/usr/bin/env python

"""Alfred2Albert Snippets

Use your Alfred Snippets with Albert."""

from albertv0 import *
import glob
import re
import os
import json

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Alfred2Albert Snippets'
__version__ = '0.1'
__trigger__ = 'sn '
__author__ = 'coderedpanda'
__bin__ = 'sh'

SNIPPET_PATH = '/home/jake/Dropbox/Alfred/Alfred.alfredpreferences/snippets'
SNIPPET_EXT = 'json'
iconPath = ":python_module"


class snippets():

    def __init__(self, *args, **kwargs):
        self.path = args[0].rstrip('/')
        self.snippets_store = []

    def score(self, query, text):
        score = 0
        score += len(re.findall('\b{}\b'.format(query), text.lower()))
        score += len(re.findall('\b{}'.format(query), text.lower()))
        score += text.lower().count(query)
        return score

    def search(self, query):
        results = []
        # Calculate scores
        for snippet in self.snippets_store:
            temp = snippet.copy()
            temp['score'] = self.score(query, snippet['dir']) * 2
            temp['score'] = self.score(query, snippet['title']) * 1.5
            temp['score'] += self.score(query, snippet['text'])
            temp['score'] = self.score(query, snippet['file'])
            if temp['score'] > 0:
                results.append(temp)
        # Sort by scores
        results = sorted(results, key=lambda k: k['score'], reverse=True)
        return results

    def update_store(self):
        # Clear snippets
        self.snippets_store = []

        # Find json files
        files = []
        for filename in glob.iglob(self.path + '**/*.{}'.format(SNIPPET_EXT)):
            files.append(filename)
        for filename in glob.iglob(self.path + '/' + '**/*.{}'.format(SNIPPET_EXT)):
            files.append(filename)

        # Read json files
        for snippet_file in files:
            with open(snippet_file, 'r') as f:
                # Parse snippet
                filepath = snippet_file.strip()
                directory = os.path.basename(os.path.dirname(filepath))
                content = json.load(f)
                title = content['alfredsnippet']['name']
                text = content['alfredsnippet']['snippet']

                # Append to snippet store
                self.snippets_store.append({
                    'dir': directory,
                    'title': title,
                    'text': text,
                    'file': filepath,
                })

        info('[{}] Indexed {} snippet files.'.format(__prettyname__, len(self.snippets_store)))

snippets = snippets(SNIPPET_PATH)


def paste_directly(text):
    text = text.replace('\n\n','\r')
    os.system('sleep 0.02 && xdotool type "'+ text + '" &')
    return


def initialize():
    try:
        snippets.update_store()
    except Exception as e:
        critical(str(e))


def handleQuery(query):
    results = []
    if query.isTriggered:
        try:
            if query.string.strip():
                def copyToClipboard(text):
                    p = subprocess.Popen(
                        ['xclip', '-selection', 'c'], stdin=subprocess.PIPE)
                    p.communicate(input=bytes(text, 'utf-8'))

                for snippet in snippets.search(query.string.lower()):
                    results.append(
                        Item(id='%s%s' % (__prettyname__, snippet),
                             icon=iconPath,
                             text=snippet['dir'][0:12]+': '+snippet['title'],
                             completion=query.rawString,
                             actions=[
                                 ClipAction(text='Copy to Clipboard',
                                            clipboardText=snippet['text']),
                        ]))
            else:
                results.append(Item(id='%s-create' % __prettyname__,
                                    icon=iconPath,
                                    text=__prettyname__,
                                    subtext='Open Folder containing Snippets',
                                    completion=query.rawString,
                                    actions=[
                                        UrlAction(
                                            'Open', 'file://{}'.format(SNIPPET_PATH)),
                                        FuncAction(
                                            'Update Index', snippets.update_store)
                                    ]
                                    )
                               )
        except Exception as e:
            critical(str(e))
    return results
