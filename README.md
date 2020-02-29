# Alfred2Albert Snippets

All the credit for this goes to [dynobo's SnippetStore](https://github.com/dynobo/SnippetStore). I am trying to make the switch from Mac to Linux and Alfred's Snippets are a major part of my productivity. I found dynobo's SnippetStore extension and was impressed by his great work. I was able to modify his extension to work with Alfred's Snippets, which will help in my transition.

All you need to do is modify the SNIPPET_PATH to point Alfred2Albert Snippets to your Alfred Snippets directory. For example, mine are sync'd across my Mac and Linux via Dropbox:
```
SNIPPET_PATH = '/home/jake/Dropbox/Alfred/Alfred.alfredpreferences/snippets'
```
This extension cannot add/edit/delete snippets. This should still be done on your Mac directly in Alfred. Changes will then sync to Dropbox and update in Albert.

I am using Alfred v3 and have not tested with Alfred v4.

## Features
- Triggered by "sn"
- Search your Alfred Snippets
- Rank results based on number, position and sourroundings of occurrences
- Actions:
   - Copy to clipboard
   - Open Snippet-Folder ("sn" without searchterm)

## Dependencies
- [xdotool](https://www.semicomplete.com/projects/xdotool) *search for it in your distro's repository*

## Manual installation
Download [alfred2albert-snippets.py](https://github.com/code-red-panda/alfred2albert-snippets/blob/master/alfred2albert-snippets.py) to one of Albert Launchers folders for python extensions:
- ~/.local/share/albert/org.albert.extension.python/modules
- /usr/local/share/albert/org.albert.extension.python/modules
- /usr/share/albert/org.albert.extension.python/modules

Adjust the configuration, which is currently hard coded:
- `SNIPPET_PATH = '/home/jake/Dropbox/Alfred/Alfred.alfredpreferences/snippets'` - Folder, where your Alfred Snippets are stored

Activate in Albert:
- Open Albert Launcher's Settings
- Go to "Extensions"
- Make sure the "Python"-Extension is activated
- In the Python Extension settings, activate "Alfred2Albert Snippets"

## Snippets
You can search by directory or snippet name.

The results will display the first 12 characters of the snippet's parent directory followed by the snippet name.
![screenshot](./search_example.png)
