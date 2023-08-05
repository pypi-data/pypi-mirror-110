==================================
Libervia Web Framework Quick Start
==================================

This documentation will help you getting started with Libervia Web Framework to create your first web site.

Creating an external site
-------------------------

First let's get basic vocabulary we'll use: a "site" is all the data necessary to display a full web site.
A site have one or more "themes" which is a way to display it. A theme may be anything from simple style change (e.g. "dark" theme, or "high contrast"), to a complete rework of the apparence of a site, but keep the same pages structure (see below). If you want to change pages structure, you have to make a new site.
A site is made of pages and templates. Pages are the code which gather and manipulate the data, and templates are about the final rendering.
Don't worry too much if you don't get it yet, we'll see that with a practical example.

We'll create the classical "Salut à Toi le monde" site.

You first have to choose a location were your site will be. We name "external site" any site which is not the standard Libervia site.
Choose a location, for instance ``~/dev/libervia_quick_start`` then create the following hierarchy or directories inside it:

- templates/
   - default/
- pages/
- i18n/

``templates`` is where you'll put… template, used to render the final pages. ``default`` is a theme name, this one is special as is it the main theme of your site and must always exist.
``pages`` is where you'll put python code to manipulate data of your site.
``i18n`` is used for translating your site in other languages, but we'll get to this later.

Now we have to declare this new site to Salut à Toi and Libervia. When installing Salut à Toi, you should have created a ``sat.conf`` file, if not, just create one at ``~/.sat.conf``.
Edit this file, and in the section ``[DEFAULT]``, add the following setting:

.. sourcecode:: javascript

   sites_path_public_dict = {
       "quick_start": "~/dev/libervia_quick_start"
       }

This declare the templates of your websites, you'll now be able to use them with tools like ``jp``.

Now you have to add your site to Libervia. Choose a host name, and link it to the site name by adding a ``vhost_dict`` setting in your ``[libervia]`` section of ``sat.conf``:

.. sourcecode:: javascript

   vhosts_dict = {"quickstart.int": "quick_start"}

That means that when you'll get to ``quickstart.int``, you'll land to your own site instead of official Libervia one.

Last but not least, you have to declare this website as alias for your localhost during developments. On GNU/Linux, this is done by editing ``/etc/hosts`` (as root user), to have something like that::

   127.0.0.1       localhost.localdomain   localhost quickstart.int
   ::1             localhost.localdomain   localhost quickstart.int

To see your website, you'll have to use the specified host name, and the port used by Libervia (8080 by default). If you kept default configuration, let's go to http://quickstart.int:8080.

But for now, you'll just see ``No Such Resource`` (if you see standard Libervia site, that means that something is not working, you can check for assistance in our XMPP room at `sat@chat.jabberfr.org <xmpp:sat@chat.jabberfr.org?join>`_).

All right? Good, let's start then.

A first template
----------------

For this simple page, we won't have any data to manipulate, so let's start directly with the template.
Create a ``salut.html`` file at ``templates/default/salut/salut.html`` inside your development directory, and put the following content inside:

.. sourcecode:: jinja

   {% if not embedded %}{% extends 'base/base.html' %}{% endif %}

   {% block body %}
   Salut à Toi le monde !
   {% endblock body %}

Let's explain a bit.

The template use Jinja2_ engine, which is easy to learn and powerful. You have the documentation available on the official website, you should read in particular the `Template Designer Documentation <http://jinja.pocoo.org/docs/latest/templates/>`_.

.. sourcecode:: jinja

   {% if not embedded %}{% extends 'base/base.html' %}{% endif %}

This firt line should be present on every front page, it extends the base template which handle many things for you and to facilitate integration with the backend. "But I have not written any ``base/base.html`` template" you may say. That's right, that's because SàT template engine is looking for file in several places. When you link a template, first it will check the current theme of your site, then the ``default`` theme, and finally the ``default`` theme of SàT official site. That allows you to have access to the generic features like the backend integration.

.. sourcecode:: jinja

   {% block body %}
   Salut à Toi le monde !
   {% endblock body %}

The ``base/base.html`` define some common blocks (check Jinja2_ documentation for the definitiion and instructions on how to use blocks). Those blocks are ``title``, ``favicon``, ``body``, ``footer``, ``main_menu``, ``confirm`` and ``category_menu``. For now, you can only take care of the first 4.
The ``body`` block is, as you can guess, the main area of your page, the perfect place to say hello to the world.

A first page
------------
We have a template, but we need a page to use it.
Pages are put in a directories hierarchy which correspond directly to your URL hierarchy, simple! To be used as a Libervia page, a directory must contain a file named ``page_meta.py``. So to create your first page, you just have to create the file ``pages/salut/page_meta.py`` and put this inside:

.. sourcecode:: python

   #!/usr/bin/env python2.7
   #-*- coding: utf-8 -*-

   template = "salut/salut.html"

And that's it! Note that we are still using Python 2.7, as the rest of Salut à Toi ecosystem. This will change for ``0.8`` release which will see the port of the whole project to Python 3.

Now you certainly want to see your rendered page. For this you'll have to restart Libervia (automatic reloading is not yet available for pages, but it works for templates). In Libervia logs, you should see something like this::


   [libervia.server.pages] [quickstart.int] Added /salut page

Now let's go to http://quickstart.int:8080/salut and admire your first Libervia page :).

But if you go to http://quickstart.int:8080 you still see this annoying ``No Such Resource``, would not it be nice to land directly to your salut page?
All you have to do for that, is to add a couple of lines in your ``sat.conf``, once again in ``[libervia]`` section:

.. sourcecode:: javascript

   url_redirections_dict = {
     "quick_start": {
         "/": "/salut"
         }
     }

That means that the root of your ``quick_start`` site is redirected to your ``salut`` page. After restarting Libervia, you can check again http://quickstart.int:8080, you should see the welcoming message.

.. _Jinja2: http://jinja.pocoo.org/
