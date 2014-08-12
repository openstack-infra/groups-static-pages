#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Make the UserGroups Wiki page.

Takes a JSON file made for the User Group Portal and generates a mediawiki
format page.
"""

import json
import logging

groups_json = json.load(open('groups.json'))
groups = {}
logger = logging.getLogger('makewiki')
continent_names = {'AF': 'Africa', 'AS': 'Asia Pacific', 'EU': 'Europe',
                   'ME': 'Middle East', 'NA': 'North America',
                   'SA': 'South America'}

def nice_label(attribute):
    nice_labels = {'facebook': 'Facebook Group', 'meetup' : 'Meetup details here',
                   'linkedin': 'LinkedIn Group', 'irc': 'IRC',
                   'twitter': 'Twitter', 'website': 'Website',
                   'google-groups': 'Google Group', 'blog': 'Blog',
                   'coordinators': 'Coordinators',
                   'google-plus': 'Google Plus Community',
                   'mailing-list': 'Mailing List'}

    if attribute in nice_labels:
        return nice_labels[attribute]
    else:
        return attribute

def make_header(continent_groups):
    print '__NOTOC__'
    print 'Welcome to the list of the OpenStack User Groups!'
    print
    print "Can't find one nearby? Want to start one? The\
[[Teams#Community_team|OpenStack International Community team]] is your main\
contact point. Join\
[http://lists.openstack.org/cgi-bin/mailman/listinfo/community the mailing\
list] and read [[OpenStackUserGroups/HowTo|the HowTo page]] if you are hosting\
or want to start a user group with meetups, hackathons and other social events\
talking about OpenStack and free/libre open source software for the cloud. You\
can also edit this page to add your group, but remember - we're an [[Open]]\
community."
    print
    print '<div style="column-count:3;-moz-column-count:3;-webkit-column-count:3">'
    for continent in sorted(continent_groups.iterkeys()):
        print ( "* '''[[#" + continent_names[continent] + '|' +
               continent_names[continent] + "]]'''" )
        for group in continent_groups[continent]:
            print "** [[#" + group + '|' + group + "]]"
    print '</div>'
    pass

def make_continent(continent):
    print "== " + continent_names[continent] + " =="

def make_group (group):
    print "=== " + group + " ==="
    for attribute in groups_json['groups'][group_indexes[group]]['attributes']:
        for key,value in attribute.iteritems():
            print '* ' + nice_label(key) + ': ' + value.encode('utf-8')
    print


continents = []
continent_groups = {}
group_indexes = {}
counter = 0
for group in groups_json['groups']:
    continent = group['location']['continent']
    if continent not in continents:
        continents.append(continent)
        continent_groups[continent] = []
    continent_groups[continent].append(group['title'])
    group_indexes[group['title']] = counter
    counter = counter + 1

make_header(continent_groups)

for continent in continents:
    make_continent(continent)
    for group in continent_groups[continent]:
        make_group(group)

