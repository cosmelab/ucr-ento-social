# email templates usage guide

## how to send html emails

### method 1: python script via gmail api (recommended - best formatting preservation)

**this method preserves dark backgrounds and all HTML formatting perfectly.**

1. open terminal and navigate to the email-templates directory:
   ```bash
   cd /Users/lucianocosme/Projects/ucr-ento-social/email-templates
   ```

2. edit the `send-poll-announcement.py` script to update the recipient:
   - open the file in a text editor
   - find the line: `TO_EMAIL = "cosme.simple@gmail.com"`
   - change to your desired recipient email address
   - save the file

3. run the script using miniforge python:
   ```bash
   /opt/homebrew/Caskroom/miniforge/base/bin/python3 send-poll-announcement.py
   ```

4. if prompted, authorize the application in your browser
5. the email will be sent with perfect formatting!

**note**: this method requires:
- google api credentials (already configured in `/Users/lucianocosme/Library/CloudStorage/Dropbox/teaching/luciano/email_results/final/`)
- python with google api libraries (already installed in miniforge environment)

**important**: if you see "Exam PDF Sender" during authentication (from a previous project), you can update the app name:
1. go to https://console.cloud.google.com/
2. navigate to apis & services → oauth consent screen
3. click edit and change app name to "UCR Social Committee Emailer"
4. save changes (no need to regenerate credentials)

**to send to multiple recipients**: you can modify the script to loop through a list of email addresses or send to a mailing list.

### method 2: copy-paste to gmail (quick but may lose dark background)

1. open the html file in your web browser (double-click the .html file)
2. select all content (cmd+a on mac)
3. copy (cmd+c)
4. open gmail and click "compose"
5. paste directly into the compose window (cmd+v)
6. gmail will render the html automatically
7. add recipients and send!

**warning**: gmail may strip the dark background when copy-pasting. use method 1 for best results.

### method 3: outlook

1. open the html file in your browser
2. right-click and "view page source" or press cmd+u
3. copy all the html code
4. in outlook, go to new email
5. click the "..." menu → insert → attach file → browse
6. or use insert → html option (if available)
7. paste the html code
8. send!

## template files

### 1. poll-announcement.html
**purpose**: announce department polls with deadline
**when to use**: when sending poll invitations
**customization needed**: update deadline date if needed

### 2. general-announcement.html
**purpose**: general purpose template
**when to use**: for any department announcement
**customization needed**:
- replace "your email title here" with your title
- edit the message body
- update button text and link (or remove button)
- modify highlight box or remove if not needed

## email template design & formatting

### color scheme (updated for gmail compatibility)
the poll-announcement.html template uses colors optimized for gmail rendering:

- **body text**: #66ccff (bright sky blue) - gmail-safe color that maintains visibility
- **primary blue**: #003da5 (dark blue) - used for button background
- **golden accent**: #ffc947 (gold) - used for "the social committee" signature
- **orange**: #ff8c00 (dark orange) - used for deadline text
- **light blue links**: #4a90e2 - used for footer website/contact links
- **copyright text**: #7b9db8 - light faded blue for copyright
- **background colors**:
  - uses linear-gradient hack: `background: linear-gradient(#1a1a1a, #1a1a1a)`
  - gmail strips regular background-color but preserves linear-gradients
  - background image: body_bg.png from website shows around edges

### key design elements (current version)

1. **logo**: 100px height, centered in footer
2. **call-to-action button**:
   - blue background using linear-gradient: `background: linear-gradient(#003da5, #003da5)`
   - bright blue text (#66ccff)
   - centered using div wrapper and margin: 0 auto
3. **deadline**: centered orange text (#ff8c00) - stands out well
4. **footer structure**:
   - logo (100px, centered)
   - "social committee" in bold golden text (#ffc947)
   - "visit our website | contact us" in blue (#4a90e2)
   - copyright in light faded blue (#7b9db8)
5. **borders removed**: no borders for cleaner appearance
6. **background pattern**: body_bg.png visible around edges

### special css requirements

**critical**: the template requires a style block in the head to override browser dark mode defaults that can make text appear white instead of the intended cyan color:

```html
<head>
    <meta name="color-scheme" content="only light">
    <style>
        html { color-scheme: only light; }
        body { color: #00CED1 !important; }
        p { color: #00CED1 !important; }
        td { color: #00CED1 !important; }
    </style>
</head>
```

this css ensures:
- browser doesn't apply dark mode color overrides
- default text color is dark turquoise (#00ced1) with !important to prevent browser override
- inline color styles on specific elements (golden signature, blue headings, orange deadline) still override the default because they are more specific

### structure details

- uses html table layout (required for email client compatibility - divs don't work reliably)
- all styles must be inline (email clients don't support external css files or style imports)
- responsive width: 600px max for desktop, adapts automatically on mobile
- no emojis (unless explicitly requested by user)
- no colored left borders on cards (removed for cleaner, more modern look)
- all text alignment specified explicitly (left, center) - don't rely on defaults

## gmail compatibility issues & solutions

### the problem with gmail
gmail aggressively modifies email styles for "readability" and security:
- **strips background colors** - regular `background-color` declarations are removed
- **changes text colors** - adjusts colors based on what it thinks provides better contrast
- **ignores !important** - especially on mobile apps
- **inverts colors in dark mode** - light text becomes dark on iOS gmail app
- **forces white backgrounds** - overrides dark backgrounds with white

### solutions we implemented
1. **linear-gradient hack**: use `background: linear-gradient(#1a1a1a, #1a1a1a)` instead of `background-color: #1a1a1a`
   - gmail doesn't strip linear gradients
   - provides consistent dark background

2. **brighter text colors**: changed from #00ced1 to #66ccff
   - gmail less likely to modify brighter blues
   - maintains readability on dark backgrounds

3. **simplified structure**: removed unnecessary nested tables
   - fewer elements for gmail to interfere with
   - cleaner rendering across email clients

4. **centered button fix**: use div with align="center" and table with margin: 0 auto
   - ensures button stays centered in gmail

### known limitations
- **exact color matching**: gmail will still slightly modify colors
- **mobile dark mode**: ios gmail app may still invert some colors
- **professional alternative**: for exact branding, consider email marketing services (mailchimp, sendgrid)

## tips for effective emails

1. **subject line**: keep it clear and concise
   - ✅ "social committee polls - deadline oct 19"
   - ❌ "please read this important message"

2. **preview text**: first line shows in inbox
   - make your first sentence compelling

3. **length**: keep emails concise
   - most people skim emails
   - use bullet points for lists
   - bold important information

4. **call to action**: make it obvious what you want recipients to do
   - use the blue button for primary action
   - keep button text short (2-4 words)

5. **testing**: always send a test to yourself first
   - check on both desktop and mobile
   - verify all links work
   - make sure images load
   - test in multiple browsers if opening html file directly

## email best practices

### do:
- ✅ use clear, descriptive subject lines
- ✅ keep paragraphs short (2-3 sentences max)
- ✅ include a clear call-to-action
- ✅ proofread before sending
- ✅ send test email to yourself first
- ✅ thank people for their time/participation

### don't:
- ❌ use all caps (looks like shouting)
- ❌ include too many links
- ❌ make emails too long (keep under 300 words)
- ❌ forget to include contact information
- ❌ send without testing first

## troubleshooting

**images don't show:**
- make sure you're connected to the internet
- github images might take a moment to load
- if sending from local file, images need to be uploaded to github first
- verify image urls are using raw.githubusercontent.com format

**formatting looks wrong:**
- some email clients strip certain styles
- test in multiple clients if possible
- the templates are designed to work in gmail, outlook, and apple mail

**button doesn't work:**
- check the `href="..."` attribute in the anchor tag
- make sure the url is complete (includes https://)

**email looks different on mobile:**
- this is normal - emails adapt to screen size
- test on your phone before sending to department
- 600px width becomes responsive on smaller screens

**text appears white instead of cyan when opening html file:**
- this happens when browser dark mode overrides inline styles
- ensure the `<style>` block with `color-scheme: only light` is present in the `<head>` section
- use cmd+shift+r (mac) or ctrl+shift+r (windows) to hard refresh browser when testing
- try testing in incognito/private browsing mode to rule out extensions

## editing the poll announcement

to change the deadline:

1. open `poll-announcement.html` in a text editor
2. find: `deadline: sunday, october 19, 2025 at 11:59 pm`
3. replace with new date
4. save and send!

to change poll descriptions or links:

1. find the poll section you want to edit
2. modify the text within the `<p>` tags
3. update the `href` attribute in the button link if needed
4. test in browser before sending

## creating new email templates

when creating new email templates from scratch or modifying existing ones, follow this structure:

### required elements:

1. **head section**:
   - must include `<meta name="color-scheme" content="only light">`
   - must include style block with default text color (#00ced1) and `!important` flags
   - include viewport meta tag for mobile responsiveness

2. **body tag**:
   - set default color on body tag as backup
   - include font-family, background-color, and basic reset styles

3. **main container**:
   - 600px width table (not div)
   - dark background (#0d0d0d for outer, #1a1a1a for card)
   - cellpadding="0" cellspacing="0" border="0" (required for consistency)

4. **content area**:
   - use inline styles for all colors, spacing, fonts, and formatting
   - specify text-align explicitly (center or left)
   - use table-based layouts for structure, not css flexbox or grid

5. **footer structure**:
   - include logo at 100px height with drop-shadow filter
   - "social committee" in bold golden text (#ffc947)
   - blue links (#003da5) for website and contact
   - light faded blue (#7b9db8) for copyright

6. **color consistency**:
   - match website color scheme
   - use cyan (#00ced1) for body text
   - use blue (#003da5) for headings/links
   - use gold (#ffc947) for branding/signatures
   - use orange (#ff8c00) for urgent items like deadlines

### file naming convention:
- use lowercase with hyphens: `poll-announcement.html`, `event-invitation.html`
- matching guide file: `usage-guide.md` (all lowercase, not uppercase)
- avoid spaces, underscores, or capital letters in filenames
