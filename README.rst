===============================================================
Example solution for the Extract Summit 2024 Coding Competition
===============================================================

There are 2 different solution spiders, one that uses AI parsing by default and
only uses custom parsing where AI fails, and one that uses custom parsing code
only, no AI.

Both solutions are implemented with the `e-commerce spider`_ from
zyte-spider-templates.

.. _e-commerce spider: https://zyte-spider-templates.readthedocs.io/en/latest/templates/e-commerce.html

To run the AI solution::

    scrapy crawl ecommerce -s SOLUTION=ai -a url="https://zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app/navigation"

To run the non-AI solution::

    scrapy crawl ecommerce -s SOLUTION=non_ai -a url="https://zzcvcpnfzoogpxiqupsergvrmdopqgrk-744852047878.us-south1.run.app/navigation"
