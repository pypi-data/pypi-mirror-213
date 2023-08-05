🌿**ionicons_python**
==================

🍃**Description**
--------------------
This package containing the icons taken from `ionicons` website for using those easily in Python. You will not only get the basic icons from this package, but also get the social icons too, for example Linkedin, GitHub, Twitter, etc.

🍃**Installation**
============


#### **Stable release**


To install `ionicons_python`, run this command in your terminal:


    $ pip install ionicons_python



This is the preferred method to install `ionicons_python`, as it will always install the most recent stable release.



If you don't have `pip` installed, this `Python installation guide` can guide

you through the process.



_pip_: https://pip.pypa.io


_Python installation guide_: http://docs.python-guide.org/en/latest/starting/installation/

🍃**Usage**
---------------
After the installation is complete, use it with any of your favourite framework like **Flet, Streamlit** etc. Here I am giving an example of using **Flet**.

```python
from ionicons_python.ionicons_icons import *
import flet as ft

def main(page: ft.Page):
   page.add(ft.Image(linkedin_icon, width=24, height=24))

ft.app(target=main)
```
Don't use this icons with `Iconbutton` or  `Icon` of **Flet**.  Those only take flet inbuilt icons.

for **Streamlit**, below is an example:
```python
import streamlit as st
from ionicons_python.ionicons_icons import *

st.image(python_icon, width=30)
```
in the version 0.1.5, you can get some colored icons too. Those icons are available in the `extra_icons` module. The usage of it in **Flet** and **Streamlit** are shown below respectively.

##### **Flet**

```python
from ionicons_python.colored_icons import *
import flet as ft


def main(page: ft.Page):
    page.add(ft.Image(google_color_icon, width=24, height=24))


ft.app(target=main)
```
##### **Streamlit**

```python
import streamlit as st
from ionicons_python.colored_icons import *

st.image(python_color_icon, width=30)
```
if you want to know which colored icons are available, see the **Releases** section. All the icons provided here is in **.svg** format. So, if you change the size of the icon, it will still looks sharp.

if you want to see all the ionicons icons available, visit [this](https://ionic.io/ionicons) website.