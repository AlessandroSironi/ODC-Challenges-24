# RateLimited
The challenge RateLimited was a challenge on Race Condition.
A race condition occurs in a computing system when the system's behavior is dependent on the sequence or timing of other events. 
The goal of this challenge was to bypass the timing constraints on the likes of a post submitted by the user.

## Vulnerability
In this case, the vulnerability that could be exploited from a Race Condition is the check of the timing of the likes, as the wait between one and the other was significantly high. However, the actual check required the other likes to have been already registered. 

## Exploit

The attached ```RateLimited.py``` is structured as follows:

- Some functions to handle all the actions useful on the website:
    - Register
    - Login
    - Post
    - Like
    - ... and some utility functions to:
        - Generate random strings.
        - Find the correcty post...
        - ... and extract its ID.
- The creation of the session.
- Sign Up and Sign In of the user in the session.

Then, the main exploit is wrapped in a while True loop, that:
- Creates a new post.
- Starts 4 threads that try to simultaneously like that post. 

The functions output the page only when the HTML contains the flag. 

### Flag
#flag{You_like_your_post_very_much!}