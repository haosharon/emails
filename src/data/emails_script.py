import sys, json, io

'''
We want to create JSON file of the form:
{
    emails: [
        {
            Sent: true
            From: 'blah',
            Cc: ['blah1', 'blah2'],
            To: ['blah1', 'blah2'],
            Time: 'blah'
        },
    ]
}
'''
def createCleanJsonFile(filename):
    print 'reading ' + filename
    json_data = open(filename, 'r').read()
    print 'loading ' + filename
    data = json.loads(json_data)

    emails = []
    print 'parsing ' + filename
    for d in data:
        email = {}
        sent = d[0]
        rest = d[1]
        email['Sent'] = len(sent) > 0

        subjects = rest.split('\r\n')
        for subject in subjects:
            split = subject.split(':')
            if len(split) == 2:
                key = split[0].strip()
                val = split[1].strip()
                if key == 'To' or key == 'Cc':
                    vals = val.split(',')
                    email[key] = vals
                else:
                    email[key] = val
        emails.append(email)

    final_json = {'emails': emails}
    # write json to file
    print 'writing ' + filename
    prefix = filename.split('.')[0]
    outfile = prefix + '_json.json'
    with open(outfile, 'w') as outfile:
        json.dump(final_json, outfile)

    print 'done!'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        createCleanJsonFile(filename)
