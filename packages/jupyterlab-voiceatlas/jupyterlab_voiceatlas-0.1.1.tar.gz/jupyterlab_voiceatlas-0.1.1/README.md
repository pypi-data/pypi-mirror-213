# Contents

- [Why?](#why)
- [Installation](#installation)
- [Usage](#usage)
- [Want to contribute?](#want-to-contribute)
- [Found an issue? Have suggestions?](#found-an-issue-have-suggestions)
- [Licensing](#licensing)
- [Notes](#notes-for-your-consideration)

<br/>

### Why?

This is the JupyterLab extension for Voice Atlas. The administrators of the platform can set the atlas to be used to provide help for the platform.

The extension also allows notebook creators to attach an atlas to a specific notebook that can be used later by other users that has the extension installed in their JupyterLab instance.

<br/>

### Installation

You cna use `pip` to install this extension:

```bash
pip install jupyterlab-voiceatlas
```

or

```bash
git clone https://github.com/Navteca/jupyterlab-voice-atlas
cd jupyterlab-voiceatlas/
npm install
python -m build
pip install jupyterlab_voiceatlas-<version>-py3-none-any.whl
```

<br/>
if the installation process runs successfully, check if the extension has been activated:

```
jupyter labextension list
jupyter serverextension list
```

<br/>
If not, you might need to run:

```
jupyter labextension enable --py jupyterlab_voiceatlas
jupyter serverextension enable --py jupyterlab_voiceatlas
```

<br/>

### Usage

Once the extension is installed a new menu "NLP" will be shown. It has a few options within it:

- Create new atlas: opens a new tab with the Voice Atlas Web App which will allow you to create a new atlas.
- Edit settings: allows you to set up the atlas id to be used by the extension.
- Open Chatlas: will open a new main area in JupyterLab with Chatlas in it. You can use it to talk to your atlas. You can also use voice as an input.
- Help: Will open a new tab with our Help Center in case you have doubts or want to provide feedback.
- About Voice Atlas: will open a popup with information about Voice Atlas.

<br/>

### Want to contribute?

First of all, thank you for taking the time to contribute!

Do you find this extension useful, with potential to be great and you like writing code? Please, don't hesitate to contribute. There is so much to do from improving an already existing feature, implement a new one to fixing bugs, etc.

There are a couple ways you can contribute to the extension:

- [Opening issues](https://github.com/Navteca/jupyterlab-voiceatlas/issues): you can open an issue either to report a bug, request an enhancement, ask a question, suggest a new feature, etc.
- [Pull Requests](https://github.com/Navteca/jupyterlab-voiceatlas/pulls): This would be awesome. We suggest you to open an issue or comment an issue before creating the Pull Request.

We are working on a contributor document and guidelines with additional information you might to work on the extension.

<br/>

### Found an issue? Have suggestions?

Please open an [issue](https://github.com/Navteca/jupyterlab-voiceatlas/issues), we would like to hear from you.

<br/>

### Licensing

[BSD 3-Clause License](LICENSE)

<br/>

### Notes for your consideration

- This project is in early stage. We are continuously working on it to make it better.
- This is the first extension we put out there. We are aware we have so much to learn from the FLOSS communities and that is one of the reasons we why decided to publish it.
