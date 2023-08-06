# This example illustrates how to use entity links
import os

import projectal
from projectal.enums import StaffType, PayFrequency, DateLimit, SkillLevel

projectal.api_base = os.environ.get('PROJECTAL_URL')
projectal.api_username = os.environ.get('PROJECTAL_USERNAME')
projectal.api_password = os.environ.get('PROJECTAL_PASSWORD')

# Create Staff entity. Note that links can only be set after entity creation.
n = len(projectal.Staff.list())
staff = projectal.Staff.create({
    "email": 'projectal-staff{}@example.com'.format(n),
    "firstName": "Firstname",
    "lastName": "Lastname",
    "staffType": StaffType.Consultant,
    "payFrequency": PayFrequency.Weekly,
    "payAmount": 600,
    "startDate": "2020-03-04",
    "endDate": DateLimit.Max,
})

location1 = projectal.Location.create({'name': 'Location 1'})
location2 = projectal.Location.create({'name': 'Location 2'})
location3 = projectal.Location.create({'name': 'Location 3'})
location4 = projectal.Location.create({'name': 'Location 4'})

# Link these locations to the staff
staff['locationList'] = [location1, location2, location3, location4]
staff.save()

# Somewhere else, you decide to fetch this staff and use its locations.
# To do this, you need to include the 'location' links in the request
# or you will not get the 'locationList' in the response.
staff = projectal.Staff.get(staff['uuId'], links=['location'])
for location in staff['locationList']:
    print(location['name'])

# To change the list, we do the same thing as before
staff['locationList'] = [location1, location2]
staff.save()

# To remove locations, pass an empty list ('None' will raise an exception)
staff['locationList'] = []
staff.save()

# Now let's link some skills. Skills are a little more complex since
# the skill link contains data within it. Here's how to do it.

# For convenience
def make_skill(name):
    # Skills have some mandatory fields
    return projectal.Skill.create({
        'name': name,
        'juniorLevel': 5.0,
        'midLevel': 5.0,
        'seniorLevel': 5.0
    })


skill1 = make_skill('Skill 1')
skill2 = make_skill('Skill 2')
skill3 = make_skill('Skill 3')

# Staff-to-Skill links need a 'skillLink' property to set the skill level.
# Add one to each of the skills we intend to link.
skill1['skillLink'] = {'level': SkillLevel.Junior}
skill2['skillLink'] = {'level': SkillLevel.Mid}
skill3['skillLink'] = {'level': SkillLevel.Senior}
# Save the new list
staff['skillList'] = [skill1, skill2, skill3]
staff.save()

# Performance note:

# The above will work, but the library will output some warnings:
# Warning: Fetching STAFF again with missing links: skill
# This happens when you try to save a list of links *without* fetching
# the entity with those links first. This requires the library to fetch them
# for you which requires a network request per object.

# If you intend to modify links, it is preferred to request all the links
# you need along with the object to minimize network activity:

staff = projectal.Staff.get(staff['uuId'], links=['skill', 'location'])
staff['skillList'] = [skill3, skill1]
staff['locationList'] = [location4, location2]
staff.save()

