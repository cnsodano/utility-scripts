## Gmail UX Improvements

CSS Rules to improve the Gmail user experience by offering customizable tools to improve one's ability to visually scan their inbox, organize priorities, and find what they're looking for. This will be turned into a simple CSS-injector extension with customization options available through the extension UI. Posted here in the meantime, as it can be used by people comfortable with generic CSS injector extensions like [Stylus](https://github.com/openstyles/stylus?tab=readme-ov-file)


## Highlighting Emails by Category
Gmail labels are a great way to organize emails by topic or priority, but they are not very easy to visually scan. You can set a filter to move them to a different view, but I wanted the option to quickly scan my inbox and pick out emails according to the topic of interest they are related to. Moreover, I wanted to have a clearer visual signal for emails that I've already replied to. This tool allows for selective highlighting of emails in the inbox according to the label assigned to them (which can be done automatically using the native Gmail filter feature).

![test](/gmail_UX_improvements/docs/email_highlighting_by_label.jpg)
In the image above, emails labeled "label" are highlighted in purple, and the email that was already replied to is grayed out. 

- Not yet implemented:
    - Setting priorities for coloring of an email that may have two labels applied to it, each with their own color rule
    - UI for customizing colors and automatically checking for contrast issues that would make it hard to read

## Removing Visual Noise From Search Results
This tool also allows customization of the way search query matches are presented. Rather than highlighting every string that matches the query in neon yellow, you can opt for more easily readable approaches like a heavy underline shown below.
![](/gmail_UX_improvements/docs/search_results_adjustment.jpg)

- Not yet implemented: 
    - UI for selecting preferred text decoration style and color/opacity/boldness/weight of the decoration