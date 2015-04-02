OpenStack Community portal static pages
=======================================

This repository holds the static content of groups.openstack.org website. You
can easily add or modify new content using the standard 
[OpenStack CI workflow](https://wiki.openstack.org/wiki/Gerrit_Workflow).

Structure
---------

Every .md file here defines a specific page of the site, and consists
of a yaml style header to describe meta information such as the title
of the page, content path, menu item, etc. The body of the file is
formatted in
[Markdown](http://daringfireball.net/projects/markdown/syntax).

Example:

```
---
title: Organizer tips
path: tips
menu: Organizer tips
---

Contents
========

Content goes here...

```
