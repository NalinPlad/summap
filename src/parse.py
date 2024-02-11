import json

def process_pdf_data_v2(pdf_data):
    # Split the pdf data into lines
    lines = pdf_data.split('\n')
    
    # List to hold group data
    groups = []
    
    # Variables to hold ongoing group data
    group_project = None
    group_members = []
    for line in lines:
        if line.startswith('Group'):  # This is a group title
            # If we have an ongoing group, save it
            if group_project is not None:
                groups.append({'id': len(groups) + 1, 'project': group_project, 'members': group_members})
            
            # Start a new group
            _, group_project = line.split(':', 1)
            group_project = group_project.strip()
            group_members = []  # Reset the members list
        else:  # These are group member details
            # Split the details on tabs
            member_details = line.split('\t')

            # Idx 0 is the field name, others are the details
            field = member_details[0]
            details = member_details[1:]
            
            if field == 'Name':  # Start a new set of members
                for detail in details:
                    group_members.append({'name': detail})
            elif field == 'Club Location':  # Add location to existing members
                for idx, detail in enumerate(details):
                    group_members[idx]['location'] = detail
            elif field == 'FileName':  # Add portrait to existing members
                for idx, detail in enumerate(details):
                    group_members[idx]['portrait'] = detail
    
    # Don't forget the last group
    groups.append({'id': len(groups) + 1, 'project': group_project, 'members': group_members})
    
    return groups




# read data from file passed as argument

data = open('./data.txt', 'r').read()


# Generate the groups JSON
groups_json = process_pdf_data_v2(data)
groups_json = json.dumps(groups_json, indent=4)

print(groups_json)