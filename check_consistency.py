
import os
import sys
import re

#CHANGE THIS PATH TO LOCATION OF YOUR log_messages.*\.h FILES:
dev_home = r"C:\gwsource\TOCOM_PS-07.15.00\core\api\7.7\dev\coreex\priceserver"

print( "Scanning %s for log_messages_[something].h files." % dev_home )
sys.stdout.flush()
log_dictionary_headers = []
log_dictionary_regex = re.compile( r".*log_messages.*\.h$" )
for (root, dirs, files) in os.walk( dev_home ):
    for name in files:
        a_file = str(os.path.join( root, name ))
        if( None != log_dictionary_regex.match( a_file ) ):
            log_dictionary_headers.append( a_file )

print( "Found %d log_messages_[something].h files." % len(log_dictionary_headers) )
sys.stdout.flush()

comments_regex = re.compile( r".*?<message>(?P<messageComment>.*?)</message>", re.DOTALL)
bodies_regex = re.compile( r".*?(?P<cppFunc>(?:inline.*?)+void.*?\.Log\(.*?})", re.DOTALL)

comment_id_regex = re.compile( r".*?<id>(?P<id>.*?)</id>", re.DOTALL)
comment_sev_regex = re.compile( r".*?<sev>(?P<sev>.*?)</sev>", re.DOTALL)
comment_function_regex = re.compile( r".*?<function>(?P<funct>.*?)</function>", re.DOTALL)

body_id_regex = re.compile(r".*? Log[a-zA-Z0-9]*?\(.*?(?P<id>[0-9]{8})", re.DOTALL)
body_sev_regex = re.compile(r".*? Log[a-zA-Z0-9]*?\(.*?(?:tt_log::)+SV_(?P<sev>ERROR|WARNING|INFO|CRIT_ERR|RISKINFO|AUDIT|DEBUG)", re.DOTALL)
body_functionName_regex = re.compile( r".*?(?:inline.*?)+void.*?(?P<functionName>Log.*?)\(", re.DOTALL )

functionName_sev_regex = re.compile(r"Log(?P<sev>Critical|RiskInfo|Info|Warn|Err|Debug|Audit)")
fname_to_bodysev_dict = {'Critical':'CRIT_ERR', 'Err':'ERROR', 'Warn':'WARNING', 'RiskInfo':'RISKINFO', 'Info':'INFO', 'Audit':'AUDIT', 'Debug':'DEBUG'}
bodysev_to_commentsev_dict = {'CRIT_ERR':'CRITICAL ERROR', 'ERROR':'ERROR', 'WARNING':'WARNING', 'RISKINFO':'RISKINFO', 'INFO':'INFO', 'AUDIT':'AUDIT', 'DEBUG':'DEBUG'}

for header_file in log_dictionary_headers:
    print "\nCurrently working on file "+header_file
    readFile = open( header_file, 'r' )

    lines = "".join(readFile.readlines())
    body_matches = re.findall( bodies_regex, lines )
    comment_matches = re.findall( comments_regex, lines )
    
    parsed_bodies = {}
    parsed_comments = {}

    for match in body_matches:
        function_signature = re.search(body_id_regex, match)
        if function_signature is None:
            print "Inconsistent function name: " + match
        else:
            body_id = function_signature.group(1)
            body_sev = re.search(body_sev_regex, match).group(1)
            body_functionName = re.search(body_functionName_regex, match).group(1)
            if body_id in parsed_bodies:
                print "WARNING: found multiple functions with the same ID "+body_id
            parsed_bodies[body_id] = (body_sev, body_functionName)
        
    for match in comment_matches:    
        comment_id = re.search(comment_id_regex, match).group(1)
        comment_sev = re.search(comment_sev_regex, match).group(1)
        comment_function = re.search(comment_function_regex, match).group(1)
        if comment_id in parsed_comments:
            print "WARNING: found multiple comments with same ID "+comment_id
        parsed_comments[comment_id] = (comment_sev, comment_function)
        
    for body_key in parsed_bodies:
        
        body_id = body_key
        body_sev = parsed_bodies[body_key][0]
        body_functionName = parsed_bodies[body_key][1]
        
        # Check if severity in function name matches severity in function body
        function_signature = re.match(functionName_sev_regex, body_functionName)
        if function_signature is None:
            print "There is no severity in the function name: " + body_functionName
        else:
            functionName_sev = function_signature.group(1)
            if(fname_to_bodysev_dict[functionName_sev]!=body_sev):
                print "WARNING: Mismatch of severity in function name and body:"
                print "ID = "+body_id+", sev = "+body_sev+", function = "+body_functionName+" (name severity = "+functionName_sev+")"
            
        # Check if comment exists for this function
        if body_key not in parsed_comments:
            print "WARNING: Uncommented function:"
            print "Body   : ID = "+body_id+", sev = "+body_sev+", function = "+body_functionName
            continue
           
        comment_id = body_key
        comment_sev = parsed_comments[body_key][0]
        comment_function = parsed_comments[body_key][1]
        
        # Check that the comment matches the function body
        if (comment_id != body_id or 
            bodysev_to_commentsev_dict[body_sev] != comment_sev or
            comment_function != body_functionName ):
            print "WARNING: Mismatch in function and comment:"
            print "Comment: ID = "+comment_id+", sev = "+comment_sev+", function = "+comment_function
            print "Body   : ID = "+body_id+", sev = "+body_sev+", function = "+body_functionName
        
print "\nScript finished analyzing log headers."
sys.stdout.flush()
