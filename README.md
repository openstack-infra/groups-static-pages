OpenStack Community portal static pages
=======================================

This repository holds the static content of groups.openstack.org website. You
can easily add or modify new content using the standard 
[OpenStack CI workflow](https://wiki.openstack.org/wiki/Gerrit_Workflow).

Structure
---------

Every .md file here define a specific page of the site, and consits of
a yaml style header to describe meta informations like title of the
page, content path, menu item, etc. and a markdown body.

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