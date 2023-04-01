# Windows Distributable

**By** Royston E Tauro

**Email:** tauro.royston@gmail.com

**Github**: [lucasace](https://github.com/lucasace)

## Synopsis

Metacall was built initially mainly towards the linux ecosystem but as it is going towards cross platform , the windows distributable needs to undergo some changes to keep up with the rate metacall is growing.

I have been contributing to metacall for sometime now and my contributions were all mainly focused on improving the windows distributable package. I am gald to say that I was part of a few essential contributions to the package which includes fixing the install scripts on windows [#11](https://github.com/metacall/install/pull/11),  fixing python problems in the distributable like [#20](https://github.com/metacall/distributable-windows/pull/20), [#341](https://github.com/metacall/core/pull/341),  added tests for all the package managers metacall supports, and built workflows testing the install and windows packages.

My project Idea would mainly include the following features:
* Testing and Adding the languages metacall currently supports to the windows distributable
*  Currently the tests only support package managers and to be honest are very messy, will clean the tests for each language
*  Added enough CI/CD workflows to ensure smooth working of the package after metacall install is complete

## Implementation Plan

This project would essentially have three phases:

### 1. Identifying problems with the language support and resolving them

This phase essentially begins before the coding period, I will be exploring the codebase and testing out all the language supports on windows to see if they work or why they dont work. This part should  be completed prior to the coding period.
Once done, I will have a document ready of all the languages and the results of if they work and why they dont work, if they dont work , whats the Root Cause Analysis or RCA of it.

The second part of this phase will be resolving these issues which will begin once the coding period begins

### 2. Writing coverage tests for the languages which are supported

Once the first phase completes, I will be writing coverage tests for all the languages, and these tests will be extensive and will include all the features provided by metacall for that language. Currently the tests are only limited to running a simple `sum` function.

### 3. Testing the changes on the install script

After all the changes are completed, a comprehensive CI/CD pipeline needs to be built, covering all changes and on any change in metacall core, we should hope it doesnt break the installation on windows as currently this seems to be the case for it



## Timeline

 * #### May 4- May 28 (Pre coding period)
Understand more of the projects, if I have missed any points from my understanding of the project, Build the environment on my system and start creating a document understanding the current problems per language.

* #### May 29 - July 2

Completing the first phase of the project, fix all problems related to the languages, document my progress  and begin working on tests

* #### July 2 - July 30

Begin working on coverage tests for all the languages implemented.

* #### July 30 - Aug 10

Implement the CI/CD pipeline and test on the install script

* #### Aug 10 - Aug 28
Have a two week buffer incase of any delays.


### Regards 

Thank you for taking the time to look at my proposal , will be open for a discussion on it.

You can reach me at tauro.royston@gmail.com. discord @lucasace#8064 and my github username is [lucasace](https://github.com/lucasace)







