Asyncio powered blog aggregation, static-website style!
=======================================================

This is a plugin for the `Pelican`_ static site generator.

It allows generating a page aggregating blog articles from other web sites.

.. _Pelican: https://getpelican.com

Usage
-----

Install this plugin::

    $ pip install pelican-aio-planet

Then, in your ``pelicanconf.py`` file, enable the plugin:

.. code-block:: python

    from pelican.plugins import aio_planet

    PLUGINS = [
        aio_planet,
        ...
    ]

.. note::

   If you plan to aggregate many feeds, it might be useful to only add the plugin in
   ``publishconf.py`` for faster rebuilds.

Next, declare the feeds you want to aggregate in your Pelican config file:

.. code-block:: python

    PLANET_FEEDS = {
        'Some amazing blog': 'https://example1.org/feeds/blog.atom.xml',
        'Another great blog': 'http://example2.org/feeds/blog.atom.xml',
    }

Write a `Jinja2`_ template for your aggregation page. For example, if the rest
of your website is generated from Markdown pages, then create a
``planet.md.tmpl`` file with the following contents:

.. code-block:: jinja

    Some blogs aggregated here.

    {% for article in articles %}
    # {{ article.title }}

    {% endfor %}

Finally, declare the template and destination page in your ``pelicanconf.py``
file:

.. code-block:: python

    PLANET_TEMPLATE = 'planet.md.tmpl'
    PLANET_PAGE = 'content/planet.md'


Then rebuild your website as usual using the ``pelican`` command line, and you
should have your blog aggregation page.

You'll probably want to rebuild your website periodically though, maybe with a
systemd timer or a cron job, to always fetch the latest articles in the feeds
you aggregate.

.. _Jinja2: https://jinja.palletsprojects.com/

Template design
---------------

The template for your aggregation page will be passed an ``articles`` variable,
containing the list of articles_ aggregated.

Each item of this list will have the following attributes:

* ``title``: The title of the article;
* ``updated``: The date at which the article was last updated, as a
  timezone-aware ``datetime`` object;
* ``author``: The author of the article;
* ``link``: The URL to the article on its original website;
* ``summary``: The summary text of the article;
* ``feed_name``: The name of the feed from which the article originated, as
  defined in the Pelican config file;

 .. _articles: https://docs.getpelican.com/en/stable/themes.html#article

Optional configuration
----------------------

You can have more control on the generated page, by setting a few more options
in your Pelican config file:

* ``PLANET_MAX_ARTICLES``: The maximum number of articles to show on the page.

  By default, 20 articles from all feeds will be added to the page.

* ``PLANET_MAX_ARTICLES_PER_FEED``: The maximum of articles from a single feed
  ending on the page.

  By default all articles of a given feed are considered.

* ``PLANET_MAX_SUMMARY_LENGTH``: The maximum number of words kept from the
  summary.

  By default the `summary` of the article will be the full text coming from
  the feed.

* ``PLANET_MAX_AGE_IN_DAYS``: The maximum age of an article to be included in
  the page.

  By default only articles no older than 180 days are added.

* ``PLANET_RESOLVE_REDIRECTS``: Resolve redirecting URLs to articles.

  By default redirects are not resolved.

Legalities
----------

pelican-aio-planet is offered under the terms of the
`GNU Affero General Public License, either version 3 or any later version`_.

We will never ask you to sign a copyright assignment or any other kind of
silly and tedious legal document before accepting your contributions.

In case you're wondering, we do **not** consider that a website built with
pelican-aio-planet would need to be licensed under the AGPL.

.. _GNU Affero General Public License, either version 3 or any later version: https://www.gnu.org/licenses/agpl.html
