# Feedback on sprint 1

## Some useful git commands
I used these commands to get a quick read on what everyone did. Then I delved into specific files for a closer look.
* git log --all --graph --oneline --pretty=format:"%C(auto)%<|(20,trunc)%an%<(10)%h%<(60,trunc)%s%d"
* git log --all --numstat --oneline --author <author>

## Overall score: 10/10

As a group, you've made quite a bit of progress! Scraping the recipes, extracting the ingredients, and then wrestling
with equivalence is a good chunk of work for a first sprint. What has me concerned is that progress has been uneven.
There are other parts of the app, like the UI and especially the storage layer that have received much less attention.
I'm hoping to see these come to life soon!

## Specific callouts

* Colin, you did a prodigious amount of work right in the beginning. Good job getting the recipes off the ground!
  One skill you can develop further: when you put up a PR, try curating your commits first so you leave a readable
  git log. For example, most of the time when you have several commits on one task, they could be squashed together
  before landing the PR.
* Camila, I'm impressed with your determination to get all the ingredients sorted out. As I've mentioned in class, I
  think it may be time for you to make sure other other parts of the system are making progress as well. You can always
  return to the ingredients later if there's time!
* Nikil, I see you're working on the UI. It's great that you've made some progress on this, but I think it's going
  to take a bigger push to get the whole system hooked up.
* Sofiya, it looks like you got a late start on workingo on ingredients? I'm adjusting your score down to 8/10, but
  please let me know if I'm missing something!
* Sindhura, it looks like you worked mostly on the SQL connector, but there's not much code there. I'm adjusting your
  score down to 6/10, but again, please let me know if I'm missing something!
