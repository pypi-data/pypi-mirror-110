Libervia CSS Framework
======================


Libervia comes with generic CSS styling which is thought to be re-usable. If you create a new theme/site, you don't have to use it and can use something totally different, but building on top of Libervia CSS make theming more easy and consistent as you can re-use existant components without changing the classes.

Bases
-----
All CSS files must be in the ``static`` directory of your theme. Following names are assumed to be in this directory.

Libervia may link one to several style sheets when it renders a template. It will always links the following file (if they exist):
   - ``fonts.css`` (fonts loading)
   - ``styles.css`` (main CSS style, see below)
   - ``styles_extra`` (customizations of main style)

Then it will link styles relative to the current theme (where path is joined with a ``_``). For instance, if your template is ``blog/article.html``, the following files will be linked (in this order, and if they exists):
   - ``blog.css``
   - ``blog_article.css``

You can suffix any style sheet (but ``fonts.css``) with ``_noscript``: this suffixed file will be loaded only when javascript is not available, allowing to adapt your template to such case.

The main CSS styling is ``styles.css``, it contains styles for every major elements used in Libervia.
CSS in Libervia follows ``BEM`` (Block Element Modifier) conventions.

If you create a new theme, you should not touch ``styles.css``, but work on ``styles_extra.css`` instead. The later doesn't exist in default Libervia theme on purpose.

There are a few "magic" classes, which imply some DOM modification when Javascript is enabled, see below.
Last but not least, there is also a "state system", i.e. classes which are dynamically changed during runtime.

Magic Classes
-------------
Magic classes are classes which imply a modification of DOM when the page is loaded and Javascript is activated.
The modification is done by a script launched by ``base/base.html``.
There are only a few of them:

box--expand
   When this class is applied, the box will be folded when higher than 250px, and 2 "expand zone" (buttons)
   will be added on top and bottom of the box to expand/reduce it.

state_init
   This is linked to state system (see below). When applied, the element will keep the ``state_init`` class until
   clicked for the first time, then it will apply other magic classes effects if suitable.

State System
------------
A basic state system is used to do some dynamic operation (like (un)folding a box). The two main states are:

state_init
   This class is present until first clicked

state_clicked
   This state is used with some magic classes (e.g. ``box-expand``) or when a clicking method from ``common.js``
   is used on an element (e.g. ``clicked_cls``). The classes is toggled on each click.

Some classes are used to manipulate elements according to state:

show_if_init
   Display this class only if in ``state_init``.

show_if_parent_clicked
   display this class only if **parent** is in ``state_clicked``

show_if_parent_not_clicked
   display this class only if **parent** is **not** in ``state_clicked``

show_if_grandparent_clicked
   display this class only if **grandparent** is in ``state_clicked``

show_if_grandparent_not_clicked
   display this class only if **grandparent** is **not** in ``state_clicked``
