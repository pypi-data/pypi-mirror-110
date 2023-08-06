# AutoCoconut, a workflow recording tool for Linux

**AutoCoconut** is a tool that enables tracking mouse and keyboard events to make a workflow report with screenshot illustrations. 
Such workflow report can be helpful when creating bug reports, tutorials, or test cases for GUI testing frameworks, such as OpenQA
and others.

**AutoCoconut** works on **X11** sessions only. The current version is **not Wayland ready**.

## Development

Currently, the development has reached **Phase 4**.

Which means that the script is able:

* record various events,  mouse buttons and actions (click, double click, drag, vertical scroll), keyboard events (press and release)
* identify various types of keys (modifiers, special keys, character keys, etc.)
* find pre-defined patterns in single events and interpret them
* take screenshots to illustrate the workflow (or create needles for OpenQA)
* produce various output - *raw* file, *json* file, or a workflow description in adoc and html.
* it has a GUI version which brings more functionality, such as edit, delete, or create events for the recorded workflow
* is packaged on PyPi for easy installation.


## How to install?

The script is being developed and tested on Fedora, so the following procedure is related to Fedora. For other distributions, you need to
make sure, that the following requirements are met:

* Python development packages.
* Tkinter libraries

On Fedora, you can follow this procedure:

1. Install the `python3-devel`.
2. Install `python3-tkinter`.

Then you can install the application:

1. `pip install --user autococonut`

## How to use?

See the documentation in the `docs` directory of the `autococonut` package.

