---
title: OpenStack Groups Portal Contribution Guide
path: contribute
---


OpenStack Groups Portal Contribution Guide
=============================================

The Groups Portal based on Drupal 7.x [1] and Drupal Commons [2] distribution, and
the entire development process is integrated into the OpenStack CI system
including the code-review and automatic deployment of development and production
branch. If you want to contribute back a new portal feature or just simply
resolve a bug it is very important to setup a local development environment
with proper application stack to match the environment of staging and production
servers and avoid a lot's of unwanted issues. As we are using the OpenStack CI
the contribution process exactly match the official way [3], so this paper contains
additional project specific details.

Prerequisites
-------------

The Groups Portal production and development currently based on the following
application stack:

- Ubuntu 12.04 LTS
- Apache 2.2.22
- MySQL database server 5.5.38
- PHP 5.3.10 (extensions: mysql, gd)
- Drush 6.0
- Git
- Git-review
- Compass

Development workflow
--------------------

## Install site from scratch ##

As the first step of the development workflow we need to prepare an empty
database, register a drush site alias, clone the site source code from
git repository and finally install the site into an apache vhost docroot
directory.

### Create a mysql database ###

Create a new mysql database and grant permissions:

    $ mysqladmin -u username -p create groupsdev
    $ mysql -u username -p
    $ GRANT ALL ON groupsdev.* TO groupsdev@'localhost' IDENTIFIED BY 'urs3cr3tpassw0rd';

Where groupsdev will be the user name and urs3cr3tpassw0rd will be the password.

### Define drush site alias ###

Drush alias helps to shorten the access of local or remote Drupal installation.
For example you can set an alias as a default site root with `drush use @sitealias`
command.

The alias files must be placed in the global /etc/drush/aliases.drushrc.php or
in the local ~/.drush/aliases.drushrc.php files.

Example aliases.drushrc.php configuration:

    <?php
    $aliases['groupsdev'] = array(
      'uri' => 'groups-dev.local',
      'root' => '/var/www/groups-dev.local',
      'db-url' => 'mysql://groupsdev:12345678@localhost/groupsdev',
      'databases' => array(
        'default' => array(
          'driver' => 'mysql',
          'username' => 'groupsdev',
          'password'  => 'urs3cr3tpassw0rd',
          'port' => '',
          'host' => 'localhost',
          'database' => 'groupsdev',
        ),
      ),
    );

Further alias configuration examples available here [4].

Query available site aliases:

    $ drush sa
    @groupsdev
    default

### Build a working copy ###

The Groups Portal based on a Drupal Installation Profile, it means we are
keeping only the portal related modules in the git repository, and define all
of the original Drupal contributed modules and their patches in make files. The
drupal-org-core.make contains the defintion of Drupal core distribution and the
required core patches, the drupal-org.make file includes the defintion of
contrib modules, patches, themes and libraries.

Fetch the git repository and clone a working copy, then build the distribution
into site vhost directory:

    $ git clone git://git.openstack.org/openstack-infra/groups groups
    $ cd groups
    $ bash scripts/dev-build.sh /var/www/groups-dev.local

The /var/www/groups-dev.local is the site root registered in your apache
vhost file, this can be different in your local environment.

### Install Groups portal ###

    $ drush use @groupsdev
    $ drush si groups -y
    $ drush features-revert-all -y
    $ drush cc all

Now the portal available at your local site url, for example at
`http://groups-dev.local`.

### Rebuild theme css files ###

    $ cd /var/www/groups-dev.local/profiles/groups/themes/openstack
    $ bundle exec compass compile

## Import contents ##

The default installation will come with a really minimal content set, so
we need to import some initial content for testing.

### Import user group data ###

The user group data located at https://git.openstack.org/cgit/openstack-infra/groups-static-pages/tree/groups.json file, so you can easily modify or contribute back modification
through openstack-infra/groups-static project.

    $ drush import-user-groups

### Import static pages content ###

The static pages are holding markdown formatted content, during development
clone to a local directory from openstack-infra/groups-static-pages repository
and don't forget to set the groups_feeds_markdown_directory variable to
specify the location of the files

    $ git://git.openstack.org/openstack-infra/groups-static-pages /var/www/groups-static-pages
    $ drush vset groups_feeds_markdown_directory /var/www/groups-static-pages
    $ drush import-static-pages

### Import meetup events ###

The meetup events can be imported directly from meetup.com calendars, and
related user group meetup.com location extracted from meetup attribute of the
uploaded user group content.

    $ drush import-meetup-events

## Submit a patch ##

Start with low-hanging fruits and first try to fix a small bug or
do some housekeeping. The entire code-space maintained by the Groups
Portal team lives under the profiles/groups directory. If you like
to change anything, add a new drupal module, create a new feature,
you must place the files there. It is very important to know that
Drupal 7 store a lot of configuration setting, variable in database
and to make the code portable, we need to move those settings out
to code, using the Features module [5].

Follow the development workflow of OpenStack [6] and post
your patches to gerrit code review system.

    $ git checkout -b TOPIC-BRANCH
    $ git commit -a
    $ git review

Example commit message:

    Security upgrade of core and date module
    
    Update Drupal Core to 7.30 and Date module to 2.8.
    Related release notes available here:
    https://www.drupal.org/drupal-7.30-release-notes
    https://www.drupal.org/node/231188
    Change-Id: Ia2d04322fff4bc1f49e8cccada2ac2b267a3f9ca

After execution of successful jenkins check jobs, you need to get a
manual approval from project owners. If everything works well your
approved code will be automatically deployed into
groups-dev.openstack.org staging site.

[1] Drupal Core
https://www.drupal.org/project/drupal

[2] Drupal Commons
https://www.drupal.org/project/commons

[3] OpenStack How To Contribute
https://wiki.openstack.org/wiki/How_To_Contribute

[4] Drush alias examples
http://drush.ws/examples/example.aliases.drushrc.php

[5] Drupal Features module
https://www.drupal.org/project/features

[6] Gerrit workflow
https://wiki.openstack.org/wiki/Gerrit_Workflow
